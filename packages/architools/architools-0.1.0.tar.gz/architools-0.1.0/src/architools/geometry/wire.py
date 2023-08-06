from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import (
  BRepBuilderAPI_MakeFace,
  BRepBuilderAPI_MakePolygon,
  BRepBuilderAPI_MakeWire,
)
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.gp import gp_Pnt
from OCC.Core.TopAbs import TopAbs_VERTEX

from architools.connectors.wkt import coords_to_curve
from architools.geometry.edge import get_endpoints
from architools.geometry.measure import area
from architools.geometry.common import extract_elements

def is_ccw(wire):
  """Check if the wire is counterclockwise. If area
  is positive, wire is CCW by OCC conventions.
  """
  
  face = BRepBuilderAPI_MakeFace(wire).Face()
  a = area(face)
  return a > 0


def fit_to_bounds(edge, bounds):
  """Extend/trim ends of edge to boundary wire."""

  return None


def get_vertices(wire, topo=True):
  """Get Vertices (or with topo=False, Points) inside OCC Wire"""
  result = []

  explorer = BRepTools_WireExplorer()
  explorer.Init(wire)
  
  while explorer.More() == True:
    result.append(explorer.CurrentVertex())
    explorer.Next()

  # when wire is a single edge, return both vertices
  if len(result) == 1:
    all_verts = extract_elements(wire, TopAbs_VERTEX)
    result = all_verts
    # here could preserve order by checking vs
    # original result, known to be first vertex

  # when wire is closed, append first vertex to end of list
  if wire.Closed(): result.append(result[0])

  if not topo:
    result = [BRep_Tool.Pnt(e) for e in result]

  return result


def to_curve_from_vertices(wire):
  # make sure this is the right get_vertices function?
  coords = [p.Coord()  for p in get_vertices(wire, topo=False)]
  curve = coords_to_curve(coords)
  return curve


def wire_from_edges(edges):
  builder = BRepBuilderAPI_MakeWire()
  for e in edges:
    builder.Add(e)
  return builder.Wire()


# def get_edges(shape, topo=True, z=True):
#   """Get Edges (or with topo=False, Curves) inside any OCC Shape"""
#   edges = extract_elements(shape, TopAbs_EDGE)

#   if not topo:
#     if not z:
#       curves_3d = [BRep_Tool.Curve(e) for e in edges]
#       # curves_2d = [geomapi_To2d(c, world_xy) for c in curves_3d]
#       # edges = curves_2d
#     else:
#       edges = [BRep_Tool.Curve(e) for e in edges]

#   return edges

def wire_from_coordinates(coords, closed=False):
  """Builds a polygonal wire from coordinate tuples"""

  builder = BRepBuilderAPI_MakePolygon()

  for c in coords:
    p = gp_Pnt(*c)
    builder.Add(p)

  if closed == True: builder.Add(gp_Pnt(*coords[0]))

  return builder.Wire()
