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
        self.gui_trigger_limit = 15

        self.ds4 = factory.from_image(RESOURCES.get_path("ds4.png"))

        self.button_sprite = factory.from_image(RESOURCES.get_path('ds4_button.png'))
        button_sprite = self.button_sprite
        button_sprite.hidden = True

        self.lbumper_sprite = factory.from_image(RESOURCES.get_path('ds4_bumper.png'))
        lbumper_sprite = self.lbumper_sprite
        lbumper_sprite.hidden = True

        self.rbumper_sprite = factory.from_image(RESOURCES.get_path('ds4_bumper_r.png'))
        rbumper_sprite = self.rbumper_sprite
        rbumper_sprite.hidden = True

        self.trigger_sprite = factory.from_image(RESOURCES.get_path('ds4_arrow.png'))
        trigger_sprite = self.trigger_sprite
        trigger_sprite.hidden = False

        cp = copy.copy

        self.buttons = {'square': False, 'cross': False, 
                        'triangle': False, 'circle': False,
                        'dpad-up': False, 'dpad-down': False,
                        'dpad-left': False, 'dpad-right': False,
                        'l_bumper': False, 'r_bumper': False}

        self.button_sprites = {'square':cp(button_sprite), 'cross':cp(button_sprite), 
                        'triangle':cp(button_sprite), 'circle':cp(button_sprite),
                        'dpad-up':cp(button_sprite), 'dpad-down':cp(button_sprite),
                        'dpad-left':cp(button_sprite), 'dpad-right':cp(button_sprite),
                        'l_bumper':cp(lbumper_sprite), 'r_bumper':cp(rbumper_sprite)}

        self.sticks = {'left': [(0,0),(0,0)], 'right': [(0,0),(0,0)], 
                        'l_trigger': [0,0], 'r_trigger': [0,0]}

        self.stick_sprite = factory.from_image(RESOURCES.get_path('ds4_cap.png'))
        stick_sprite = self.stick_sprite

        self.stick_sprites = {'left': cp(stick_sprite), 'right': cp(stick_sprite),
                                'l_trigger': cp(trigger_sprite), 'r_trigger': cp(trigger_sprite)}
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
        bs = self.button_sprites
        bs['square'].position = self.x+223, self.y+57
        bs['cross'].position = self.x+245, self.y+79
        bs['circle'].position = self.x+267, self.y+57
        bs['triangle'].position = self.x+245, self.y+35
        bs['l_bumper'].position = self.x+51, self.y+11
        bs['r_bumper'].position = self.x+232, self.y+12
        bs['dpad-up'].position = self.x+58, self.y+36
        bs['dpad-down'].position = self.x+58, self.y+76
        bs['dpad-left'].position = self.x+38, self.y+56
        bs['dpad-right'].position = self.x+78, self.y+56

        ss = self.stick_sprites
        sp = self.sticks

        ss['left'].position = self.x+sp['left'][1][0]+100 , self.y+sp['left'][1][1]+94
        ss['right'].position = self.x+sp['right'][1][0]+195 , self.y+sp['right'][1][1]+94
        ss['l_trigger'].position = self.x+63, self.y+int(sp['l_trigger'][1])-33
        ss['r_trigger'].position = self.x+245, self.y+int(sp['r_trigger'][1])-33

        for button in self.button_sprites:
            sprites.append(self.button_sprites[button])
        for stick in self.stick_sprites:
            sprites.append(self.stick_sprites[stick])

        

        self.sprites = sprites

    def update_buttons(self):
        """ Button Layout
            cross: 0
            triangle: 3
            square: 2
            circle: 1
            l_stick: 7
            r_stick: 8
            r_bumper: 10
            l_bumper: 9
            dpad-up: 11
            dpad-down: 12
            dpad-left: 13
            dpad-right: 14
        """
        get_button = SDL_GameControllerGetButton
        bs = self.button_sprites
        b = self.buttons

        if bool(get_button(self.controller, 11)):
            bs['dpad-up'].hidden = False
            b['dpad-up'] = True
        else:
            bs['dpad-up'].hidden = True
            b['dpad-up'] = False
        
        if bool(get_button(self.controller, 12)):
            bs['dpad-down'].hidden = False
            b['dpad-down'] = True
        else:
            bs['dpad-down'].hidden = True
            b['dpad-down'] = False

        if bool(get_button(self.controller, 13)):
            bs['dpad-left'].hidden = False
            b['dpad-left'] = True
        else:
            bs['dpad-left'].hidden = True
            b['dpad-left'] = False

        if bool(get_button(self.controller, 14)):
            bs['dpad-right'].hidden = False
            b['dpad-right'] = True
        else:
            bs['dpad-right'].hidden = True
            b['dpad-right'] = False

        if bool(get_button(self.controller, 9)):
            bs['l_bumper'].hidden = False
            b['l_bumper'] = True
        else:
            bs['l_bumper'].hidden = True
            b['l_bumper'] = False

        if bool(get_button(self.controller, 10)):
            bs['r_bumper'].hidden = False
            b['r_bumper'] = True
        else:
            bs['r_bumper'].hidden = True
            b['r_bumper'] = True

        if bool(get_button(self.controller, 0)):
            bs['cross'].hidden = False
            b['cross'] = True
        else:
            bs['cross'].hidden = True
            b['cross'] = False

        if bool(get_button(self.controller, 3)):
            bs['triangle'].hidden = False
            b['triangle'] = True
        else: 
            bs['triangle'].hidden = True
            b['triangle'] = False

        if bool(get_button(self.controller, 2)):
            bs['square'].hidden = False
            b['square'] = True
        else: 
            bs['square'].hidden = True
            b['square'] = False

        if bool(get_button(self.controller, 1)):
            bs['circle'].hidden = False
            b['circle'] = True
        else: 
            bs['circle'].hidden = True
            b['circle'] = False

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

        self.sticks['l_trigger'][0] = self.map_trigger(4)
        self.sticks['l_trigger'][1] = self.map_trigger(4, gui=True)

        if self.sticks['l_trigger'][1] == 0:
            self.stick_sprites['l_trigger'].hidden = True
        else:
            self.stick_sprites['l_trigger'].hidden = False

        self.sticks['r_trigger'][0] = self.map_trigger(5)
        self.sticks['r_trigger'][1] = self.map_trigger(5, gui=True)

        if self.sticks['r_trigger'][1] == 0:
            self.stick_sprites['r_trigger'].hidden = True
        else:
            self.stick_sprites['r_trigger'].hidden = False

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


    def map_trigger(self, axis, gui=False):
        get_axis = SDL_GameControllerGetAxis
        axis = get_axis(self.controller, axis)

        if gui:
            axis = self.map_value(float(axis), 0, self.top, 0, self.gui_trigger_limit)

        return axis

    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

