"""Provides classes and functions related to the geographic location
of architools sites, allowing for interoperability with GIS and other
spatial data workflows.

LIST CLASSES, FUNCTIONS ETC EXPORTED W 1-LINE SUMMARY
"""

class AOI():
  """Area of Interest, defines a custom local coordinate system
  for buildings and scenes based on a CRS and transform.

  LIST PUBLIC METHODS/INSTANCE VARIABLES
  """

  def __init__(self, crs, transform):
    """Initialize a new AOI, given a CRS and transform."""
    self.crs = None # crs by EPSG code
    self.transform = (0, 0, 0) # transform by x, y, z
