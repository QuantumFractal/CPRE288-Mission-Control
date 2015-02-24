# Main application for Mission Control

import serial, os
import sys

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

import sdl2, sdl2.ext


incoming_COM = 'COM4'
outgoing_COM = 'COM8'

# Vortex Settings
vCOM = 'COM2'
vBaud = 38600
vBits = serial.STOPBITS_TWO

#Setup serial port
ser = serial.Serial(port=outgoing_COM, baudrate=9600, stopbits=serial.STOPBITS_TWO)


is_running = True
variable = "pankaces"

WHITE = sdl2.ext.Color(50, 74, 200)
BLACK = sdl2.ext.Color(0,0,0)

''' Initialize pysdl2 stuff '''

sdl2.ext.init()
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
sdl2.SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)

joystick = sdl2.SDL_GameControllerOpen(0)

window = sdl2.ext.Window("MISSION CONTROL", size=(800, 600))
RESOURCES = sdl2.ext.Resources(__file__, "resources")

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
sprite = factory.from_image(RESOURCES.get_path("vortex.png"))
sprite.x = 300
sprite.y = 200

spriterenderer = factory.create_sprite_render_system(window)


uifactory = sdl2.ext.UIFactory(factory)
button = uifactory.from_color(sdl2.ext.gui.BUTTON, WHITE, size=(100,100))
#spriterenderer.render(button)

#button.click(sdl2.events.SDL_QUIT)

def run():
	print variable

	
	window.show()
	running = True
	while running:
		if sdl2.SDL_GameControllerGetButton(joystick, 11):
			sprite.y-=5
			ser.write("w")

		if sdl2.SDL_GameControllerGetButton(joystick, 13):
			sprite.x-=5
			ser.write("a")

		if sdl2.SDL_GameControllerGetButton(joystick, 14):
			sprite.x+=5
			ser.write("s")

		if sdl2.SDL_GameControllerGetButton(joystick, 12):
			sprite.y+=5
			ser.write("d")

		states = sdl2.SDL_GetKeyboardState(None)
		
		for state in states:
			if state is sdl2.SDL_SCANCODE_A:
				print state


		events = sdl2.ext.get_events()
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				running = False
				break
			if event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
				print event.cbutton.state

	
				break
			if event.type == sdl2.SDL_CONTROLLERAXISMOTION:
				if abs(event.caxis.value) > 5000:
					print event.caxis.axis
					if event.caxis.axis is 11:
						print 'MOVED'
						
				break
		sdl2.SDL_Delay(10)
		sdl2.ext.fill(spriterenderer.surface, BLACK)
		spriterenderer.render(sprite)
		window.refresh()
	return 0


if __name__ == "__main__":
	sys.exit(run())