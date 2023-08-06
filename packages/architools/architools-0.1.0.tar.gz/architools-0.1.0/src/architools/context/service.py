from geography.context import aoi_default as aoi
from generated.scene_pb2_grpc import SceneServiceServicer
from generated.scene_pb2 import (
  ExistingBuildingResponse,
  GroundSurfaceResponse,
  GroundTextureResponse,
)
from connectors.postgis import run_query
from connectors.three import serialize_shape
from geometry.conversion import tinz_to_brep, polyhedralsurfacez_to_brep
from queries.building_bybin import template as building_template
from queries.ground import template as ground_template
from queries.orthoimagery_bybounds import template as texture_template

class SceneServicer(SceneServiceServicer):
  """Provides methods for fetching scene elements for context via RPC."""

  def MakeGroundSurface(self, request, context):
    params = {
      'center_x': aoi.representative_point().x,
      'center_y': aoi.representative_point().y,
      'bounds': request.geom,
    }

    result = run_query(ground_template, params) # expect one item
    geom = result[0].geom

    occ_shape = tinz_to_brep(geom)
    three_shape = serialize_shape(occ_shape)

    return GroundSurfaceResponse(geom=three_shape)


  def GetGroundTexture(self, request, context):
    params = {
      'bounds': request.geom,
    }

    result = run_query(texture_template, params)
    jpg = result[0].jpg # expect one result
    jpg = jpg.tobytes() # get bytes from memoryview object

    return GroundTextureResponse(jpg=jpg)


  def GetExistingBuilding(self, request, context):
    params = {
      'center_x': aoi.representative_point().x,
      'center_y': aoi.representative_point().y,
      'bin': request.id,
    }

    result = run_query(building_template, params)
    geom = result[0].wkt # expect one result

    occ_shape = polyhedralsurfacez_to_brep(geom)
    three_shape = serialize_shape(occ_shape)

    return ExistingBuildingResponse(geom=three_shape)
