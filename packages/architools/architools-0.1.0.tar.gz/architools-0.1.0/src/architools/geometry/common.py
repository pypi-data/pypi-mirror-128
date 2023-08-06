import re
import math
# from OCC.Core import GeomAPI
from OCC.Core.BOPAlgo import BOPAlgo_MakeConnected, BOPAlgo_BuilderSolid
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeShell, BRepBuilderAPI_MakeSolid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gce import gce_MakePln
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline, geomapi_To2d
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Ax2, gp_Pln, gp_Trsf
from OCC.Core.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.TColgp import TColgp_HArray1OfPnt2d, TColgp_Array1OfPnt2d
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Display.WebGl.jupyter_renderer import JupyterRenderer
import OCC.Core.TColgp as tcol
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_SHELL, TopAbs_VERTEX, TopAbs_SOLID
from OCC.Core.BRep import BRep_Tool
from architools.geometry.reference import world_xy


# takes flat list of occ faces
# fuses together
# and returns result
def fuse_faces(faces):
    count = len(faces)
    n = 1
    result = BRepBuilderAPI_MakeFace()
    
    for face in faces:
        if n > count : break
    
        try:
          result = BRepAlgoAPI_Fuse(result.Shape(), face.Shape())
        except RuntimeError:
          result = face
            
        n += 1
    
    result = upgrade_brep(result.Shape())
    
    return result

# function to return true or false if azimuth a
# is within 45 degrees of all values in a list of azimuth b
def within_45_all(az_a, list_of_az_b):
  tests = []

  for az_b in list_of_az_b:
    # test uses modulo to ignore direction of azimuth
    az_a_ignoredir = az_a % math.pi
    az_b_ignoredir = az_b % math.pi
    test = (az_b_ignoredir - math.pi/4) <= az_a_ignoredir <= (az_b_ignoredir + math.pi/4)
    tests.append(test)
       
  return all(tests)


def moved(shape, vector):
  """Given a OCC shape and a 3d vector expressed as a tuple,
  return a copy of the shape translated by the vector.
  """
  vec = gp_Vec(*vector)
  transform = gp_Trsf()
  transform.SetTranslation(vec)
  mover = TopLoc_Location(transform)
  result = shape.Moved(mover)
  return result


def get_vertices(shape, topo=True):
  """Get Vertices (or with topo=False, Points) inside any OCC Shape"""
  vertices = extract_elements(shape, TopAbs_VERTEX)

  if not topo:
    vertices = [BRep_Tool.Pnt(e) for e in vertices]

  return vertices


def get_edges(shape, topo=True, z=True):
  """Get Edges (or with topo=False, Curves) inside any OCC Shape"""
  edges = extract_elements(shape, TopAbs_EDGE)

  if not topo:
    if not z:
      curves_3d = [BRep_Tool.Curve(e) for e in edges]
      # curves_2d = [geomapi_To2d(c, world_xy) for c in curves_3d]
      # edges = curves_2d
    else:
      edges = [BRep_Tool.Curve(e) for e in edges]

  return edges


def get_faces(shape, topo=True, z=True):
  """Get Faces (or with topo=False, Surfaces) inside OCC Shape"""
  faces = extract_elements(shape, TopAbs_FACE)

  # if not topo:
  # if not z:
  # print('NOT IMPLEMENTED')
  # curves_3d = [BRep_Tool.Curve(e) for e in edges]
  # curves_2d = [geomapi_To2d(c, world_xy) for c in curves_3d]
  # edges = curves_2d
  # else:
  #   faces = [BRep_Tool.Curve(e) for e in edges]

  return faces


def get_solids(shape, topo=True, z=True):
  """Get Faces (or with topo=False, Surfaces) inside OCC Shape"""
  result = extract_elements(shape, TopAbs_SOLID)
  return result


def extract_elements(shape, el_type):
  """INTERNAL ONLY, used to grab vertices, edges out of wire. 
  el_type should be OCC TopAbs"""
  explorer = TopExp_Explorer(shape, el_type)
  els = []

  while explorer.More() == True:
    els.append(explorer.Current())
    explorer.Next()

  return els
