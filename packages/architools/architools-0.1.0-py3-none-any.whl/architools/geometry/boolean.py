from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse,
    BRepAlgoAPI_Common,
    BRepAlgoAPI_Cut,
    BRepAlgoAPI_Section,
)
# from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon
# from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
# from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BOPAlgo import BOPAlgo_Builder, BOPAlgo_MakerVolume
# from OCC.Core.gp import gp_Vec, gp_Dir
from OCC.Core.TopTools import TopTools_ListOfShape


def union(breps):
  #result = BOPAlgo_Builder()
  # result = BOPAlgo_MakerVolume()
  
  if len(breps) == 1: return breps[0]

  union_alg = BRepAlgoAPI_Fuse()

  args = TopTools_ListOfShape()
  args.Append(breps.pop())
  union_alg.SetArguments(args)

  tools = TopTools_ListOfShape()
  for b in breps:
    tools.Append(b)
    #result.AddArgument(b)
  union_alg.SetTools(tools)

  union_alg.SetFuzzyValue(0.1)
  union_alg.SetRunParallel(True)
  union_alg.Build()

  return union_alg.Shape()
  # result.SetRunParallel(True)
  # # or performwithfiller
  # result.Perform()

  # if result.HasErrors():
  #   print('error performing union')

  # return result.Shape()

def intersection(b1, b2):

  comm = BRepAlgoAPI_Common()
  args = TopTools_ListOfShape()
  args.Append(b1)
  comm.SetArguments(args)

  tools = TopTools_ListOfShape()
  tools.Append(b2)
  comm.SetTools(args)

  comm.SetFuzzyValue(0.1)
  comm.SetRunParallel(True)
  comm.Build()

  return comm.Shape()


def diff(brep, cutter, clean=True):

  cut = BRepAlgoAPI_Cut()

  args = TopTools_ListOfShape()
  args.Append(brep)
  cut.SetArguments(args)

  tools = TopTools_ListOfShape()
  tools.Append(cutter)
  cut.SetTools(tools)

  cut.SetFuzzyValue(0.1)
  cut.SetRunParallel(True)
  cut.Build()

  # if clean: return cut.Shape()
  return cut.Shape()


def section(brep, cutter):

  section_alg = BRepAlgoAPI_Section()
  args = TopTools_ListOfShape()
  args.Append(brep)
  section_alg.SetArguments(args)

  tools = TopTools_ListOfShape()
  tools.Append(cutter)
  section_alg.SetTools(tools)

  section_alg.SetFuzzyValue(0.1)
  section_alg.SetRunParallel(True)
  section_alg.Build()

  return section_alg.Shape()