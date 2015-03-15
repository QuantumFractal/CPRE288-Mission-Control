class Input():

    def __init__(self):
        # Initialize subsystem. Check if joystick exists, AND is a GameController.
        # TODO: second controller support. Check for 1st when instantanced.
        SDL_Init(SDL_INIT_GAMECONTROLLER)
        SDL_GameControllerAddMappingsFromFile("resources/mapping.txt")
        self.haptic_available = False
        if SDL_NumJoysticks() > 0:
            if SDL_IsGameController(0) == 1:
                self.controller = SDL_GameControllerOpen(0)
                controllername = str(SDL_GameControllerName(self.controller))
                print("Initialized: " + controllername)
                # Initialize haptics if available.
                if SDL_NumHaptics() > 0:
                    self.haptics = SDL_HapticOpen(0)
                    if SDL_HapticRumbleSupported(self.haptics) > 0:
                        SDL_HapticRumbleInit(self.haptics)
                        self.haptic_available = True
        else:
            print("No game controller found.")

        self.inputs = {"up": 0, "down": 0, "left": 0, "right": 0, "a": 0, "b": 0, "x": 0, "y": 0,
                       "l": 0, "r": 0, "start": 0, "back": 0}

    def rumble(self, intensity, length_ms):
        SDL_HapticRumblePlay(self.haptics, intensity, length_ms)

    def update(self, new_events):
        for event in new_events:
            if event.type == SDL_KEYUP:
                if event.key.keysym.sym == SDLK_z:
                    self.inputs["a"] = 0
                if event.key.keysym.sym == SDLK_x:
                    self.inputs["b"] = 0
                if event.key.keysym.sym == SDLK_c:
                    self.inputs["x"] = 0
                if event.key.keysym.sym == SDLK_v:
                    self.inputs["y"] = 0
                if event.key.keysym.sym == SDLK_ESCAPE:
                    self.inputs["back"] = 0
                if event.key.keysym.sym == SDLK_UP:
                    self.inputs["up"] = 0
                if event.key.keysym.sym == SDLK_DOWN:
                    self.inputs["down"] = 0
                if event.key.keysym.sym == SDLK_LEFT:
                    self.inputs["left"] = 0
                if event.key.keysym.sym == SDLK_RIGHT:
                    self.inputs["right"] = 0
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_z:
                    self.inputs["a"] = 1
                if event.key.keysym.sym == SDLK_x:
                    self.inputs["b"] = 1
                if event.key.keysym.sym == SDLK_c:
                    self.inputs["x"] = 1
                if event.key.keysym.sym == SDLK_v:
                    self.inputs["y"] = 1
                if event.key.keysym.sym == SDLK_ESCAPE:
                    self.inputs["back"] = 1
                if event.key.keysym.sym == SDLK_UP:
                    self.inputs["up"] = 1
                if event.key.keysym.sym == SDLK_DOWN:
                    self.inputs["down"] = 1
                if event.key.keysym.sym == SDLK_LEFT:
                    self.inputs["left"] = 1
                if event.key.keysym.sym == SDLK_RIGHT:
                    self.inputs["right"] = 1

            if event.type == SDL_CONTROLLERBUTTONUP:
                self.inputs["a"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_A)
                self.inputs["b"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_B)
                self.inputs["x"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_X)
                self.inputs["y"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_Y)
                self.inputs["l"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_LEFTSHOULDER)
                self.inputs["r"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_RIGHTSHOULDER)
                self.inputs["back"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_BACK)
                self.inputs["start"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_START)
                self.inputs["up"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_UP)
                self.inputs["down"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_DOWN)
                self.inputs["left"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_LEFT)
                self.inputs["right"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_RIGHT)
            if event.type == SDL_CONTROLLERBUTTONDOWN:
                self.inputs["a"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_A)
                self.inputs["b"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_B)
                self.inputs["x"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_X)
                self.inputs["y"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_Y)
                self.inputs["l"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_LEFTSHOULDER)
                self.inputs["r"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_RIGHTSHOULDER)
                self.inputs["back"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_BACK)
                self.inputs["start"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_START)
                self.inputs["up"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_UP)
                self.inputs["down"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_DOWN)
                self.inputs["left"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_LEFT)
                self.inputs["right"] = SDL_GameControllerGetButton(self.controller, SDL_CONTROLLER_BUTTON_DPAD_RIGHT)
        return self.inputs