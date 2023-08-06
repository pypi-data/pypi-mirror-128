"""This module converts well-known-text (WKT) geometry representations 
to/from OpenCASCADE geometry and topology classes used internally.
"""

import re

import shapely

from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.BOPAlgo import BOPAlgo_BuilderSolid, BOPAlgo_MakeConnected
from OCC.Core.BRepBuilderAPI import (
  BRepBuilderAPI_MakePolygon,
  BRepBuilderAPI_MakeFace,
  BRepBuilderAPI_MakeEdge,
  BRepBuilderAPI_MakeShell,
  BRepBuilderAPI_MakeSolid,
  BRepBuilderAPI_Sewing
)
from OCC.Core.Geom2dAPI import Geom2dAPI_PointsToBSpline
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
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
from OCC.Core.TopTools import TopTools_ListOfShape
# from OCC.Display.WebGl.jupyter_renderer import JupyterRenderer
# import OCC.Core.TColgp as tcol
# from OCC.Core.TopExp import TopExp_Explorer
# from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_SHELL, TopAbs_VERTEX
# from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shell, TopoDS_Solid

from architools.geometry.boolean import union as brep_union
# from geometry.healing import upgrade
# from geometry.reference import world_xy
# from geometry.conversion import coords_to_polygon


# def compound_to_list(shape, type):
#   explorer = TopExp_Explorer(shape, type)
#   result = []
#   while explorer.More():
#     result.append(explorer.Current())
#     explorer.Next()
#   return result


def coords_to_array(coords, z=True):
  """Converts list of point tuples to OCC Array of Point."""

  if z: occ_array = TColgp_Array1OfPnt(1, len(coords))
  else: occ_array = TColgp_Array1OfPnt2d(1, len(coords))

  for i, p in enumerate(coords):
    if z: occ_pt = gp_Pnt(*p)
    else: occ_pt = gp_Pnt2d(*p)
    occ_array.SetValue(i + 1, occ_pt)

  return occ_array


def coords_to_curve(coords, z=True):
  """Converts list of point tuples to OCC Curve"""
  occ_array = coords_to_array(coords, z)

  if z: occ_curve = GeomAPI_PointsToBSpline(occ_array, 1, 1)
  else: occ_curve = Geom2dAPI_PointsToBSpline(occ_array, 1, 1)

  return occ_curve.Curve()


def coords_to_polygon(coords, z=True):
  """Converts list of tuples representing points to OCC Polygon"""
  occ_polygon = BRepBuilderAPI_MakePolygon()
  closed = len(coords) > 0 and coords[0] == coords[-1]

  for p in coords:
    occ_pt = gp_Pnt(*p) if z else gp_Pnt(*p, 0)
    occ_polygon.Add(occ_pt)
  
  if closed: occ_polygon.Close()
  return occ_polygon.Shape()


def coord_string_to_tuples(wkt):
  """Converts one or more well-known text points 
  separated by commas to list of X,Y,Z tuples."""
  coord_re = r'([\-\.\d\s]+)[\,\)]*'
  coord_search = re.findall(coord_re, wkt)

  tuples = []
  for match in coord_search:
    coord = match.strip().strip(',')
    coord = coord.split(' ')
    coord = [float(c) for c in coord]
    coord = tuple(coord)
    tuples.append(coord)

  return tuples


def coords_to_edge(coords, z=True):
  pts = []
  
  for p in coords:
    pt = gp_Pnt(*p) if z else gp_Pnt(*p, 0)
    pts.append(pt)
  
  edge_builder = BRepBuilderAPI_MakeEdge(*pts)
  edge = edge_builder.Edge()
  return edge

# def edges_to_wire(edges):
#   wire_alg = BRepBuilderAPI_MakeWire()
#   for e in edges:
#     wire_alg.Add(e)
#   return wire_alg.Wire()


def linestring_to_occ(wkt, z=False, topo=False):
  shape = shapely.wkt.loads(wkt)
  coords = shape_to_coords(shape, z)

  if topo:
    edge = coords_to_edge(coords, z)
    return edge
  else:
    curve = coords_to_curve(coords, z)
    return curve
  # print('NOT IMPLEMENTED: LINESTRING')


def multipolygon_to_occ(wkt, z=False, topo=False):
  wires = []

  multi_re = r'MULTIPOLYGON[ZM\s]*\(([\(\)\d\.\,\-\s]*)\)'
  polygon_re = r'\((\([\d\s\,\.\-]+?\))\)'
  ring_re = r'\(([\d\.\,\s\-]*)\)'

  multi = re.search(multi_re, wkt).group(1)
  polygons = re.findall(polygon_re, multi)

  for p in polygons:
    rings = re.findall(ring_re, p)
    for r in rings:
      coords = coord_string_to_tuples(r)
      occ_polygon = coords_to_polygon(coords, z=z)
      wires.append(occ_polygon)

  if len(wires) == 0: return None
  result = brep_union(wires)
  return result


# takes a shapely multipolygon as input
# (ignores holes)
# returns list of occ faces
#     faces = []
#     #wires = []

#     shapely_polygons = shape.geoms
    
#     for p in shapely_polygons:
#         occ_polygon = coords_to_polygon(p.exterior.coords)
#         wire = occ_polygon.Wire()
#         face = BRepBuilderAPI_MakeFace(wire, True)
#         faces.append(face)
#         # to get wire it would be 
#         # occ_polygon.Wire()

#     return faces


def point_to_occ(wkt, z=False, topo=False):
  point_re = r'\(([\-\.\d]+) ([\-\.\d]+)[\)\,\s]([\.\d]*)[\)\,]*'
  groups = re.search(point_re, wkt).groups()
  result = [float(string) for string in groups if len(string)]
  if z: occ_pt = gp_Pnt(*result)
  else: occ_pt = gp_Pnt2d(*result)
  return occ_pt


def polygon_to_occ(wkt, z=False, topo=False):
  """Converts a WKT polygon to OCC.

  If a number is passed to z instead of True/False, can be used
  to create a planar polygon at a given Z elevation.
  """
  polygon_re = r'\(\(([\d\s\-\.\,\(\)]*)\)\)'
  polygon_search = re.search(polygon_re, wkt)
  coord_string = polygon_search.group(1)

  coords = coord_string_to_tuples(coord_string)
  if type(z) in [int, float]:
    coords = [(c[0], c[1], z) for c in coords]
    # result = coords_to_curve(coords_z_translated, True)

  if topo: result = coords_to_polygon(coords, z)
  else: result = coords_to_curve(coords, z)
  return result


# not in use
def polyhedralsurfacez_list_to_brep(wkt_list):
  breps = [polyhedralsurfacez_to_occ(wkt) for wkt in wkt_list]
  result = brep_union(breps)
  return result


def polyhedralsurfacez_to_occ(wkt, z=True, topo=True):
    occ_faces = TopTools_ListOfShape()

    outer_regex = r'(POLYHEDRALSURFACE Z \()([\(\)\d\.\,\-\s\(]*\))(\))'
    inner_regex = r'\(([\d\.\,\s\-]*)\)'

    body = re.search(outer_regex, wkt).group(2)
    faces = re.findall(inner_regex, body)

    for f in faces:
        face_coords = []
        # var coordinatepairlist = p.Replace(")", "").Replace("(", "").Split(',');
        f_clean = f.replace(')', '').replace(')', '')
        f_split = f_clean.split(',')
        for pt in f_split:
            coords = [float(d) for d in pt.split(' ')]
            face_coords.append(tuple(coords))

        face_polygon = coords_to_polygon(face_coords, z=True)
        face = BRepBuilderAPI_MakeFace(face_polygon, True)
        if face.IsDone():
          occ_faces.Append(face.Shape())

    # weld faces into solid
    make_solid = BOPAlgo_BuilderSolid()
    make_solid.SetShapes(occ_faces)
    make_solid.Perform()

    # weld faces together
#     make_connected = BOPAlgo_MakeConnected()
#     make_connected.SetArguments(occ_faces)
#     make_connected.Perform()

#     result = upgrade_brep(make_connected.Shape())
#     return result

    return make_solid.Areas().First()


# alternate version, to phase out?
# def polyhedralsurfacez_to_brep(wkt):
#   outer_regex = r'(POLYHEDRALSURFACE Z \()([\(\)\d\.\,\-\s\(]*\))(\))'
#   inner_regex = r'\(([\d\.\,\s\-]*)\)'

#   body = re.search(outer_regex, wkt).group(2)
#   faces = re.findall(inner_regex, body)

#   occ_faces = []

#   for f in faces:
#     face_coords = []
#     f_clean = f.replace(')', '').replace(')', '')
#     f_split = f_clean.split(',')
#     for pt in f_split:
#         coords = [float(d) for d in pt.split(' ')]
#         face_coords.append(tuple(coords))

#     face_polygon = coords_to_polygon(face_coords)
#     face = BRepBuilderAPI_MakeFace(face_polygon, True)
#     occ_faces.append(face.Shape())

#   sew_alg = BRepBuilderAPI_Sewing(1.0) # arg is tolerance
#   for f in occ_faces:
#     sew_alg.Add(f)

#   sew_alg.Perform()
#   result = sew_alg.SewedShape()

#   if type(result) == TopoDS_Shell:
#     print('was shell')
#     sld_alg = BRepBuilderAPI_MakeSolid()
#     sld_alg.Add(result)
#     result = sld_alg.Solid()

#   elif type(result) == TopoDS_Compound:
#     print('was compound')
#     sld_alg = BRepBuilderAPI_MakeSolid()
#     for r in compound_to_list(result, TopAbs_SHELL):
#       sld_alg.Add(r)
#     result = sld_alg.Solid()

#   elif type(result) == TopoDS_Solid:
#     print('was solid')
#     result = result

#   result = upgrade(result)
#   return result


def shape_to_coords(shape, z=False):

  if z:
    coords = [(cp[0], cp[1], 0) for cp in list(shape.coords)]
  else:
    coords = [(cp[0], cp[1]) for cp in list(shape.coords)]

  return coords


def tin_to_occ(wkt, z=True, topo=True):
  mesh_str = re.search(r'TIN Z \(([\(\)\,\.\s\d\-]*)\)', wkt).group(1)
  face_strs = re.findall(r'\(\(([\,\.\s\d\-]*)\)\)', mesh_str)

  sew = BRepBuilderAPI_Sewing()

  for f in face_strs:
    face_verts = f.split(',')
    face_verts_pts = [gp_Pnt(*[float(n) for n in v.split(' ')]) for v in face_verts]
    face_wire = BRepBuilderAPI_MakePolygon(*face_verts_pts).Shape()
    face = BRepBuilderAPI_MakeFace(face_wire).Shape()
    sew.Add(face)

  sew.Perform()

  return sew.SewedShape()


def wkt_to_occ(wkt, topo=False, z=False):
  """Converts a well-known-text geometry representation to OCC geometry.

  For certain types, if topo is True, returns a topology (TopoDS_Shape), 
  otherwise returns a geometry (Curve, Surface etc.)
  """

  wkt = wkt.upper()

  # ignore prepended SRID for now
  if ';' in wkt: wkt = wkt.split(';')[1]

  geomtype_re = r'^([\w]+)[\s]*([ZM]*)[\s]*\('

  geomtype_search = re.search(geomtype_re, wkt)
  geomtype = geomtype_search.group(1)
  geomflags = geomtype_search.group(2)

  z_flag = 'Z' in geomflags or z
  # m_flag = False # not implemented
  # empty_flag = False # not implemented

  handlers = {
    'LINESTRING': linestring_to_occ,
    'MULTIPOLYGON': multipolygon_to_occ,
    'POINT': point_to_occ,
    'POLYGON': polygon_to_occ,
    'POLYHEDRALSURFACE': polyhedralsurfacez_to_occ,
    'TIN': tin_to_occ,
  }

  handler = handlers.get(geomtype, lambda wkt, z, topo: f'{geomtype} NOT SUPPORTED')
  result = handler(wkt, z=z_flag, topo=topo)

  return result

