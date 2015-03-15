"""User interface examples."""
import sys, os

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext

# Define some global color constants
WHITE = sdl2.ext.Color(255, 255, 255)
GREY = sdl2.ext.Color(200, 200, 200)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)

# A callback for the Button.motion event.
def onmotion(button, event):
    print("Mouse moves over the button!")


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
        button.texture, tmpsprite.texture = tmpsprite.texture, button.texture
        del tmpsprite

    else:
        tmpsprite = button.factory.from_image(temp_file.get_path("button_unselected.png"))
        button.texture, tmpsprite.texture = tmpsprite.texture, button.texture
        del tmpsprite


def run():
    # You know those from the helloworld.py example.
    # Initialize the video subsystem, create a window and make it visible.
    sdl2.ext.init()
    window = sdl2.ext.Window("Mission Control", size=(800, 600))

    # Create a resource, so we have easy access to the example images.
    RESOURCES = sdl2.ext.Resources(__file__, "resources")

    elite_font = sdl2.ext.FontManager('resources/eurostile.ttf')
    window.show()

    # Create a sprite factory that allows us to create visible 2D elements
    # easily. Depending on what the user chosses, we either create a factory
    # that supports hardware-accelerated sprites or software-based ones.
    # The hardware-accelerated SpriteFactory requres a rendering context
    # (or SDL_Renderer), which will create the underlying textures for us.
    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer,
                                         fontmanager=elite_font)
    else:
        print("Using software rendering")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    # Create a UI factory, which will handle several defaults for
    # us. Also, the UIFactory can utilises software-based UI elements as
    # well as hardware-accelerated ones; this allows us to keep the UI
    # creation code clean.
    uifactory = sdl2.ext.UIFactory(factory)

    label = factory.from_text('Mission Control', size=40)
    #label = uifactory.from_text(sdl2.ext.BUTTON, 'Mission Control')


    # Create a simple Button sprite, which reacts on mouse movements and
    # button presses and fill it with a white color. All UI elements
    # inherit directly from the TextureSprite (for TEXTURE) or SoftwareSprite
    # (for SOFTWARE), so everything you can do with those classes is also
    # possible for the UI elements.
    button = uifactory.from_image(sdl2.ext.BUTTON, RESOURCES.get_path("button.bmp"))
    button.position = 50, 50
    button.scale = 20

    # Create a CheckButton sprite. The CheckButton is a specialised
    # Button, which can switch its state, identified by the 'checked'
    # attribute by clicking.
    checkbutton = uifactory.from_image(sdl2.ext.CHECKBUTTON, 
                                        RESOURCES.get_path("button_unselected.png"))
    checkbutton.position = 200, 200
    checkbutton.size = (20,20)

    # Bind some actions to the button's event handlers. Whenever a click
    # (combination of a mouse button press and mouse button release), the
    # onclick() function will be called.
    # Whenever the mouse moves around in the area occupied by the button, the
    # onmotion() function will be called.
    # The event handlers receive the issuer of the event as first argument
    # (the button is the issuer of that event) and the SDL event data as second
    # argument for further processing, if necessary.
    button.click += onclick
    button.motion += onmotion

    checkbutton.click += oncheck
    checkbutton.factory = factory

    # Since all gui elements are sprites, we can use the
    # SpriteRenderSystem class, we learned about in helloworld.py, to
    # draw them on the Window.
    spriterenderer = factory.create_sprite_render_system(window)

    # Create a new UIProcessor, which will handle the user input events
    # and pass them on to the relevant user interface elements.
    uiprocessor = sdl2.ext.UIProcessor()

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
        render((button, label, checkbutton), renderer)

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

        dorender(renderer.renderer, sprite.texture, None, r)

    renderer.present()

if __name__ == "__main__":
    sys.exit(run())
