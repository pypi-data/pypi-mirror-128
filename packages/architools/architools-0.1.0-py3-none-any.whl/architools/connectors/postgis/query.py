# from connectors.postgis.queries import (
#     building_by_bin,
# )
# from connectors.postgis.template import run_query
# from connectors.wkt import polyhedralsurfacez_to_brep


# def building_by_id(bin, crs):
  
#   params = {
#     "bin": bin,
#     "center_x": 1004374,
#     "center_y": 242209
#   }

#   results = run_query(building_by_bin.template, params)

#   shape = polyhedralsurfacez_to_brep(results[0].wkt)
 
#   bldg = {
#       "bin": bin,
#       "shape": shape
#   }

#   return bldg
