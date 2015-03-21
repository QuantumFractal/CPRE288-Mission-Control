""" Sim file that holds all classes for vortex simulator """

import sys, os, copy

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext
import sdl2.sdlgfx as gfx
import itertools
from math import sin, cos, radians

SCALE = 2

rectangle = gfx.rectangleRGBA
box = gfx.boxRGBA
line = gfx.lineRGBA
circle = gfx.circleRGBA
pie = gfx.pieRGBA
text = gfx.stringRGBA


white = sdl2.ext.Color(255,255,255)
light_green = sdl2.ext.Color(144, 238, 144)
red = sdl2.ext.Color(255, 0, 0)


class sim_obj():
	def draw(self, renderer):
		print 'You can\' draw this'


class Vortex(sim_obj):
	def __init__(self, pos=(0,0)):
		self.x = pos[0]
		self.y = pos[1]
		self.rotation = 0
		self.sensor_rotation = 0


	def draw(self, renderer):
		x = self.x
		y = self.y
		r = self.rotation
		sr = self.sensor_rotation

		# Outside line
		circle(renderer, x, y, 24, *white.rgba)

		semi_off_x = rnd(x+2*sin(radians(r)))
		semi_off_y = rnd(y-2*cos(radians(r)))

		# Front semi circle
		pie(renderer, semi_off_x , semi_off_y , 18, rnd(180+r), rnd(0+r), *white.rgba)
		
		# Draw label
		line(renderer, rnd(x+10*sin(radians(r+180))), rnd(y-10*cos(radians(r+180))), x, y, *white.rgba)

		# Draw sensor sweep
		sensor_off_x = rnd(x+16*sin(radians(r)))
		sensor_off_y = rnd(y-16*cos(radians(r)))
		pie(renderer, sensor_off_x, sensor_off_y, 200, rnd(260+sr), rnd(0+sr-80), *light_green.rgba)


class Dropoff(sim_obj):
	def __init__(self, size, pos=(0,0)):
		self.x = pos[0]
		self.y = pos[1]
		self.size = size

	def draw(self, renderer):
		x = self.x
		y = self.y
		size = self.size

		# Draw box
		rectangle(renderer, x-size, y-size, x+size, y+size, *red.rgba)


def draw_rotated_rect(renderer, x1, y1, x2, y2, degrees, color, ox=0, oy=0):
	points = ((x1,y1),(x2,y1),(x2,y2),(x1,y2))
	pts = []

	for point in points:
		x = point[0] - ox
		y = point[1] - oy

		temp_x = rnd(x * cos(radians(degrees)) - y * sin(radians(degrees)))
		temp_y = rnd(x * sin(radians(degrees)) + y * cos(radians(degrees)))
		pts.append((temp_x+ox, temp_y+oy))

	for n in xrange(4):
		line(renderer, pts[n][0], pts[n][1], pts[(n+1)%4][0], pts[(n+1)%4][1], *color.rgba)

def map_value(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def rnd(float):
	return int(round(float))