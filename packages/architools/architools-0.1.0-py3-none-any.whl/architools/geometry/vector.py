from math import pi

from architools.geometry.reference import (
  unit_z, 
  north, 
  south, 
  east, 
  west,
  pos_z,
)

horiz_tol = pi * 0.0834 # based on 1:12 max ADA slope for floors
vert_tol = horiz_tol # todo: use different value?


def is_up(v):
  """Check if vector is pointing up, within tolerance."""
  compare_angle = v.Angle(pos_z)
  test = compare_angle < (0 + horiz_tol)
  return test

def is_down(v):
  """Check if vector is pointing down, within tolerance."""
  compare_angle = v.Angle(pos_z)
  test = compare_angle > (pi - horiz_tol)
  return test

def is_vert(v):
  """Check if vector is pointing up or down, within tolerance."""
  test = is_up(v) or is_down(v)
  return test

def is_horiz(v):
  """Check if vector is pointing horizontally, within tolerance."""
  compare_angle = v.Angle(pos_z)
  test = (pi/2 - vert_tol) < compare_angle < (pi/2 + vert_tol)
  return test
