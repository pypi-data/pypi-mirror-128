from OCC.Core.GProp import GProp_PEquation
from OCC.Core.gp import gp_Pnt

from architools.geometry.conversion import pts_to_array


class Point():

  def say_hello():
    print('hello')


def test_colinear(pts, tol=0.01, z=False, force_z=False):
  """Tests whether OCC pts in list are colinear."""

  if z: pts = [gp_Pnt(*p.Coord()) for p in pts]

  # force z option
  if force_z: pts = [gp_Pnt(*p.Coord(), 0) for p in pts]

  arr = pts_to_array(pts)
  pe = GProp_PEquation(arr, tol)
  return pe.IsLinear()
