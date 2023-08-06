import tempfile
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal


def shapes_to_step(shapes, path=None):

  if not path:
    temp = tempfile.NamedTemporaryFile()
    path = temp.name

  step_writer = STEPControl_Writer()
  Interface_Static_SetCVal("write.step.schema", "AP203")
  Interface_Static_SetCVal("xstep.cascade.unit", "FT")

  for shape in shapes:
    step_writer.Transfer(shape, STEPControl_AsIs)
  
  status = step_writer.Write(path)
  print(status)
  with open (path, "r") as f:
    result = f.read()

  return result

