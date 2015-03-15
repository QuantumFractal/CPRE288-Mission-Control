#Controller 


import serial, os
import sys

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

import sdl2, sdl2.ext


class Controller():

	def __init__(self):
		sdl2.ext.init()
		sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
		sdl2.SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)
		sdl2.SDL_GameControllerEventState(sdl2.SDL_IGNORE)

		self.joystick = sdl2.SDL_GameControllerOpen(0)

		self.buttons = {}
		self.button_map = {'X'}
		for button in self.button_map:
			self.buttons[button] = None

		self.dpad = {}
		self.dpad_map = {'up':11, 'down':12, 'left':13, 'right':14}
		for direction in self.dpad_map:
			self.dpad[direction] = None

		self.joysticks = {}

		#print sdl2.SDL_JoystickNumButtons(self.joystick)

	def update(self):
		sdl2.SDL_GameControllerUpdate()
		print sdl2.SDL_GameControllerGetButton(self.joystick, 1)





#Simple button state wrapper
def getButtonState(joystick, button):
	return sdl2.SDL_GameControllerGetButton(joystick, button)

ds4 = Controller()
var = ""

print sdl2.SDL_NumJoysticks()
print sdl2.SDL_GameControllerName(ds4.joystick)

#ds4.joystick.rumble(20, 40)

while(True):
	#print sdl2.SDL_GameControllerGetAxis(ds4.joystick,0)
	ds4.update()
	sdl2.SDL_Delay(10)

