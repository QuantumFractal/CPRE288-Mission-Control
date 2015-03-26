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
V_COM_IN = 'COM6'
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

    button.click += gui.onclick
    button.motion += gui.onmotion
    ir_off.click += gui.oncheck
    ir_off.factory = factory

    sonar_off.click += gui.oncheck
    sonar_off.factory = factory

    return [ir_off, sonar_off]


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

    ds4 = ControllerGUI(factory, WIDTH/2-330/2 , 610)
    print SDL_GameControllerName(ds4.controller)
    ds4.update()

    radar = Radar(renderer, x=WIDTH/2-400, y=40, h=400)

    range_val = 20
    radar.set_data([random.randint(fabs(108-range_val), 100+range_val) for x in xrange(90)], sensor_type='sonar')
    radar.set_data([random.randint(fabs(108-range_val), 100+range_val) for x in xrange(90)], sensor_type='ir')

    spriterenderer = factory.create_sprite_render_system(window)
    uiprocessor = sdl2.ext.UIProcessor()

    sprites = []
    sprites.extend([label, ir_button_label, sonar_button_label])

    ui_elements = init_gui(factory)
    sprites = tuple(ui_elements + ds4.sprites + sprites)

    port = serial.Serial(V_COM_IN, baudrate=baud, timeout=read_timeout, stopbits=serial.STOPBITS_TWO)
    SDL_SetWindowTitle(window.window, "Connected!")

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
                break

            # Pass the SDL2 events to the UIProcessor, which takes care of
            # the user interface logic.
            uiprocessor.dispatch(ui_elements, event)


        # Render all user interface elements on the window.
        ds4.update()
        radar.draw()

        data_message = comms.get_message(port, vortex_pb2.sensor_data)
        if data_message is not None:
            #data_message.sonar_data_array
            radar.set_data(data_message.ir_data_array, sensor_type='ir')
            radar.set_data(data_message.sonar_data_array, sensor_type='sonar')

        radar.ir_visible = ui_elements[1].checked
        radar.sonar_visible = ui_elements[0].checked

        #sdl2.ext.fill(spriterenderer.surface, BLACK)
        spriterenderer.render(sprites)
        #render(sprites, renderer)

        

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
