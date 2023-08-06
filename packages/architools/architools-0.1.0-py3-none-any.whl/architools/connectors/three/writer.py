import gzip
import uuid
from jinja2 import Template

from OCC.Core.Tesselator import ShapeTesselator
from OCC.Core.TopoDS import TopoDS_Wire

from architools.geometry.brep import brep_vertices
from architools.connectors.three.templates.geometry import buffer_geometry as buffer_geometry_template
from architools.connectors.three.templates.scene import scene as three_scene_template
from architools.connectors.three.templates.material import material as default_material

class ThreeWriter():
  """For meshes, use the built-in ShapeTesselator from pythonocc-core"""

  def serialize_scene(self, scene):
    """Expects an architools scene object and returns 
    JSON Object Scene format 4 for three.js"""
    
    three_scene = Template(three_scene_template)
    geoms = []
    # default_material = Template()

    for o in scene.objects:
      if isinstance(o, TopoDS_Wire):
        geom = serialize_wire(o)
      else:
        geom = shape_to_three_json(o)

      geoms.append(geom)
    
    props = {
      'geoms': geoms,
      'materials': [],
      'guid': 'testguid',
      'scene_children': [],
    }

    scene_json = three_scene.render(props)
    
    return scene_json



def shape_to_three_json(s):
  """For meshes, use the built-in ShapeTesselator from pythonocc-core"""

  # compute the tessellation
  tess = ShapeTesselator(s)
  tess.Compute()

  # convert to threejs json
  three_json = tess.ExportShapeToThreejsJSONString('UDTools')

  return three_json
  # b = bytes(three_json, 'utf-8')
  # c = gzip.compress(b)
  # return c


def serialize_wire(s):
  """Converts wires to threejs json"""

  vx = brep_vertices(s)
  vx = [[v.X(), v.Y(), v.Z()] for v in vx]
  vx = [i for sl in vx for i in sl] # flatten list

  params = {
    'uuid': str(uuid.uuid1()),
    'vertex_coords': vx
  }

  three_json = Template(buffer_geometry_template).render(params)

  return three_json
