#Controller 


import serial, os, copy
import sys

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext
import sdl2.sdlgfx as sdlgfx


class Controller():

    def __init__(self, sdl_controller):

        self.Controller

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


class ControllerGUI():

    def __init__(self, factory, x=0, y=0):
        SDL_GameControllerAddMappingsFromFile("resources/mapping.txt")
        self.controller = SDL_GameControllerOpen(0)
        self.haptics = SDL_HapticOpen(0)

        RESOURCES = sdl2.ext.Resources(__file__, "resources")

        self.x = x
        self.y = y
        self.deadzone = 5000
        self.top = 32767
        self.gui_stick_limit = 9

        self.ds4 = factory.from_image(RESOURCES.get_path("ds4.png"))

        self.button_sprite = factory.from_image(RESOURCES.get_path('ds4_button.png'))
        button_sprite = self.button_sprite
        button_sprite.hidden = True
        cp = copy.copy

        self.buttons = {'square':cp(button_sprite), 'cross':cp(button_sprite), 
                        'triangle':cp(button_sprite), 'circle':cp(button_sprite)}
        self.sticks = {'left': [(0,0),(0,0)], 'right': [(0,0),(0,0)], 
                        'l_trigger': [(0,0),(0,0)], 'r_trigger': [(0,0),(0,0)]}

        self.stick_sprite = factory.from_image(RESOURCES.get_path('ds4_cap.png'))
        stick_sprite = self.stick_sprite

        self.stick_sprites = {'left': cp(stick_sprite), 'right': cp(stick_sprite),
                                'l_trigger': cp(button_sprite), 'r_trigger': cp(button_sprite)}
        self.factory = factory
        self.sprites = []

        self.update()


    def update(self):

        sprites = []

        SDL_GameControllerUpdate()
        self.update_buttons()
        self.update_sticks()

        self.ds4.position = self.x , self.y
        sprites.append(self.ds4)

        #Set vectors for buttons
        self.buttons['square'].position = self.x+223, self.y+57
        self.buttons['cross'].position = self.x+245, self.y+79
        self.buttons['circle'].position = self.x+267, self.y+57
        self.buttons['triangle'].position = self.x+245, self.y+35

        ss = self.stick_sprites
        sp = self.sticks

        ss['left'].position = self.x+sp['left'][1][0]+100 , self.y+sp['left'][1][1]+94
        ss['right'].position = self.x+sp['right'][1][0]+195 , self.y+sp['right'][1][1]+94


        for button in self.buttons:
            sprites.append(self.buttons[button])
        for stick in self.stick_sprites:
            sprites.append(self.stick_sprites[stick])

        

        self.sprites = sprites

    def update_buttons(self):
        if bool(SDL_GameControllerGetButton(self.controller, 0)):
            self.buttons['cross'].hidden = False
            self.rumble(40, 100)
        else:
            self.buttons['cross'].hidden = True

        if bool(SDL_GameControllerGetButton(self.controller, 3)):
            self.buttons['triangle'].hidden = False
        else: 
            self.buttons['triangle'].hidden = True

        if bool(SDL_GameControllerGetButton(self.controller, 2)):
            self.buttons['square'].hidden = False
        else: 
            self.buttons['square'].hidden = True

        if bool(SDL_GameControllerGetButton(self.controller, 1)):
            self.buttons['circle'].hidden = False
        else: 
            self.buttons['circle'].hidden = True

    def update_sticks(self):
        get_axis = SDL_GameControllerGetAxis
        c = self.controller
        """
            Axis 0: Left Horizontal
            Axis 1: Left Vertical
            Axis 2: Right Horizontal
            Axis 3: Right Vertical 
            Axis 4: Left Trigger
            Axis 5: Right Trigger
        """

        #Map both the actual stick and the gui version
        self.sticks['left'][0] = self.map_stick(0,1)
        self.sticks['left'][1] = self.map_stick(0,1,gui=True)

        self.sticks['right'][0] = self.map_stick(2,3)
        self.sticks['right'][1] = self.map_stick(2,3,gui=True)

        test_sprite = self.stick_sprites['l_trigger']
        test_sprite.surface = sdlgfx.zoomSurface(test_sprite.surface, 5, 5, 1)

    def rumble(self, intensity, length_ms):
        SDL_HapticRumblePlay(self.haptics, intensity, length_ms)


    def map_stick(self, hori_axis, vert_axis, gui=False):
        get_axis = SDL_GameControllerGetAxis
        hori_axis = get_axis(self.controller, hori_axis)
        vert_axis = get_axis(self.controller, vert_axis)

        hori_axis = 0 if abs(hori_axis) < self.deadzone else hori_axis
        vert_axis = 0 if abs(vert_axis) < self.deadzone else vert_axis

        if gui:
            hori_axis = self.map_value(hori_axis, 0, self.top, 0, self.gui_stick_limit)
            vert_axis = self.map_value(vert_axis, 0, self.top, 0, self.gui_stick_limit)

        return hori_axis, vert_axis


    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

