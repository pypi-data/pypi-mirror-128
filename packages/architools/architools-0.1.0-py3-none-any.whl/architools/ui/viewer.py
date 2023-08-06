import ctypes
import logging
import os
import sys

# from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
# from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_ALICEBLUE, Quantity_NOC_ANTIQUEWHITE
# from OCC.Display import OCCViewer
# from OCC.Display.backend import load_backend, get_qt_modules
# from OCC.Display.SimpleGui import init_display
# # QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

# from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeTorus
# from OCC.Core.Bnd import Bnd_Box
# from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Display.backend import load_backend
from OCC.Display.


def start_occ_display():


    print(loggers)

    display, start_display, add_menu, add_function_to_menu = init_display()
    # register callbacks
    display.register_select_callback(print_xy_click)
    display.register_select_callback(compute_bbox)
    display.EnableAntiAliasing()

    # creating geometry
    my_torus = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
    my_box = BRepPrimAPI_MakeTorus(30., 5.).Shape()
    # and finally display geometry
    display.DisplayShape(my_torus)
    display.DisplayShape(my_box, update=True)
    start_display()
