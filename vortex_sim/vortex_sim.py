"""User interface examples."""
import sys, os, copy

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
from math import sin, fabs
import sdl2.ext

import gui
import sim
from timer import *
import random
import serial
import vortex_pb2
import random
import struct


WIDTH = 600   
HEIGHT = 600

# Define some global color constants
WHITE = sdl2.ext.Color(255, 255, 255)
GREY = sdl2.ext.Color(200, 200, 200)
ORANGE = sdl2.ext.Color(231, 144, 96)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)


def init_gui(factory):
    pass


def run():
    # You know those from the helloworld.py example.
    # Initialize the video subsystem, create a window and make it visible.
    sdl2.ext.init()
    SDL_Init(SDL_INIT_GAMECONTROLLER)
    SDL_Init(SDL_RENDERER_PRESENTVSYNC)

    fps_timer = Timer(60)
    fps_counter = Speedometer()

    window = sdl2.ext.Window("Mission Control", size=(WIDTH, HEIGHT))
    RESOURCES = sdl2.ext.Resources(__file__, "resources")

    SDL_SetWindowIcon(window.window, sdl2.ext.image.load_image(RESOURCES.get_path('icon.png')))
    elite_font = sdl2.ext.FontManager('resources/eurostile.ttf')
    elite_font.color = ORANGE
    
    window.show()

    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer,
                                         fontmanager=elite_font)
    else:
        print("Using software rendering")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE, fontmanager=elite_font)

    if "-fullscreen" in sys.argv:
        SDL_SetWindowFullscreen(window.window, SDL_WINDOW_FULLSCREEN)

    label = factory.from_text('Vortex Simulator', size=16)
    label.position = WIDTH/2-label.size[0]/2 , 0

    spriterenderer = factory.create_sprite_render_system(window)
    uiprocessor = sdl2.ext.UIProcessor()

    sprites = []
    sprites.append(label)

    ui_elements = init_gui(factory)
    sprites = tuple(sprites)


    vortex = sim.Vortex(pos=(300,300))
    dropoff = sim.Dropoff(20, pos=(200,200))

    shapes = (vortex, dropoff)

    ticks = 0
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
            #uiprocessor.dispatch(ui_elements, event)


        # Render all user interface elements on the window.
        #sdl2.ext.fill(spriterenderer.surface, BLACK)

        for shape in shapes:
            shape.draw(renderer.renderer)
        

        spriterenderer.render(sprites)

        #vortex.rotation += 1
        vortex.sensor_rotation = 90.0*sin(ticks/50.0)

        ticks += 1

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
