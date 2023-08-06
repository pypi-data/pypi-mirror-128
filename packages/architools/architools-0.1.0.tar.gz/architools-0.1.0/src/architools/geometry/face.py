from OCC.Core.BOPTools import BOPTools_AlgoTools3D
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.gp import gp_Dir, gp_Vec
from OCC.Core.GProp import GProp_GProps


def face_normal(face, use_topo_orientation=False):
    """Assuming a planar face, return the normal of
    the underlying surface. Note that in OpenCASCADE
    for correctly oriented BReps, face normal will sometimes be
    opposite that of the underlying surface because it is a
    function of wire direction."""

    result = gp_Dir()
    face_as_srf = BRep_Tool.Surface(face)
    BOPTools_AlgoTools3D.GetNormalToSurface(face_as_srf, 0, 0, result)

    if use_topo_orientation and face.Orientation() == 1:
      result.Reverse()

    return result


def face_centroid(face):
    props = GProp_GProps()
    brepgprop_SurfaceProperties(face, props, False, False)
    # check if props.Mass() is less than precision.confusion, throw exception
    result = props.CentreOfMass()
    return result


def face_from_wire(wire):
    """Build a Face from planar Wire"""

    builder = BRepBuilderAPI_MakeFace(wire, True)
    return builder.Face()
