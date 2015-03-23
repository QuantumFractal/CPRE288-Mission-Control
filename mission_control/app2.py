"""User interface examples."""
import sys, os, copy

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.sdlgfx as gfx

from math import sin, fabs
import sdl2.ext
import random

import gui
from controller import *
from timer import *
from radar import *

WIDTH = 1024   
HEIGHT = 768

# Define some global color constants
WHITE = sdl2.ext.Color(255, 255, 255)
GREY = sdl2.ext.Color(200, 200, 200)
ORANGE = sdl2.ext.Color(212, 104, 45)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)


def run():
    # You know those from the helloworld.py example.
    # Initialize the video subsystem, create a window and make it visible.
    sdl2.ext.init()
    SDL_Init(SDL_INIT_GAMECONTROLLER)
    SDL_Init(SDL_RENDERER_PRESENTVSYNC)

    if SDL_NumJoysticks() == 0:
        print 'DS4 Not connected!\nTry again!'
        sys.exit()

    fps_timer = Timer(60)
    fps_counter = Speedometer()

    window = sdl2.ext.Window("Connecting...", size=(WIDTH, HEIGHT))
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
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE, fontmanager=elite_font)

    if "-fullscreen" in sys.argv:
        SDL_SetWindowFullscreen(window.window, SDL_WINDOW_FULLSCREEN)

    label = factory.from_text('Mission Control', size=40)
    label.position = WIDTH/2-label.size[0]/2 , 0

    spriterenderer = factory.create_sprite_render_system(window)
    uiprocessor = sdl2.ext.UIProcessor()

    ds4 = ControllerGUI(factory, x=350, y=600)


    sprites = []
    sprites.append(label)
    sprites += tuple(ds4.sprites)

    radar = Radar(renderer, x=WIDTH/2-400, y=40, h=400)

    radar.set_data([random.randint(8,200) for x in xrange(90)], 'ir')
    #radar.set_data([100 for x in range(90)], 'sonar')


    range_val = 100
    last_range = range_val
    ticks = 0

    running = True
    while running:

        if ticks % 100 == 0:
            radar.set_data([random.randint(fabs(108-range_val), 100+range_val) for x in xrange(90)], 'ir')

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
       	ds4.update()

        if ds4.buttons['dpad-up']:
            range_val += 10

        if ds4.buttons['dpad-down']:
            range_val -= 10

        #sdl2.ext.fill(spriterenderer.surface, BLACK)
        radar.draw()
        spriterenderer.render(sprites)

        #renderer.present()
        #render(sprites, renderer)
    
        renderer.present()

        fps_timer.tick()

        last_range = range_val
        ticks+=1

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())
