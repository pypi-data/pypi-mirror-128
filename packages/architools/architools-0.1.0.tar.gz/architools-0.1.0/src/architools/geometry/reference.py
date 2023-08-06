from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Ax1, gp_Vec
from OCC.Core.Geom import Geom_Plane
from OCC.Core.TopLoc import TopLoc_Location


world_origin = gp_Pnt(0, 0, 0)


# axis directions
pos_x = gp_Dir(1, 0, 1)
pos_y = gp_Dir(0, 1, 0)
pos_z = gp_Dir(0, 0, 1)
neg_x = gp_Dir(-1, 0, 1)
neg_y = gp_Dir(0, -1, 0)
neg_z = gp_Dir(0, 0, -1)


# cardinal directions
# ASSUMING POSITIVE Y IS NORTH!
north = gp_Dir(0, 1, 0)
south = gp_Dir(0, -1, 0)
east = gp_Dir(1, 0, 0)
west = gp_Dir(-1, 0, 0)


# unit vectors
unit_x = gp_Vec(1, 0, 0)
unit_y = gp_Vec(0, 1, 0)
unit_z = gp_Vec(0, 0, 1)


# world axes
world_x_ax = gp_Ax1(world_origin, pos_x)
world_z_ax = gp_Ax1(world_origin, pos_z)
world_y_ax = gp_Ax1(world_origin, pos_y)


# world axis planes
world_xy = gp_Pln(world_origin, pos_z)
world_xz = gp_Pln(world_origin, pos_y)
world_yz = gp_Pln(world_origin, pos_x)

world_xy_geom = Geom_Plane(world_xy)
world_xz_geom = Geom_Plane(world_xz)
world_yz_geom = Geom_Plane(world_yz)


# default datum
default_datum = TopLoc_Location()
