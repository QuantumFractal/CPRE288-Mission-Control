# -*- coding: utf-8 -*-
""" Object Detection Viewer """
import serial, os, copy
import sys
import ctypes

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
from math import sin, cos, radians
import sdl2.ext
import sdl2.sdlgfx as gfx


class Radar():

    def __init__(self, renderer, x=200, y=200, h=200):
        #SDL Semantics :/
        self.renderer = renderer.renderer
        self.sprites = []
        self.data = None

        self.x = x
        self.y = y

        self.pad = 20
        self.steps = 8
        self.points = [() for x in range(90)] 
        
        self.w = h*2
        self.h = h+2*self.pad
        self.sensor_max = 200 # In CM

        self.dark_orange = sdl2.ext.Color(59, 42, 14)
        self.orange = sdl2.ext.Color(212, 104, 45)
        self.white = sdl2.ext.Color(200, 200, 200)
        self.green = sdl2.ext.Color(0, 255, 0)
        self.dark_green = sdl2.ext.Color(0, 176, 0)
        

    def update(self):
        pass


    def set_data(self, data):
        points = self.points 
        for n in range(len(points)):
            # N is our angle
            amplitude = self.map_value(data[n], 0, 200, 0, self.w/2-self.pad)
            xpos = amplitude*cos(radians(self.map_value(n*2+1,0,180,5,175)))
            ypos = amplitude*sin(radians(self.map_value(n*2+1,0,180,5,175)))

            points[n] = int(xpos), int(ypos)


    def draw(self):
        self.draw_grid()
        self.draw_data()

    def draw_data(self):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pad = self.pad

        points_x = []
        points_y = []

        # Make points relative to our radar
        for point in self.points:
            points_x.append(point[0]+x+w/2)
            points_y.append(-1*point[1]+y+h-2*pad)

        # Add last point to make things look nice
        points_x.append(x+w/2)
        points_y.append(y+h-2*pad)


        # Do some fancy ctypes magic
        #points_x , points_y = zip(*self.points)

        xptr = (ctypes.c_short * len(points_x))(*points_x)
        yptr = (ctypes.c_short * len(points_x))(*points_y)

        gfx.aapolygonRGBA(self.renderer, xptr, yptr, 91, *self.green.rgba )


    def draw_grid(self):
        #gfx.circleRGBA(self.renderer, 400, 400 , 100, *self.green.rgba)
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pad = self.pad

        # Draw radar background
        gfx.boxRGBA(self.renderer, x, y, x+w, y+h, *self.dark_orange.rgba)

        # Draw border
        gfx.rectangleRGBA(self.renderer, x, y, x+w, y+h, *self.white.rgba)

        '''TEST LINE'''
        #gfx.hlineRGBA(self.renderer, x, x+w, y+h-2*pad, *self.white.rgba)
        
        # Draw arcs / labels
        for n in xrange(0, w/2-pad, (w/2-pad)/self.steps):
            # Draw radar lines
            gfx.arcRGBA(self.renderer, x+w/2, y+h-2*pad, n, 185, -5, *self.orange.rgba)

            # Draw distance marks
            mark_y = int(y+h-2*pad-n*sin(radians(5)))+8
            mark_x = int(x+w/2-n*cos(radians(5)))

            ''' TEST LINE '''
            #gfx.vlineRGBA(self.renderer, mark_x, y+h-2*pad, mark_y, *self.white.rgba)

            literal_dist = self.map_value(n, 0, w/2-pad, 0, self.sensor_max)
            gfx.stringRGBA(self.renderer, mark_x, mark_y, str(literal_dist)+"cm", *self.orange.rgba)

        # Draw lines
        for n in range(0, 181, 180/6):
            xpos = int((w/2-pad)*cos(radians(self.map_value(n,0,180,5,175))))
            ypos = -1*int((w/2-pad)*sin(radians(self.map_value(n,0,180,5,175))))

            gfx.lineRGBA(self.renderer, x+w/2, y+h-2*pad, xpos+x+w/2, ypos+y+h-2*pad, *self.orange.rgba )
        # Draw Angle labels

         # Draw outside border
        gfx.pieRGBA(self.renderer, x+w/2, y+h-2*pad, w/2-pad, 185, -5, *self.orange.rgba)


    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min