from OCC.Core.gp import gp_Pnt, gp_Pnt2d
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.TopoDS import (
  TopoDS_Wire,
  TopoDS_Compound,
  TopoDS_Solid,
  TopoDS_Shell,
)
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_SOLID, TopAbs_SHELL
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Extend.TopologyUtils import TopologyExplorer
import rhino3dm as rh
from rhino3dm._rhino3dm import Point3d, Brep, Curve, Mesh


def shape_to_rhino(shape):
  """Converts OCC Topology or Geometry to Rhino."""

  # --- POINTS ---
  if isinstance(shape, gp_Pnt):
    coords = shape.Coord()
    result = rh.Point3d(*coords)
    return result

  if isinstance(shape, gp_Pnt2d):
    coords = shape.Coord()
    result = rh.Point3d(*coords, 0.0)
    return result


  # --- OPEN AND CLOSED POLYGONAL WIRES ---
  if isinstance(shape, TopoDS_Wire):
    rhino_pts = []
    closed = shape.Closed()
    explorer = BRepTools_WireExplorer(shape)
    tool = BRep_Tool()
    while explorer.More():
      v = explorer.CurrentVertex()
      occ_pt = tool.Pnt(v)
      rhino_pt = shape_to_rhino(occ_pt)
      rhino_pts.append(rhino_pt)
      explorer.Next()
    
    if closed: rhino_pts.append(rhino_pts[0])

    rhino_crv = rh.NurbsCurve.Create(closed, 1, rhino_pts)
    return rhino_crv

  # --- COMPOUND CONTAINING SOLIDS ---
  if isinstance(shape, TopoDS_Compound):
    breps = []
    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    while explorer.More():
      s = explorer.Current()
      (verts, faces) = brep_verts_faces(s)
      rhino_brep = mesh_from_verts_faces(verts, faces, as_brep=True)
      breps.append(rhino_brep)
      explorer.Next()
    return breps

  # --- SOLID ---
  if isinstance(shape, TopoDS_Solid):
    (verts, faces) = brep_verts_faces(shape)
    rhino_brep = mesh_from_verts_faces(verts, faces, as_brep=True)
    return rhino_brep

  if isinstance(shape, TopoDS_Shell):
    # print('WAS SHELL')
    (verts, faces) = brep_verts_faces(shape)
    rhino_brep = mesh_from_verts_faces(verts, faces, as_brep=False)
    return rhino_brep


def scene_to_rhino(scene, out=None):
  """Converts an architools Scene object to a rhino3dm model.
  If file path out is provided, writes the file to disk, otherwise
  returns encoded binary."""
  
  model = rh.File3dm()
  model.Settings.ModelUnitSystem = rh.UnitSystem.Feet
  model.Strings.__setitem__('UDToolsVersion', '0.0.1')
  model.Strings.__setitem__('UDToolsIdentifier', scene.uuid)

  # set geographic origin of model
  # assume Y axis is due north and elevation is preserved
  offset_x, offset_y = scene.coordinate_offset
  model.Strings.__setitem__('UDToolsOrigin', f'{offset_x},{offset_y}')
  # model.Settings.EarthAnchorPoint.EarthBasepointLatitude = 40.705545313780426
  # model.Settings.EarthAnchorPoint.EarthBasepointLatitude = -74.00794117792812

  for name, layer in scene.layers.items():
    l = add_layer(name, layer.color, layer.parent_name, model)
    for o in layer.objects:
      g = shape_to_rhino(o.geom)
      add_model_object(model, g, name=o.name, layer_index=l.Index)

  if not out:
    return model.Encode()
  else:
    model.Write(out)


known_layers = {}


def add_model_object(model, obj, name=None, layer_index=None):
    """Performs type checking on rhino3dm object and
    call the correct Objects.Add* method to add to a model"""
    uuid = None

    if isinstance(obj, Point3d):
      uuid = model.Objects.AddPoint(obj)
    elif isinstance(obj, Brep):
      uuid = model.Objects.AddBrep(obj)
    elif isinstance(obj, Curve):
      uuid = model.Objects.AddCurve(obj)
    elif isinstance(obj, Mesh):
      uuid = model.Objects.AddMesh(obj)
    else:
      # print(f'UNSUPPORTED TYPE: {0}', type(obj))
      return None

    model_obj = model.Objects.FindId(uuid)

    if name:
      model_obj.Attributes.Name = name

    if layer_index:
      model_obj.Attributes.LayerIndex = layer_index

    return uuid


def add_layer(name, color, parent_name, model):
    """Adds a layer to the Rhino document."""
    l = rh.Layer()
    l.Name = name
    l.Color = color

    if parent_name:
        l.ParentLayerId = known_layers[parent_name]
    
    l_index = model.Layers.Add(l)
    l_from_table = model.Layers.FindIndex(l_index)
    l_id = l_from_table.Id
    known_layers[name] = l_id
    return l_from_table


def brep_verts_faces(brep):
  """Returns vertices and face loops given brep with planar faces"""
  explorer = TopologyExplorer(brep)
  tool = BRep_Tool()
  verts = []
  faces = []

  # ensure there is a triangulation on the brep
  BRepMesh_IncrementalMesh(brep, 1.0)

  for f in explorer.faces():
    triangulation = tool.Triangulation(f, TopLoc_Location())
    tris = triangulation.Triangles()

    for t in tris:
      nodes = t.Get()
      tri_pts = []

      for n in nodes:
        n_pt = triangulation.Node(n).Coord()
        if n_pt not in verts: verts.append(n_pt)
        tri_pts.append(n_pt)

      face = [verts.index(p) for p in tri_pts]
      faces.append(tuple(face))
  
  return(verts, faces)


def mesh_from_verts_faces(verts, faces, as_brep=False):
  mesh = rh.Mesh()

  for p in verts:
    mesh.Vertices.Add(*p)

  for f in faces:
    mesh.Faces.AddFace(*f)

  if as_brep: mesh = rh.Brep.CreateFromMesh(mesh, False)
  return mesh
