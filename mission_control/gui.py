"""User interface examples."""
import sys, os, copy

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext
from controller import *
from timer import *

WIDTH = 800
HEIGHT = 600


# Define some global color constants
WHITE = sdl2.ext.Color(255, 255, 255)
GREY = sdl2.ext.Color(200, 200, 200)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)

# A callback for the Button.motion event.
def onmotion(button, event):
    #print("Mouse moves over the button!")
    pass


# A callback for the Button.click event.
def onclick(button, event):
    print("Button was clicked!")


# A callback for the TextEntry.input event.
def oninput(entry, event):
    print("Input received with text '%s'" % event.text.text)
    print("Text on the entry now is '%s'" % entry.text)


# A callback for the TextEntry.edit event.
def onedit(entry, event):
    print("Edit received with text '%s', start '%d', length '%d'" %
          (event.text.text, event.text.start, event.text.length))


def oncheck(button, event):
    temp_file = sdl2.ext.Resources(__file__, "resources")
    if button.checked:
        tmpsprite = button.factory.from_image(temp_file.get_path("button_selected.png"))
        button.surface, tmpsprite.surface = tmpsprite.surface, button.surface
        del tmpsprite

    else:
        tmpsprite = button.factory.from_image(temp_file.get_path("button_unselected.png"))
        button.surface, tmpsprite.surface = tmpsprite.surface, button.surface
        del tmpsprite


def run():
    # You know those from the helloworld.py example.
    # Initialize the video subsystem, create a window and make it visible.
    sdl2.ext.init()
    SDL_Init(SDL_INIT_GAMECONTROLLER)
    SDL_Init(SDL_RENDERER_PRESENTVSYNC)

    fps_timer = Timer(30)
    fps_counter = Speedometer()

    window = sdl2.ext.Window("Mission Control", size=(WIDTH, HEIGHT))
    

    # Create a resource, so we have easy access to the example images.
    RESOURCES = sdl2.ext.Resources(__file__, "resources")

    SDL_SetWindowIcon(window.window, sdl2.ext.image.load_image(RESOURCES.get_path('icon.png')))
    elite_font = sdl2.ext.FontManager('resources/eurostile.ttf')
    window.show()

    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer,
                                         fontmanager=elite_font)
    else:
        print("Using software rendering")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE, fontmanager=elite_font)

    uifactory = sdl2.ext.UIFactory(factory)

    label = factory.from_text('Mission Control', size=40)
    label.position = WIDTH/2-label.size[0]/2 , 0
    #label = uifactory.from_text(sdl2.ext.BUTTON, 'Mission Control')

    button = uifactory.from_image(sdl2.ext.BUTTON, RESOURCES.get_path("button.bmp"))
    button.position = 50, 50


    checkbutton = uifactory.from_image(sdl2.ext.CHECKBUTTON, 
                                        RESOURCES.get_path("button_unselected.png"))
    checkbutton.position = 200, 200

    button.click += onclick
    button.motion += onmotion
    checkbutton.click += oncheck
    checkbutton.factory = factory


    ds4 = ControllerGUI(factory, 240, 300)

    ds4.update()

    spriterenderer = factory.create_sprite_render_system(window)

    uiprocessor = sdl2.ext.UIProcessor()

    sprites = []
    sprites = (label, button, checkbutton) + tuple(ds4.sprites)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            # Pass the SDL2 events to the UIProcessor, which takes care of
            # the user interface logic.
            uiprocessor.dispatch([button, checkbutton], event)


        # Render all user interface elements on the window.
        ds4.update()
        sdl2.ext.fill(spriterenderer.surface, BLACK)
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
