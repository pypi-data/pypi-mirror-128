"""Outline is the base class for architools building classes.
It can be used by itself or subclassed to handle specific use cases.
"""

from OCC.Extend.TopologyUtils import TopologyExplorer

from architools.geometry.common import get_faces
from architools.geometry.face import face_normal, face_centroid
from architools.geometry.edge import tangent_on_edge
from architools.geometry.wire import to_curve_from_vertices
from architools.geometry.curve import pt_on_curve
from architools.geometry.vector import (
  is_up,
  is_down,
  is_horiz,
  is_vert,
)

class Outline:

  def __init__(self, geom):
    self.geom = geom # OCC Shape
    self.nonmanifold = None
    self.explorer = None
    self.faces = []
    self.faces_interior = []
    self.faces_up = []
    self.faces_down = []
    self.faces_vert = []
    self.faces_horiz = []
    self.edges = []
    self.edges_concave = []
    self.edges_roof = []
    self.edges_belly = []
    self.edges_floor = []
    self.edges_corner = []

  def classify_edges(self):
    """Indexes shape edges by topological relationship.
    Expects that classify_faces has already run.
    """
    self.initialize_shape_explorer()

    for i, e in enumerate(self.explorer.edges()):
      self.edges.append(e)
      d = tangent_on_edge(e, 0.5, as_dir=True, use_topo_orientation=True)
      connected_faces = self.explorer.faces_from_edge(e)

      # wall corner edge test
      if is_vert(d): self.edges_corner.append(i)

      compare_faces = []
      for f in connected_faces:
        # roof/belly/floor edge tests
        if any([f.IsEqual(rf) for rf in self.roof_faces()]):
          self.edges_roof.append(i)
        elif any([f.IsEqual(rf) for rf in self.belly_faces()]):
          self.edges_belly.append(i)
        elif any([f.IsEqual(rf) for rf in self.floor_faces()]):
          self.edges_floor.append(i)

        if any([f.IsEqual(rf) for rf in self.exterior_faces()]):
          compare_faces.append(f)

      # concavity test
      # compare face normals of attached exterior faces
      # obtained in previous iteration over connected faces
      # by measuring angle across axis of edge, we can know
      # whether the angle is concave or convex
      compare_normals = [face_normal(f) for f in compare_faces]
      if len(compare_normals) == 2:
        n1 = compare_normals[0]
        n2 = compare_normals[1]
        angle = n1.AngleWithRef(n2, d)

        if angle < 0: self.edges_concave.append(i)


  def classify_faces(self):
    """Update topology indexing. This must be called whenever
    the underlying geom is updated, otherwise results will be invalid!
    """
    self.initialize_shape_explorer()

    for i, f in enumerate(self.explorer.faces()):
      self.faces.append(f)
      n = face_normal(f, use_topo_orientation=True)
      face_edges = self.explorer.edges_from_face(f)

      nonmanifold_flags = []
      for e in face_edges:
        num_connected_faces = self.explorer.number_of_faces_from_edge(e)
        is_nonmanifold = num_connected_faces > 2
        nonmanifold_flags.append(is_nonmanifold)

      self.nonmanifold = any(nonmanifold_flags)

      if all(nonmanifold_flags):
        self.faces_interior.append(i)

      if is_up(n): self.faces_up.append(i)
      if is_down(n): self.faces_down.append(i)
      if is_horiz(n): self.faces_vert.append(i) # face is vertical if normal is horizontal
      if is_vert(n): self.faces_horiz.append(i) # face is horizontal if normal is vertical

  def initialize_shape_explorer(self):
    if not self.explorer:
      self.explorer = TopologyExplorer(self.geom)

  # --- indexed shape accessors ---

  def exterior_faces(self):
    return [f for i, f in enumerate(self.faces) if i not in self.faces_interior]

  def floor_faces(self):
    return [self.faces[i] for i in self.faces_interior if i in self.faces_horiz]

  def wall_faces(self):
    return [self.faces[i] for i in self.faces_vert if not i in self.faces_interior]

  def facade_faces(self):
    return [self.faces[i] for i in self.faces_vert if not i in self.faces_interior]

  def roof_faces(self):
    return [self.faces[i] for i in self.faces_up if not i in self.faces_interior]

  def belly_faces(self):
    return [self.faces[i] for i in self.faces_down if not i in self.faces_interior]

  #def unclassed_faces(self):

  def corner_edges(self):
    return [self.edges[i] for i in self.edges_corner]

  def parapet_edges(self):
    return [self.edges[i] for i in self.edges_roof if not i in self.edges_concave]

  #def unclassed_edges(self):

  # TODO: area calcs

  # TODO: volumes/rooms

  # in udtools, extend class and take lot into consideration
  # possible optimizations:
  # when roof edges only: if not is_up(n): continue after getting normal

# OLD:

# from math import pi
# from geometry.conversion import wire_to_face, faces_to_outline
# from geometry.primitives import Polygon
# from geometry.reference import pos_z, north, south, east, west
# from geometry.measure import area, perimeter, normal, horiz_tol, vert_tol
# from geometry.topology import get_edges, get_subshapes, count_connected

# class Outline():
#   """The Outline class expresses a nonmanifold geometry"""

#   def __init__(self, shape):
#     self.id = 'myoutline'
#     self.shape = shape
#     self.summary = {
#       'floor_area': 0,
#       'wall_area': 0,
#       'wall_perimeter': 0,
#       'facade_area': 0,
#     }
#     self.faces = {
#       'belly': [],
#       'facade': [],
#       'floor': [],
#       'roof': [],
#       'wall': [],
#     }

#   @classmethod
#   def from_collada(cls, collada):
#     """Create an Outline using the first geometry in a collada file"""
    
#     geom = collada.geometries[0]
#     wires = [Polygon.from_collada(p) for p in geom.primitives[0]]
#     faces = [wire_to_face(w.shape) for w in wires]
#     shape = faces_to_outline(faces)
#     o = cls(shape)
#     return o

#   def classify_faces(self):
#     faces = get_subshapes(self.shape, 'face')
    
#     for idx, f in enumerate(faces):
#       f = Face(f)

#       i = f.is_interior(self.shape)
#       h = f.is_horiz()
#       v = f.is_vert()

#       # interior floors
#       if i and h:
#         self.faces['floor'].append(idx)
#         self.summary['floor_area'] += area(f.shape)
#         self.summary['wall_perimeter'] += perimeter(f.shape)
#         continue

#       # interior walls
#       if i and v:
#         self.faces['wall'].append(idx)
#         self.summary['wall_area'] += area(f.shape) * 2 # double since two-sided
#         continue

#       # exterior walls (facades)
#       if v:
#         self.faces['facade'].append(idx)
#         a = area(f.shape)
#         self.summary['wall_area'] += a
#         self.summary['facade_area'] += a
#         continue

#       # roof
#       if f.is_up():
#         self.faces['roof'].append(idx)
#         continue

#       # belly
#       if f.is_down():
#         self.faces['belly'].append(idx)
#         continue

#       # warn if not classified?


# class Face():
#   """The Face class expresses a face within the Outline...
  
#   ...and provides tests to determine how to further classify it
#   as a wall, floor etc.
#   """

#   def __init__(self, shape):
#     self.shape = shape
#     self.normal = normal(shape)


#   def is_up(self):
#     a = self.normal.Angle(pos_z)
#     test = a < (0 + horiz_tol)
#     return test


#   def is_down(self):
#     a = self.normal.Angle(pos_z)
#     test = a > (pi - horiz_tol)
#     return test


#   def is_horiz(self):
#     test = self.is_up() or self.is_down()
#     return test


#   def is_vert(self):
#     a = self.normal.Angle(pos_z)
#     test = (pi/2 - vert_tol) < a < (pi/2 + vert_tol)
#     return test


#   def is_interior(self, topo):
#     edges = get_edges(self.shape)
#     print([count_connected(topo, 'edge', 'face', e) for e in edges])
#     test = all(count_connected(topo, 'edge', 'face', e) > 2 for e in edges)
#     return test
