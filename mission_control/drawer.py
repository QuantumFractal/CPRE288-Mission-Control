""" Drawer: Draws shapes using SDL_GFX """
#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext
import sdl2.sdlgfx as gfx


function_map = {'rectangle': gfx.rectangleRGBA,
				'box': gfx.boxRGBA,
				'line': gfx.lineRGBA}

color_map = {'white': sdl.ext.Color(255,255,255)}



def render_shape(renderer, shape_string):

	for line in shape_string.split('\n'):
		if '#' in line:
			continue
		line = line.split()

		if line[0] not in function_map:
			continue

		function = function_map[line[0]]
		args = []

		# Add args
		for n in xrange(1, len(line)-1):
			args.append(line[n])

		color = color_map[line[len(line)-1]]

		function(renderer, *args, color)

