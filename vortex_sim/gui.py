"""User interface examples."""
import sys, os, copy

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
import sdl2.ext
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
        button.texture, tmpsprite.texture = tmpsprite.texture, button.texture
        del tmpsprite

    else:
        tmpsprite = button.factory.from_image(temp_file.get_path("button_unselected.png"))
        button.texture, tmpsprite.texture = tmpsprite.texture, button.texture
        del tmpsprite

