# -*- coding: utf-8 -*-

# py_tools_ds - A collection of geospatial data analysis tools that simplify standard
# operations when handling geospatial raster and vector data as well as projections.
#
# Copyright (C) 2016-2021
# - Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences Potsdam,
#   Germany (https://www.gfz-potsdam.de/)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Daniel Scheffler"

import warnings
import json
from typing import Union

from shapely.geometry import shape, Polygon, MultiPolygon, GeometryCollection
from osgeo import gdal, osr, ogr
import numpy as np

from ...io.raster.gdal import get_GDAL_ds_inmem
from ...processing.progress_mon import ProgressBar, Timer
from ..raster.reproject import warp_ndarray
from ..vector.topology import get_bounds_polygon, polyVertices_outside_poly, get_overlap_polygon


def raster2polygon(array: np.ndarray,
                   gt: Union[list, tuple],
                   prj: Union[str, int],
                   DN2extract: int = 1,
                   exact: bool = True,
                   maxfeatCount: int = None,
                   min_npx: int = 1,
                   timeout: float = None,
                   progress: bool = True,
                   q: bool = False
                   ) -> Union[Polygon, MultiPolygon]:
    """Calculate a footprint polygon for the given array.

    :param array:             2D numpy array
    :param gt:                GDAL GeoTransform
    :param prj:               projection as WKT string, 'EPSG:1234' or <EPSG_int>
    :param DN2extract:        <int, float> pixel value to create polygons for
    :param exact:             whether to compute the exact footprint polygon or a simplified one for speed
    :param maxfeatCount:      the maximum expected number of polygons. If more polygons are found, every further
                              processing is cancelled and a RunTimeError is raised.
    :param min_npx:           minmal polygon area to be included in the result (in numbers of pixels)
    :param timeout:           breaks the process after a given time in seconds
    :param progress:          show progress bars (default: True)
    :param q:                 quiet mode (default: False)
    :return:
    """
    array = array.astype(int)

    # TODO
    if maxfeatCount is not None:
        warnings.warn("'maxfeatCount' is deprecated and will be removed soon.", DeprecationWarning)  # pragma: no cover

    # gdal.Polygonize ignores the 0
    if DN2extract == 0:
        array = array == 0
        DN2extract = 1

    assert array.ndim == 2, "Only 2D arrays are supported. Got a %sD array." % array.ndim
    gt_orig = gt
    shape_orig = array.shape

    # downsample input array in case it has more than 1e8 pixels to prevent crash
    if not exact and array.size > 1e8:  # 10000 x 10000 px
        # downsample with nearest neighbour
        zoom_factor = (8000 * 8000 / array.size) ** 0.5
        array, gt, prj = warp_ndarray(array, gt, prj,
                                      out_gsd=(gt[1] / zoom_factor,
                                               gt[5] / zoom_factor),
                                      rspAlg='near',
                                      q=True)

    src_ds = get_GDAL_ds_inmem(array, gt, prj)
    src_band = src_ds.GetRasterBand(1)

    # Create a GeoJSON OGR datasource to put results in.
    srs = osr.SpatialReference()
    srs.ImportFromWkt(prj)

    drv = ogr.GetDriverByName("GeoJSON")
    path_geojson = "/vsimem/polygonize_result.geojson"
    dst_ds = drv.CreateDataSource(path_geojson)
    dst_layer = dst_ds.CreateLayer('polygonize_result', srs=srs)
    dst_layer.CreateField(ogr.FieldDefn("DN", 4))

    # set callback
    callback = \
        ProgressBar(prefix='Polygonize progress    ',
                    suffix='Complete',
                    barLength=50,
                    timeout=timeout,
                    use_as_callback=True) \
        if progress and not q else Timer(timeout, use_as_callback=True) if timeout else None

    # run the algorithm
    status = gdal.Polygonize(src_band,
                             src_band,  # .GetMaskBand(),
                             dst_layer,
                             0,
                             ["8CONNECTED=8"] if exact else [],
                             callback=callback)

    del dst_layer, dst_ds

    # handle exit status other than 0 (fail)
    if status != 0:
        errMsg = gdal.GetLastErrorMsg()

        # Catch the KeyboardInterrupt raised in case of a timeout within the callback.
        # It seems like there is no other way to catch exceptions within callbacks.
        if errMsg == 'User terminated':
            raise TimeoutError('raster2polygon timed out!')

        raise Exception(errMsg)

    # read virtual GeoJSON file as text
    f = gdal.VSIFOpenL(path_geojson, 'r')
    gdal.VSIFSeekL(f, 0, 2)  # seek to end
    size = gdal.VSIFTellL(f)
    gdal.VSIFSeekL(f, 0, 0)  # seek to beginning
    content_str = gdal.VSIFReadL(1, size, f)
    gdal.VSIFCloseL(f)

    gdal.Unlink(path_geojson)

    # convert JSON string to dict
    gjs = json.loads(content_str)

    gc = GeometryCollection([shape(f["geometry"]).buffer(0)
                             for f in gjs['features'] if f['properties']['DN'] == str(DN2extract)])

    # convert GeometryCollection into MultiPolygon
    polys = []
    for i in gc.geoms:
        if isinstance(i, Polygon):
            polys.append(i)
        else:
            polys.extend(list(i.geoms))

    # drop polygons with an area below npx
    if min_npx > 1:
        area_1px = gt[1] * abs(gt[5])
        area_min = min_npx * area_1px

        polys = [p for p in polys if p.area >= area_min]

    poly = MultiPolygon(polys)

    # the downsampling in case exact=False may cause vertices of poly to be outside the input array bounds
    # -> clip poly with bounds_poly in that case
    if not exact:
        bounds_poly = get_bounds_polygon(gt_orig, *shape_orig)

        if polyVertices_outside_poly(poly, bounds_poly, 1e-5):
            poly = get_overlap_polygon(poly, bounds_poly)['overlap poly']

    return poly
