from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_CompCurve
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.BOPAlgo import BOPAlgo_BuilderSolid, BOPAlgo_MakeConnected
from OCC.Core.BRepBuilderAPI import (
  BRepBuilderAPI_MakePolygon, 
  BRepBuilderAPI_MakeFace,
  BRepBuilderAPI_MakeEdge,
  BRepBuilderAPI_MakeWire,
  BRepBuilderAPI_MakeShell, 
  BRepBuilderAPI_MakeSolid, 
  BRepBuilderAPI_Sewing
)
from OCC.Core.Geom2d import Geom2d_OffsetCurve, Geom2d_BSplineCurve, Geom2d_Curve
from OCC.Core.Geom2dAPI import Geom2dAPI_PointsToBSpline
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline, geomapi_To3d
from OCC.Core.gp import (
  gp_Pnt,
  gp_Pnt2d,
  gp_Vec,
  gp_Dir,
  gp_Ax2,
  gp_Pln
)
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.TColgp import TColgp_Array1OfPnt2d

# import OCC.Core.TColgp as tcol
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_SHELL, TopAbs_VERTEX
# from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shell, TopoDS_Solid

from architools.geometry.edge import get_endpoints
from architools.geometry.reference import world_xy


def pts_to_array(pts, z=True):
  """Converts list of OCC points to OCC Array"""

  if z:
    occ_array = TColgp_Array1OfPnt(1, len(pts))
  else:
    occ_array = TColgp_Array1OfPnt2d(1, len(pts))

  for i, occ_pt in enumerate(pts):
    occ_array.SetValue(i + 1, occ_pt)

  return occ_array


def pts_to_curve(pts, z=True):
  """Converts list of OCC points to OCC Curve"""
  occ_array = pts_to_array(pts, z)

  if z:
    occ_curve = GeomAPI_PointsToBSpline(occ_array, 1, 1).Curve()
  else:
    occ_curve = Geom2dAPI_PointsToBSpline(occ_array, 1, 1).Curve()

  return occ_curve


def pts_to_polygon(pts):
  occ_polygon = BRepBuilderAPI_MakePolygon()
  
  for occ_pt in pts:
    occ_polygon.Add(occ_pt)

  return occ_polygon.Shape()


def curve_to_face(curve):
  """Converts OCC Curve to OCC Face"""
  wire = curve_to_wire(curve)
  face = BRepBuilderAPI_MakeFace(wire, False)
  
  if not face.IsDone(): return None
  else: return face.Shape()


def curve_to_wire(curve):
  """Converts OCC Curve to OCC Wire"""

  if type(curve) in [Geom2d_Curve, Geom2d_BSplineCurve]:
    curve = geomapi_To3d(curve, world_xy)

  edge = BRepBuilderAPI_MakeEdge(curve).Shape()
  wire = BRepBuilderAPI_MakeWire(edge).Shape()
  return wire


def wire_from_unsorted_edges(edges):
  """Given a dictionary of edges, keyed by id and where the value is a dict
  with at least a geom field containing an OCC Edge,
  build an OCC Wire and keep track of the order of ids as they are added.
  """
  source_list = [ {'id': i[0], 'geom': i[1]['geom'] } for i in edges.items() ]
  #build_list = TopTools_ListOfShape()
  builder = BRepBuilderAPI_MakeWire()
  indices = []

  edge_0 = source_list.pop()
  builder.Add(edge_0['geom'])
  indices.append(edge_0['id'])

  # wire start and end points
  (w_start, w_end) = get_endpoints(edge_0['geom'])

  while len(source_list) > 0:
    e = source_list.pop()
    (e_start, e_end) = get_endpoints(e['geom'])

    if w_end in [e_start, e_end]:

      if w_end == e_end:
        w_end = e_start # start point will become end when reversed
        e['geom'].Reverse()
      else:
        w_end = e_end

      builder.Add(e['geom'])
      indices.append(e['id'])

    else:
      source_list.insert(0, e)

  # builder = BRepBuilderAPI_MakeWire()
  # builder.Add(build_list)
  builder.Build()
  result = builder.Shape()

  return (result, indices)


def wire_to_curve(wire):
  explorer = TopExp_Explorer(wire, TopAbs_EDGE)
  (curve, min, max) = BRep_Tool.Curve(explorer.Current())
  return curve


def wire_to_face(wire):
  face_builder = BRepBuilderAPI_MakeFace(wire)
  face = face_builder.Shape()
  # crv = wire_to_curve(wire)
  # face = curve_to_face(crv)
  return face
