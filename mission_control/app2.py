"""Main application for Mission Control"""

import serial, os
import sys
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext



#Setup serial port
WHITE = sdl2.ext.Color(50, 74, 200)
BLACK = sdl2.ext.Color(0,0,0)

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
''' Initialize pysdl2 stuff '''

sdl2.ext.init()
SDL_Init(sdl2.SDL_INIT_VIDEO)
SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)

joystick = SDL_GameControllerOpen(0)

window = sdl2.ext.Window("Mission Control", size=(WINDOW_WIDTH, WINDOW_HEIGHT))
RESOURCES = sdl2.ext.Resources(__file__, "resources")

renderer = sdl2.ext.Renderer(window)

fontManager = sdl2.ext.FontManager('resources/eurostile.ttf')

sprites = []

factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer, fontmanager=fontManager)
rendersystem = factory.create_sprite_render_system()

vortex = factory.from_image(RESOURCES.get_path("vortex.png"))
vortex.x, vortex.y = (100,100)


text = factory.from_surface(fontManager.render("Mission Control",  size=50))
text.x, text.y = (WINDOW_WIDTH/2-(text.size[0]/2), 0)

sprites.append(text)
sprites.append(vortex)

def render(sprites, renderer):
	r = SDL_Rect()
	dorender = SDL_RenderCopy
	renderer.clear(BLACK)

	for sprite in sprites:
		r.x = int(sprite.x)
		r.y = int(sprite.y)
		r.w, r.h = sprite.size

		dorender(renderer.renderer, sprite.texture, None, r)

	renderer.present()

def run():
	window.show()
	running = True
	while running:
		events = sdl2.ext.get_events()
		for event in events:
			if event.type == SDL_QUIT:
				running = False
				break

		#sdl2.ext.fill(spriterenderer.surface, BLACK)
		render(sprites,renderer)


if __name__ == "__main__":
	sys.exit(run())