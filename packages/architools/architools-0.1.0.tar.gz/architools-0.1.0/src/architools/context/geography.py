import shapely.wkt as wkt
from pyproj import CRS, Proj, Transformer

# get the nearest street on the city map
def nearest_street(start_pt, direction):
  print('not implemented')

def zone_by_context(pt):
  print('not implemented')

def base_plane_elevation(pt):
  print('not implemented')

aoi_default_wkt = 'POLYGON ((1008124.01165114 233997.49418184, 1008487.31714591 233858.35590725, 1008373.94521846 233568.48450184, 1008006.77477162 233746.27229716, 1008124.01165114 233997.49418184))'

aoi_default = wkt.loads(aoi_default_wkt)

# next, specify bbls
bbl_array = ['2025770020', '2025770022']

crs_wgs84 = CRS('EPSG:4326')
crs_webmercator = CRS('EPSG:3857')
crs_nystateplane = CRS('EPSG:2263')

wgs84_to_nystateplane = Transformer.from_crs(
    crs_wgs84, 
    crs_nystateplane,
    always_xy=True
  ).transform

point_nycityhall_wgs84 = [
  40.71273670544531,
   -74.00600376511792
]

test_studyarea_wgs84 = 'POLYGON ((-73.993996 40.67882, -73.99328800000001 40.67847, -73.993723 40.677831, -73.994533 40.678238, -73.993996 40.67882))'
