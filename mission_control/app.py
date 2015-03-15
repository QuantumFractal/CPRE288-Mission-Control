# Main application for Mission Control

import sys, os
import serial
import controller

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext



WHITE = sdl2.ext.Color(50, 74, 200)
BLACK = sdl2.ext.Color(0,0,0)

''' Initialize pysdl2 stuff '''




print sdl2.SDL_NumJoysticks()
#print sdl2.SDL_GameControllerName(joystick)


SDL_GameControllerAddMappingsFromFile("resources\mapping.txt")

window = sdl2.ext.Window("MISSION CONTROL", size=(800, 600))
RESOURCES = sdl2.ext.Resources(__file__, "resources")


factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)


controller = Input()

factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer, fontmanager=fontManager)
rendersystem = factory.create_sprite_render_system()

uifactory = sdl2.ext.UIFactory(factory)
button = uifactory.from_color(sdl2.ext.gui.BUTTON, WHITE, size=(100,100))
#spriterenderer.render(button)

#button.click(sdl2.events.SDL_QUIT)

def init_window():
	sdl2.ext.init()
	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
	sdl2.SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)

	sdl_controller = sdl2.SDL_GameControllerOpen(0)

def run():
	init_window()

	window.show()
	running = True
	while running:

		new_events = sdl2.ext.get_events()
		for event in new_events:
			if event.type == SDL_QUIT:
				running = False
		
		inputs = controller.update(new_events)


		sdl2.SDL_Delay(10)
		sdl2.ext.fill(spriterenderer.surface, BLACK)
		spriterenderer.render(sprite)
		window.refresh()
	return 0


if __name__ == "__main__":
	sys.exit(run())