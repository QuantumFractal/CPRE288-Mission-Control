"""User interface examples."""
import sys, os, copy

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
from math import sin, fabs
import sdl2.ext

import gui
import comms
from radar import *
from controller import *
from timer import *
import random
import re

import serial
import vortex_pb2
import struct

WIDTH = 1024   
HEIGHT = 768

# Define some global color constants
WHITE = sdl2.ext.Color(255, 255, 255)
GREY = sdl2.ext.Color(200, 200, 200)
ORANGE = sdl2.ext.Color(231, 144, 96)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)

#COM PORTS
V_COM_IN = 'COM4'
baud = 57600
bytesize = 8
parity = 'None'
read_timeout = 0

def init_gui(factory):
    RESOURCES = sdl2.ext.Resources(__file__, "resources")
    uifactory = sdl2.ext.UIFactory(factory)

    button = uifactory.from_image(sdl2.ext.BUTTON, RESOURCES.get_path("button.bmp"))
    button.position = 50, 50


    ir_off = uifactory.from_image(sdl2.ext.CHECKBUTTON, 
                                        RESOURCES.get_path("button_unselected.png"))
    ir_off.position = 240, 480

    sonar_off = uifactory.from_image(sdl2.ext.CHECKBUTTON, 
                                        RESOURCES.get_path("button_unselected.png"))
    sonar_off.position = 450, 480

    objects_off = uifactory.from_image(sdl2.ext.CHECKBUTTON, 
                                        RESOURCES.get_path("button_unselected.png"))
    objects_off.position = 650, 480

    button.click += gui.onclick
    button.motion += gui.onmotion
    ir_off.click += gui.oncheck
    ir_off.factory = factory

    objects_off.click += gui.oncheck
    objects_off.factory = factory

    sonar_off.click += gui.oncheck
    sonar_off.factory = factory

    return [ir_off, sonar_off, objects_off]

def map_value(x, in_min, in_max, out_min, out_max):
        value = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return max(min(value, out_max), out_min)




def run():
    # You know those from the helloworld.py example.
    # Initialize the video subsystem, create a window and make it visible.
    sdl2.ext.init()
    SDL_Init(SDL_INIT_GAMECONTROLLER)
    SDL_Init(SDL_RENDERER_PRESENTVSYNC)

    if SDL_NumJoysticks() == 0:
        print 'DS4 Not connected!\nTry again!'
        #sys.exit()

    fps_timer = Timer(60)
    fps_counter = Speedometer()

    window = sdl2.ext.Window("Mission Control", size=(WIDTH, HEIGHT))
    RESOURCES = sdl2.ext.Resources(__file__, "resources")

    SDL_SetWindowIcon(window.window, sdl2.ext.image.load_image(RESOURCES.get_path('icon.png')))
    elite_font = sdl2.ext.FontManager('resources/eurostile.ttf')
    elite_font.color = ORANGE
    
    window.show()

    ticks = 0;

    print("Using hardware acceleration")
    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer,
                                     fontmanager=elite_font)
    

    if "-fullscreen" in sys.argv:
        SDL_SetWindowFullscreen(window.window, SDL_WINDOW_FULLSCREEN)

    label = factory.from_text('Mission Control', size=40)
    label.position = WIDTH/2-label.size[0]/2 , 0

    sonar_button_label = factory.from_text('Sonar Data Toggle', size=16)
    sonar_button_label.position = 115, 487

    ir_button_label = factory.from_text('IR Data Toggle', size=16)
    ir_button_label.position = 350, 487

    object_button_label = factory.from_text('Object Data Toggle', size=16)
    object_button_label.position = 525, 487

    ds4 = ControllerGUI(factory, WIDTH/2-330/2 , 610)
    print SDL_GameControllerName(ds4.controller)
    ds4.update()

    radar = Radar(renderer, x=WIDTH/2-400, y=40, h=400)


    range_val = 20
    ir_data = [200 for x in xrange(90)]
    sonar_data = [200 for x in xrange(90)] 
    radar.set_data(sonar_data, sensor_type='sonar')
    radar.set_data(ir_data, sensor_type='ir')

    spriterenderer = factory.create_sprite_render_system(window)
    uiprocessor = sdl2.ext.UIProcessor()

    sprites = []
    sprites.extend([label, ir_button_label, sonar_button_label, object_button_label])

    ui_elements = init_gui(factory)
    sprites = tuple(ui_elements + ds4.sprites + sprites)

    port = serial.Serial(V_COM_IN, baudrate=baud, timeout=read_timeout, stopbits=serial.STOPBITS_TWO)
    SDL_SetWindowTitle(window.window, "Connected!")
    last_command = ''
    command = ''

    data_buffer = ''

    TANK_DRIVE = False
    """ Main Render Loop """
    running = True
    while running:
        renderer.clear(BLACK)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_ESCAPE:
                    running = False
                if event.key.keysym.sym == SDLK_c:
                    radar.clear_obstacles()
                break

            # Pass the SDL2 events to the UIProcessor, which takes care of
            # the user interface logic.
            uiprocessor.dispatch(ui_elements, event)


        # Render all user interface elements on the window.
        ds4.update()
        radar.draw()

        if TANK_DRIVE == True:
            if ds4.sticks['r_trigger'][0] is not 0:
                MAX_SPEED = 500
            else:
                MAX_SPEED = 250
            left_speed = map_value(-1*ds4.sticks['left'][0][1], 0, 32767, 0, MAX_SPEED)
            right_speed = map_value(-1*ds4.sticks['right'][0][1], 0, 32767, 0, MAX_SPEED)
            command = 'MOV '+str(left_speed)+' '+str(right_speed)+' 90\r'

            
            if ticks % 2:
                port.write(command)

            if ds4.buttons['cross']:
                print 'STOP'
                port.write('`')

        else:
            # CAR DRIVE MODE
            MAX_SPEED = 500
            MAX_SPEED = map_value(ds4.sticks['r_trigger'][0]-ds4.sticks['l_trigger'][0], -32767, 32767, -1*MAX_SPEED, MAX_SPEED)

            #print ds4.sticks['left'][0]

            turret = map_value(ds4.sticks['left'][0][0]*-1, -32767, 32767, 0, 180)
            left_steering = map_value(ds4.sticks['right'][0][0], 0,-1*32767, 1, 100)
            right_steering = map_value(ds4.sticks['right'][0][0], 0, 32767, 1, 100)

            left_speed = MAX_SPEED/left_steering
            right_speed = MAX_SPEED/right_steering
            command = 'MOV '+str(left_speed)+' '+str(right_speed)+' '+str(turret)+'\r'

            
            if ticks % 2:
                port.write(command)

            if ds4.buttons['cross']:
                print 'STOP'
                port.write('`')


        # Given a message like:
        # "degree, ir, sonar"
        # "0, 230, 400"
        data_buffer += port.readline()

        if '\n' in data_buffer:
            data_buffer = data_buffer.rstrip()

            if 'DATA' in data_buffer:  
                data = data_buffer.split(',')
                index = int(data[1])
                ir_data[index] = int(data[2])
                sonar_data[index] = int(data[3])

                if index is 0:
                    ir_data = [200 for x in xrange(90)]
                    sonar_data = [200 for x in xrange(90)]

                radar.set_data(ir_data, sensor_type='ir')    
                radar.set_data(sonar_data, sensor_type='sonar')
            
            if 'OBJ' in data_buffer:

                data = data_buffer.split(',')
                width = float(data[1])
                dist = int(data[2])
                angle = int(data[3])
                print 'I found an object ',width,' cm wide at ',angle,' and ',dist,' far away!'
                radar.add_obstacle(dist, angle, width/2)


            data_buffer = ''
        

       

        radar.ir_visible = not ui_elements[1].checked
        radar.sonar_visible = not ui_elements[0].checked
        radar.objects_visible = not ui_elements[2].checked

        #sdl2.ext.fill(spriterenderer.surface, BLACK)
        spriterenderer.render(sprites)
        #render(sprites, renderer)

        ticks+=1
        last_command = command;
        fps_timer.tick()


    sdl2.ext.quit()
    return 0


def render(sprites, renderer):
    r = SDL_Rect()
    dorender = SDL_RenderCopy
    renderer.clear(BLACK)

    for sprite in sprites:
        r.x = int(sprite.x)
        r.y = int(sprite.y)
        r.w, r.h = sprite.size

        if not sprite.hidden:
            dorender(renderer.renderer, sprite.texture, None, r)

    renderer.present()

if __name__ == "__main__":
    sys.exit(run())
