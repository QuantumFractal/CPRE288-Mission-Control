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
			if event.type == SDL_CONTROLLERBUTTONDOWN:
				print event.button
		


		sdl2.SDL_Delay(10)
		window.refresh()
	return 0


if __name__ == "__main__":
	sys.exit(run())