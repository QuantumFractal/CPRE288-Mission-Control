import sys, os, copy
os.environ["PYSDL2_DLL_PATH"] = "..\env"
from sdl2 import *

class Timer:
    """A timer for games with set-rate FPS."""
    
    def __init__(self,fps):
        if fps == 0: 
            self.tick = self._blank
            return
        self.wait = 1000/fps
        self.nt = SDL_GetTicks()
        SDL_Delay(0)
        
    def _blank(self):
        pass
        
    def tick(self):
        """Wait correct amount of time each frame.  Call this once per frame."""
        self.ct = SDL_GetTicks()
        if self.ct < self.nt:
            SDL_Delay(self.nt-self.ct)
            self.nt+=self.wait
        else: 
            self.nt = SDL_GetTicks()+self.wait

class Speedometer:
    """A timer replacement that returns out FPS once a second.
    
    Attributes:
        fps -- always set to the current FPS

    """
    def __init__(self):
        self.frames = 0
        self.st = SDL_GetTicks()
        self.fps = 0

    def __str__(self):
        return str(self.fps)

    def tick(self):
        """ Call this once per frame."""
        r = None
        self.frames += 1
        self.ct = SDL_GetTicks()
        if (self.ct - self.st) >= 1000: 
            r = self.fps = self.frames
            #print "%s: %d fps"%(self.__class__.__name__,self.fps)
            self.frames = 0
            self.st += 1000
        SDL_Delay(0) #NOTE: not sure why, but you gotta call this now and again
        return r