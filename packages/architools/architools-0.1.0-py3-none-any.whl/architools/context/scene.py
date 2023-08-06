from collections import namedtuple
from typing import NamedTuple
from uuid import uuid4 as uuid

from architools.connectors.postgis.template import run_query
from architools.connectors.wkt import wkt_to_occ

class Scene():
  """In-memory document containing visible objects."""

  def __init__(self):
    self.uuid = str(uuid())
    self.layers = {}
    self.coordinate_offset = [0.0, 0.0] # optional x, y offset relative to a geographic coordinate system

  def add_layer_from_query(self, layer_name, color, parent_name, template, params):
    """Queries database, adds results to a new layer in the scene."""
    result = run_query(template, params)
    value = result

    l = self.add_layer(layer_name, color, parent_name)

    # add objects to layer
    for o in result:
      layer_o = SceneObject()
      if hasattr(o, 'name'): layer_o.name = o.name
      layer_o.geom = wkt_to_occ(o.wkt)
      for k,v in o._asdict().items():
        layer_o.attributes[k] = v

      l.objects.append(layer_o)

    return l

  def add_layer(self, layer_name, color, parent_name):
    """Adds a blank layer"""

    if not self.layers.get(layer_name):
        l = SceneLayer(layer_name)
        l.color = color
        l.parent_name = parent_name
        self.layers[layer_name] = l
        return l
    else: print('LAYER ALREADY EXISTS!')

# def load_model(self):
#   """Populate the scene's object table from the database,
#   using a defined area of interest (AOI) and standard layers.
#   """

#   params = {
#     'center_x': aoi_default.representative_point().x,
#     'center_y': aoi_default.representative_point().y,
#     'bounds': aoi_default_wkt
#   }

#   # iterate over defined layers, fetch named geometries for each
#   # convert to OCC, add to scene objects table
#   for l in standard_layers:
#     result = run_query(l.query, params)
#     print(len(result))
#     for record in result:
#       converted = wkt_to_occ(record.geom, topo=True)
#       if converted == None: break
#       print(record.name)
#       converted.name = record.name
#       converted.layer = l.name
#       self.objects.append(converted)

class SceneLayer():

  def __init__(self, name):
    self.uuid = str(uuid())
    self.name = None
    self.color = None
    self.parent_name = None
    self.objects = []


class SceneObject():

  def __init__(self):
    self.uuid = str(uuid())
    self.name = None
    self.geom = None
    self.attributes = {}


def add_wktgeom_to_scene(wkt, layer, scene, attributes={}):
  obj = SceneObject()
  obj.geom = wkt_to_occ(wkt, topo=True)
  obj.attributes = attributes
  scene.layers[layer].objects.append(obj)
