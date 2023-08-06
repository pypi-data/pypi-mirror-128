# from OCC.Core.ShapeUpgrade import ShapeUpgrade_UnifySameDomain

# def upgrade(brep):
#   """use SetAngularTolerance(), SetLinearTolerance() to fine-tune results"""

#   result = ShapeUpgrade_UnifySameDomain(brep, True, True, False)
#   result.SetAngularTolerance(1.0)
#   result.SetLinearTolerance(1.0)
#   result.Build()
#   resultshape = result.Shape()
#   return resultshape

# ShapeUpgrade not working as of 2021-09-19