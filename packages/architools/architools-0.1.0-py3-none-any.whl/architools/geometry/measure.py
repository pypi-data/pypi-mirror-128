from math import pi
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepGProp import (
  brepgprop_SurfaceProperties,
  brepgprop_LinearProperties,
)
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.gp import gp_Dir, gp_Vec
from OCC.Core.GProp import GProp_GProps

horiz_tol = pi * 0.0834 # based on 1:12 max ADA slope
vert_tol = horiz_tol # todo: use different value?


def area(shape):
  props = GProp_GProps()
  brepgprop_SurfaceProperties(shape, props)
  return props.Mass() # area is given as Mass for a surface


def perimeter(shape):
  props = GProp_GProps()
  brepgprop_LinearProperties(shape, props)
  return props.Mass() # perimeter


def normal(shape):
  s = BRep_Tool().Surface(shape)
  props = GeomLProp_SLProps(s, 0.5, 0.5, 1, 1e-6)
  n = props.Normal()
  return n # normal
