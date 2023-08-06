from geometry.conversion import coords_to_polygon

class Polygon():
  """Represents a closed 3d polygon geometry using OCC."""

  def __init__(self, vertex_coords):
    self.shape = coords_to_polygon(vertex_coords)

  # def from_wkt():
  #  """From a WKT Polygon"""

  @classmethod
  def from_collada(cls, c_polygon):
    """From a pycollada Polygon"""
    vertices = c_polygon.vertices.tolist()
    vertices.append(vertices[0])
    p = cls(vertices)
    return p

  # def area():
  # """Calculate surface area"""

  # def perimeter():
  # """Calculate perimeter"""
