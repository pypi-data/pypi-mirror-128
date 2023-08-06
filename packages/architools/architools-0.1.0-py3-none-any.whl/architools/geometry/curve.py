import math

from OCC.Core.GCPnts import GCPnts_AbscissaPoint
from OCC.Core.gce import gce_MakeLin2d
from OCC.Core.Geom import Geom_OffsetCurve, Geom_BezierCurve, Geom_Line
from OCC.Core.Geom2d import (
  Geom2d_BSplineCurve,
  Geom2d_Line,
  Geom2d_OffsetCurve,
)
from OCC.Core.Geom2dAPI import (
  Geom2dAPI_ProjectPointOnCurve, 
  Geom2dAPI_ExtremaCurveCurve,
  Geom2dAPI_InterCurveCurve,
)
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.GeomAPI import (
  GeomAPI_ProjectPointOnCurve,
  geomapi_To2d,
  geomapi_To3d,
)
from OCC.Core.gp import (
  gp_Pnt2d,
  gp_Vec2d,
  gp_Dir2d,
  gp_Pnt,
  gp_Vec,
  gp_Dir,
)

from architools.connectors.wkt import coords_to_curve
from architools.geometry.conversion import pts_to_curve
from architools.geometry.point import test_colinear
from architools.geometry.reference import pos_z, world_xy


def pt_on_curve(pt, crv, tol, z=False):
  """Test if point is coincident (within tolerance) with curve."""

  pt_2d = gp_Pnt2d(pt.X(), pt.Y())
  crv_2d = geomapi_To2d(crv, world_xy)

  projector = Geom2dAPI_ProjectPointOnCurve(pt_2d, crv_2d)
  nearest_2d = projector.NearestPoint()

  dist = pt_2d.Distance(nearest_2d)
  test = dist <= tol

  return test


# def trim_curve_to_bounds(curve, bounds):
#   """Where curve and bounds are coplanar 3D OCC Curves.
#   Bounds is expected to be closed and at least part of curve
#   needs to be within bounds. Attempts to trim/extend endpoints
#   of curve to meet bounds.
#   """

#   start = curve.Value(0)
#   end = curve.Value(1)
#   start_ext = extended_point_at_param(curve, bounds, 0)
#   end_ext = extended_point_at_param(curve, bounds, 1)

#   print([p.Coord() for p in [start, start_ext, end, end_ext]])
#   # check that the start and end extension points aren't the same
# dist = start_ext.Distance(end_ext)
# thresh = 1.0
#   ext_are_diff =  > thresh

#   if start.Distance(start_ext) > 0.0:
#     start = start_ext

#   if end.Distance(end_ext) > 0.0 and ext_are_diff:
#     end = end_ext

#   result = pts_to_curve([start, end], z=True)

#   return result


def trim_curve_to_bounds(curve, bounds):
  """Where curve and bounds are coplanar 3D OCC Curves.
  Bounds is expected to be closed and at least part of curve
  needs to be within bounds. Attempts to trim/extend endpoints
  of curve to meet bounds and returns the trimmed curve.
  """
  curve_2d = geomapi_To2d(curve, world_xy)
  bounds_2d = geomapi_To2d(bounds, world_xy)

  c = curve_2d
  c_start = c.Value(0)
  c_end = c.Value(1)

  ln = gce_MakeLin2d(c_start, c_end).Value()
  ln_curve = Geom2d_Line(ln)

  tol = 0.0001
  intersector = Geom2dAPI_InterCurveCurve(ln_curve, bounds_2d, tol)

  npts = intersector.NbPoints()

  if npts < 1:
    return curve # return the original curve if no intersections
  else:
    pts = []

    for i in range(1, npts + 1):
      pt = intersector.Point(i)
      pts.append(pt)

    # to do, sort from center of curve line?

    coords = [p.Coord() for p in pts]
    result_2d = coords_to_curve([coords[0], coords[-1]], z=False)
    result = geomapi_To3d(result_2d, world_xy)

    # to do, optionally return as topo?
    # result_asedge = BRepBuilderAPI_MakeEdge(result_3d).Shape()

    return result


def length(curve, u1=0.0, u2=1.0):
  """Returns length of OCC curve between parameters u1 and u2."""

  ab = GCPnts_AbscissaPoint()

  return ab.Length(GeomAdaptor_Curve(curve), u1, u2)


# def extrema_nearest_pt(c1, c2, param):
#   """Used internally by curve_fit_to_bounds.

#   Tries to find and return point on c2 nearest to the provided
#   param on c1. If unsuccessful, returns point at the param on c1.
#   """

#   result = c1.Value(param)

#   test_from = -1 if param == 0 else 1
#   test_to = 0 if param == 0 else 2
#   ex = Geom2dAPI_ExtremaCurveCurve(c1, c2, test_from, test_to, 0, 1)
#   ex_count = ex.NbExtrema()

#   if ex_count == 0: return result

#   c1_pt = gp_Pnt2d()
#   c2_pt = gp_Pnt2d()
#   ex1_pts = ex.NearestPoints(c1_pt, c2_pt)

#   return c2_pt


# def extended_point_at_param(c1, c2, param):
#   """Tries to find nearest point on c2 to provided param on c1"""
#   p = c1.Value(param)
#   projector = GeomAPI_ProjectPointOnCurve(p, c2)
#   result = projector.NearestPoint()
#   return result


def match_curve_direction(c1, c2, tol=1.0, z=True):
  """Make c1 match direction of best coincident segment on c2.
  Expects OCC Curves as input. Result is to modify c1.
  """

  c1_mid = gp_Pnt() if z else gp_Pnt2d()
  c1_tan = gp_Vec() if z else gp_Vec2d()

  # get c1 direction at midpoint
  c1.D1(0.5, c1_mid, c1_tan)
  c1_dir = gp_Dir(c1_tan) if z else gp_Dir2d(c1_tan)
  c1_start = c1.Value(0)
  c1_end = c1.Value(1)

  # loop over local segments of c2,
  # check if colinear with c1,
  # and if so, use to ensure correct orientation of c1

  c2_knots = c2.Knots()
  c2_mid = gp_Pnt() if z else gp_Pnt2d()
  c2_tan = gp_Vec() if z else gp_Vec2d()
  c2_dir = gp_Dir() if z else gp_Dir2d()

  for i in range(1, len(c2_knots)):

    c2.LocalD1(0.5, i, i+1, c2_mid, c2_tan)

    col = test_colinear([c1_start, c1_end, c2_mid], z=z) # force z
    if not col: continue

    c2_dir = gp_Dir(c2_tan) if z else gp_Dir2d(c2_tan)
    if c1_dir.IsEqual(c2_dir, math.pi/24):
      return c1
    elif c1_dir.IsOpposite(c2_dir, math.pi/24):
      c1.Reverse()
      return c1

  # if no colinear segments are found,
  # assume c2 is a single noncolinear line segment
  # use its direction regardless of location

  c2.D1(0.5, c2_mid, c2_tan)
  c2_dir = gp_Dir(c2_tan) if z else gp_Dir2d(c2_tan)
  if c1_dir.IsEqual(c2_dir, math.pi/24):
    return c1
  elif c1_dir.IsOpposite(c2_dir, math.pi/24):
    c1.Reverse()
    return c1

  # if all else fails,
  # return the original curve
  return c1


def setback(curve, distance):
  """Setback planar 3d curves in XY plane, returns curve."""
  # pnt = gp_Pnt()
  # vec = gp_Vec()
  # edge_ascurve.D1(0.5, pnt, vec)
  offset_dir = pos_z
  result = Geom_OffsetCurve(curve, distance, offset_dir)

  return result


unit_x_as_curve = coords_to_curve([(0, 0, 0), (1, 0, 0)])


# def offset(curve, distance):
#   """offset 2d curve by distance, negative is in, positive out"""
#   return Geom2d_OffsetCurve(curve, distance)

# def lift(curve, distance):
#   """offset curve in positive z direction by distance"""
#   return Geom_OffsetCurve(curve, distance, pos_z)