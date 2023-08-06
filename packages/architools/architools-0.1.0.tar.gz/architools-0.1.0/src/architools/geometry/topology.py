# adapted from tpaviot/pythonocc-utils
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import (topods, TopoDS_Wire, TopoDS_Vertex, TopoDS_Edge,
                        TopoDS_Face, TopoDS_Shell, TopoDS_Solid,
                        TopoDS_Compound, TopoDS_CompSolid, topods_Edge,
                        topods_Vertex, TopoDS_Iterator)
from OCC.Core.TopAbs import (TopAbs_VERTEX, TopAbs_EDGE, TopAbs_FACE, TopAbs_WIRE,
                        TopAbs_SHELL, TopAbs_SOLID, TopAbs_COMPOUND,
                        TopAbs_COMPSOLID)
from OCC.Core.TopTools import TopTools_IndexedDataMapOfShapeListOfShape, TopTools_ListIteratorOfListOfShape
from OCC.Core.TopExp import topexp_MapShapesAndAncestors

topoFactory = {
  TopAbs_VERTEX: topods.Vertex,
  TopAbs_EDGE: topods.Edge,
  TopAbs_FACE: topods.Face,
  TopAbs_WIRE: topods.Wire,
  TopAbs_SHELL: topods.Shell,
  TopAbs_SOLID: topods.Solid,
  TopAbs_COMPOUND: topods.Compound,
  TopAbs_COMPSOLID: topods.CompSolid
}

topoTypes = {
  'edge': TopAbs_EDGE,
  'face': TopAbs_FACE,
  'vertex': TopAbs_VERTEX,
}

def get_subshapes(topo, type):
  '''Where topoType is TopAbs_FACE, EDGE etc'''
  topoType = topoTypes[type]
  explorer = TopExp_Explorer(topo, topoType)
  result = []

  while explorer.More():
    result.append(explorer.Current())
    explorer.Next()
      
  return result


def get_edges(topo):
  return get_subshapes(topo, 'edge')


def get_connected(topo, topoTypeA, topoTypeB, topologicalEntity):
  '''
  using the same method
  @param topoTypeA:
  @param topoTypeB:
  @param topologicalEntity:
  '''
  ignore_orientation = False
  topo_set = set()
  _map = TopTools_IndexedDataMapOfShapeListOfShape()
  topexp_MapShapesAndAncestors(topo, topoTypeA, topoTypeB, _map)
  results = _map.FindFromKey(topologicalEntity)
  if results.Size() == 0:
      yield None

  topology_iterator = TopTools_ListIteratorOfListOfShape(results)
  while topology_iterator.More():

      topo_entity = topoFactory[topoTypeB](topology_iterator.Value())

      # return the entity if not in set
      # to assure we're not returning entities several times
      if not topo_entity in topo_set:
          if ignore_orientation:
              unique = True
              for i in topo_set:
                  if i.IsSame(topo_entity):
                      unique = False
                      break
              if unique:
                  yield topo_entity
          else:
              yield topo_entity

      topo_set.add(topo_entity)
      topology_iterator.Next() 


def count_connected(topo, typeA, typeB, topologicalEntity):
  '''returns the number of connected entities
  If you want to know how many edges a faces has:
  _number_shapes_ancestors(self, TopAbs_EDGE, TopAbs_FACE, edg)
  will return the number of edges a faces has   
  @param topoTypeA:
  @param topoTypeB:
  @param topologicalEntity:
  '''
  topoTypeA = topoTypes[typeA]
  topoTypeB = topoTypes[typeB]
  topo_set = set()
  _map = TopTools_IndexedDataMapOfShapeListOfShape()
  topexp_MapShapesAndAncestors(topo, topoTypeA, topoTypeB, _map)
  results = _map.FindFromKey(topologicalEntity)
  if results.Size() == 0:
      return None
  topology_iterator = TopTools_ListIteratorOfListOfShape(results)
  while topology_iterator.More():
      topo_set.add(topology_iterator.Value())
      topology_iterator.Next()
  return len(topo_set)

