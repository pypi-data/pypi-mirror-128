from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gce import gce_MakeLin
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve

from architools.geometry.common import get_edges, get_vertices

def get_endpoints(edge):
  """Returns start, end points of OCC edge as coordinate tuples.
  """
  pt_0 = get_vertices(edge, False)[0].Coord()
  pt_1 = get_vertices(edge, False)[1].Coord()
  return (pt_0, pt_1)


def edge_to_wire(edge):
  result = BRepBuilderAPI_MakeWire(edge)
  return result.Shape()


def to_line_from_vertices(wire):
  pts = get_vertices(wire, topo=False)
  line = gce_MakeLin(pts[0], pts[-1])
  return line.Value()


def point_on_edge(edge, param):
  adaptor = BRepAdaptor_Curve(edge)
  return adaptor.Value(param)


def tangent_on_edge(edge, param, as_dir=False, use_topo_orientation=False):
  """Returns first derivative of edge curve at a parameter as gp_Vec or gp_Dir.

  Required edge, param, optional as_dir (bool), use_topo_orientation (bool).
  """
  adaptor = BRepAdaptor_Curve(edge)
  result_pnt = gp_Pnt()
  result_vec = gp_Vec()
  adaptor.D1(param, result_pnt, result_vec)

  if use_topo_orientation and edge.Orientation() == 1:
    result_vec.Reverse()

  if as_dir: return gp_Dir(result_vec)
  else: return result_vec
