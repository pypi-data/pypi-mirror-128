import sys
from collections import namedtuple

from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse,
    BRepAlgoAPI_Common,
    BRepAlgoAPI_Cut,
)
from OCC.Core.BOPAlgo import BOPAlgo_Builder, BOPAlgo_MakerVolume
from OCC.Core.BRepBndLib import brepbndlib_Add, brepbndlib_AddOptimal, brepbndlib_AddOBB
from OCC.Core.BRepBuilderAPI import (
  BRepBuilderAPI_MakePolygon,
  BRepBuilderAPI_MakeShell,
  BRepBuilderAPI_MakeSolid,
  BRepBuilderAPI_Sewing,
)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Vec, gp_Dir
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_VERTEX
from OCC.Core.BRep import BRep_Tool

from architools.geometry.boolean import union, diff
from architools.geometry.conversion import curve_to_wire, wire_to_curve, pts_to_polygon


def extrude_shape(shape, guide, infinite=False):
  """Extrudes an input shape to create a BRep.

  Guide can be either a vector (gp_Vec) for a finite result,
  or direction (gp_Dir) for semi-infinite or infinite results.
  """

  if type(guide) == gp_Vec:
    result = BRepPrimAPI_MakePrism(shape, guide).Shape()
  else:
    result = BRepPrimAPI_MakePrism(shape, guide, infinite).Shape()

  return result


def loft_wires(wires, closed=True):
  """From a list of OCC Wires, build up a solid by lofting"""

  loft = BRepOffsetAPI_ThruSections(True, True)

  caps = [[], []]

  for w in wires:
    c = wire_to_curve(w)
    caps[0].append(c.Value(0))
    caps[1].append(c.Value(1))

  for i, c in enumerate(caps):
    caps[i].append(caps[i][0])
    polygon = pts_to_polygon(c)
    loft.AddWire(polygon)

  loft.CheckCompatibility(False)

  result = None

  try:
    result = loft.Shape()
  except RuntimeError:
    return None
  # if loft.IsDone(): return loft.Shape()
  # else: return None
  return result


def bbox(shape, tol=1e-6):
  """Calculates BRep bounding box, returns typle of xyz min, xyz max."""

  bbox = Bnd_Box()
  # bbox.SetGap(tol)

  for p in brep_vertices(shape, as_points=True):
    #brepbndlib_Add(p, bbox)
    bbox.Add(p)

  BBoxResult = namedtuple('BBoxResult', 'xmin ymin zmin xmax ymax zmax')
  result = BBoxResult(*bbox.Get())

  return result


def brep_vertices(shape, as_points=True):
  explorer = TopExp_Explorer(shape, TopAbs_VERTEX)

  verts = []

  while explorer.More() == True:
    verts.append(explorer.Current())
    explorer.Next()

  # convert to points
  if as_points: verts = [BRep_Tool.Pnt(v) for v in verts]

  return verts


def brep_from_faces(faces, solid=False):
  """Connect multiple Faces using Sewing"""
  result = faces.pop(0)
  for f in faces:
   result = BRepAlgoAPI_Fuse(result, f).Shape()

  return result
