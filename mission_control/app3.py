"""User interface examples."""
import sys, os, copy

#setup sdl
os.environ["PYSDL2_DLL_PATH"] = "..\env"

from sdl2 import *
from math import sin, fabs
import sdl2.ext

import gui, comms, sim
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
DANK_GREY = sdl2.ext.Color(50,50,50)
ORANGE = sdl2.ext.Color(231, 144, 96)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLACK = sdl2.ext.Color(0, 0, 0)

#COM PORTS
V_COM_IN = 'COM15'
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
                                        RESOURCES.get_path("button_selected.png"))
    ir_off.position = 270, 640
    ir_off.checked = True

    sonar_off = uifactory.from_image(sdl2.ext.CHECKBUTTON, 
                                        RESOURCES.get_path("button_selected.png"))
    sonar_off.position = 270, 680
    sonar_off.checked = True

    objects_off = uifactory.from_image(sdl2.ext.CHECKBUTTON, 
                                        RESOURCES.get_path("button_unselected.png"))
    objects_off.position = 270, 718

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

def get_color(val):
    pass


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
    voltage = 0;
    charge = 0;

    print("Using hardware acceleration")
    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer,
                                     fontmanager=elite_font)
    
    colors = ['White', 'Red', 'Tile', 'Hole']

    if "-fullscreen" in sys.argv:
        SDL_SetWindowFullscreen(window.window, SDL_WINDOW_FULLSCREEN)


    """
    Initialize Labels for gui
    """
    label = factory.from_text('Mission Control', size=40)
    label.position = WIDTH/2-label.size[0]/2 , 0

    label_tank_mode = factory.from_text('MODE: TANK DRIVE', size=22)
    label_car_mode = factory.from_text('MODE: CAR DRIVE', size=22)

    label_car_mode.position = 780, HEIGHT-50
    label_tank_mode.position = 780, HEIGHT-50

    sonar_button_label = factory.from_text('Sonar Data Toggle', size=16)
    sonar_button_label.position = 145, 645

    ir_button_label = factory.from_text('IR Data Toggle', size=16)
    ir_button_label.position = 145, 685

    object_button_label = factory.from_text('Object Data Toggle', size=16)
    object_button_label.position = 145, 725

    key_label_title = factory.from_text('KEY MAP:', size=16)
    key_label_title.position = 20, 560

    key_line1 = factory.from_text('R: Reset Vector   T: Clear Warnings' , size=16)
    key_line1.position = 20, 580

    key_line2 = factory.from_text('C: Clear Radar     V: Clear Obstacles', size=16)
    key_line2.position = 20, 600


    DANGER = factory.from_text('<<<DANGER: CLIFF>>>', size=50)
    DANGER_WALL = factory.from_text('<<<DANGER: WALL>>>',size=50)
    DANGER_BOULDER = factory.from_text('<<<DANGER: BOULDER>>>',size=50)
    FINISH_MSG = factory.from_text('<<READY FOR PICKUP>>>',size=50)

    DANGER_BOULDER.position =WIDTH/2-250, HEIGHT/2-140
    DANGER_BOULDER.hidden = True
    DANGER_WALL.position =WIDTH/2-250, HEIGHT/2-200
    DANGER_WALL.hidden = True
    DANGER.position = WIDTH/2-250, HEIGHT/2-200
    DANGER.hidden = True
    FINISH_MSG.position = WIDTH/2-250, HEIGHT/2-200
    FINISH_MSG.hidden = True

    """
    Initialize controller, radar
    """
    ds4 = ControllerGUI(factory, WIDTH-320 , 540)

    print SDL_GameControllerName(ds4.controller)
    ds4.update()

    radar = Radar(renderer, x=WIDTH/2-200, y=HEIGHT-250, h=200)


    range_val = 20
    ir_data = [200 for x in xrange(90)]
    sonar_data = [200 for x in xrange(90)] 
    radar.set_data(sonar_data, sensor_type='sonar')
    radar.set_data(ir_data, sensor_type='ir')


    """ 
    SETUP MAP VIEW
    """
    vortex = sim.Vortex(400, 400)
    SCALE = 2
    v_x , v_y = 0,0
    v_angle = 180
    center_x, center_y = WIDTH/2, HEIGHT/2-100
    vortex.x, vortex.y = center_x, center_y
    vortex.rotation = v_angle

    map_gui = sim.MapArea(40,40)

    """
    SETUP RENDERER AND SPRITE LISTS
    """
    spriterenderer = factory.create_sprite_render_system(window)
    uiprocessor = sdl2.ext.UIProcessor()

    sprites = []
    sprites.extend([label, ir_button_label, key_label_title, key_line1, key_line2, sonar_button_label, object_button_label, label_tank_mode, label_car_mode, DANGER, DANGER_WALL, DANGER_BOULDER, FINISH_MSG])

    ui_elements = init_gui(factory)
    sprites = tuple(ui_elements + ds4.sprites + sprites)

    """
    SETUP SERIAL PORT
    """
    try:
        port = serial.Serial(V_COM_IN, baudrate=baud, timeout=read_timeout, stopbits=serial.STOPBITS_TWO)
    except serial.serialutil.SerialException:
       print '\nUSART ERROR TRY AGAIN\n'
       exit()

    SDL_SetWindowTitle(window.window, "Connected!")
    last_command = ''
    command = ''

    # Initialize loop vars
    data_buffer = ''
    last_scan_button = False
    last_drive_state = False
    cliff = False
    wall = False
    boulder = False
    found_finish = False

    trace = list()

    obstacles = list()
    obstacles.append(sim.Boundary(center_x, center_y, True))

    danger = list()

    TANK_DRIVE = False
    """
    Main Render Loop 
    """
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
                    trace = list()

                if event.key.keysym.sym == SDLK_r:
                    vortex.rotation = 180
                    v_angle = 180
                    v_x , v_y = 0,0

                if event.key.keysym.sym == SDLK_t:
                    cliff = False
                    boulder = False
                    wall = False
                    found_finish = False

                if event.key.keysym.sym == SDLK_v:
                    obstacles = list()
                    obstacles.append(sim.Boundary(center_x, center_y, True))
                    danger = list()
                break

            # Pass the SDL2 events to the UIProcessor, which takes care of
            # the user interface logic.
            uiprocessor.dispatch(ui_elements, event)

        # GFX drawing loops 

        map_gui.draw(renderer.renderer)

        """
        MAP DRAWING
        """
        if trace is not ():
            points_x = []
            points_y = []
            for point in trace:
                points_x.append(int(point[0]-v_x))
                points_y.append(int(point[1]-v_y))

            # Do some fancy ctypes magic
            #points_x , points_y = zip(*self.points)
            xptr = (ctypes.c_short * len(points_x))(*points_x)
            yptr = (ctypes.c_short * len(points_x))(*points_y)

            gfx.polygonRGBA(renderer.renderer, xptr, yptr, len(points_x), *RED.rgba )
            gfx.lineRGBA(renderer.renderer, int(center_x-v_x), int(center_y-v_y), int(center_x),int(center_y), *GREY.rgba)

        """
        OBSTACLE DRAWING
        """
        for obstacle in obstacles:
            obstacle.set_offset((-1*v_x,-1*v_y))
            obstacle.draw(renderer.renderer)

        for duh in danger:
            duh.set_offset((-1*v_x,-1*v_y))
            duh.draw(renderer.renderer)

        # Draw Masking
        sim.box(renderer.renderer, 0, 0, 39, HEIGHT,*BLACK.rgba)
        sim.box(renderer.renderer, 0, 0, WIDTH, 39 ,*BLACK.rgba)
        sim.box(renderer.renderer, WIDTH-49, 0, WIDTH, HEIGHT ,*BLACK.rgba)
        sim.box(renderer.renderer, 0, 40+500, WIDTH, HEIGHT,*BLACK.rgba)


        vortex.draw(renderer.renderer)

        # Render all user interface elements on the window.
        ds4.update()
        radar.draw()
        
        sprites[-4].hidden = not cliff
        sprites[-3].hidden = not wall
        sprites[-2].hidden = not boulder
        sprites[-1].hidden = not found_finish

        spriterenderer.render(sprites)

        # Change drive
        if ds4.buttons['circle'] and not last_drive_state:
            TANK_DRIVE = not TANK_DRIVE

        if ds4.buttons['square'] and found_finish and not last_finish_state:
            port.write('%')
            print 'READY FOR PICKUP!'

        last_finish_state = ds4.buttons['square']
        last_drive_state = ds4.buttons['circle']
        label_tank_mode.hidden = not TANK_DRIVE
        label_car_mode.hidden = TANK_DRIVE

        """ 
        SENDING COMMANDS : DRIVING SCANNING ETC
        """
        if TANK_DRIVE:
            if ds4.sticks['r_trigger'][0] is not 0:
                MAX_SPEED = 500
            else:
                MAX_SPEED = 250

            left_speed = map_value(-1*ds4.sticks['left'][0][1], -32767, 32767, -MAX_SPEED, MAX_SPEED)
            right_speed = map_value(-1*ds4.sticks['right'][0][1], -32767, 32767, -MAX_SPEED, MAX_SPEED)
            command = 'MOV '+str(left_speed)+' '+str(right_speed)+' 90\r'
            
            if ticks % 2:
                #print command
                port.write(command)

            button_state = ds4.buttons['triangle']
            if button_state and not last_scan_button:
                #print 'SCAN'
                port.write('#')

            if ds4.buttons['cross']:
                #print 'STOP'
                port.write('`')

            last_scan_button = button_state

        else:
            if ds4.sticks['r_trigger'][0] is not 0:
                MAX_SPEED = 300
            else:
                MAX_SPEED = 100
            #MAX_SPEED = map_value(ds4.sticks['r_trigger'][0]-ds4.sticks['l_trigger'][0], -32767, 32767, MAX_SPEED)

            if fabs(ds4.sticks['right'][0][1]) >= 5000:
                # Only do forward backwards
                left_speed = map_value(-1*ds4.sticks['right'][0][1], -32767, 32767, -MAX_SPEED, MAX_SPEED)
                right_speed = left_speed
                command = 'MOV '+str(left_speed)+' '+str(right_speed)+' '+str(0)+'\r'

            elif ds4.sticks['left'][0][0] is not 0:
                # Only turns
                left_speed = -1*map_value(-1*ds4.sticks['left'][0][0], -32767, 32767, -MAX_SPEED, MAX_SPEED)
                right_speed = -1*left_speed
                command = 'MOV '+str(left_speed)+' '+str(right_speed)+' '+str(0)+'\r'

            else:
                command = 'MOV '+str(0)+' '+str(0)+' '+str(0)+'\r'

            #print ds4.sticks['left'][0]

            turret = map_value(ds4.sticks['left'][0][0]*-1, -32767, 32767, 0, 180)
            left_steering = map_value(ds4.sticks['left'][0][0], 0,-1*32767, 1, 100)
            right_steering = map_value(ds4.sticks['right'][0][1], 0, 32767, 1, 100)

            left_speed = right_steering
            right_speed = right_steering
        
            if ticks % 5 == 0:
                #print command
                port.write(command)

            button_state = ds4.buttons['triangle']
            if button_state and not last_scan_button:
                #print 'SCAN'
                port.write('#')

            if ds4.buttons['cross']:
                print 'STOP'
                port.write('`')

            last_scan_button = button_state

        # Given a message like:
        # "degree, ir, sonar"
        # "0, 230, 400"
        """ 
        GET AND PARSE DATA
        """

        data_buffer += port.readline()


        if '\n' in data_buffer:
            data_buffer = data_buffer.rstrip()
            if 'Error' in data_buffer:
                pass
                #print data_buffer

            

            if 'DATA' in data_buffer:
                if 'DIST' in data_buffer:  
                    data = data_buffer.split(',')
                    index = int(data[2])/2-1
                    ir_data[index] = int(data[3])
                    sonar_data[index] = int(data[4])

                    if index is 0:
                        ir_data = [200 for x in xrange(90)]
                        sonar_data = [200 for x in xrange(90)]

                    radar.set_data(ir_data, sensor_type='ir')    
                    radar.set_data(sonar_data, sensor_type='sonar')
            
                if 'OBJ' in data_buffer:
                    data = data_buffer.split(',')
                    width = float(data[5])*SCALE
                    dist = int(data[4])*1.5*SCALE+width

                    ### CALIBRATION
                    angle = int(data[2])-12
                    print 'I found an object ',width,' cm wide at ',angle,' and ',dist,' far away!'
                    radar.add_obstacle(dist, angle, width/2)

                    x = int(v_x+center_x + dist*sin(radians(v_angle+angle-90)))
                    y = int(v_y+center_y + dist*cos(radians(v_angle+angle-90)))

                    # Add sensor offset distance
                    x += int(12*sin(radians(v_angle)))
                    y += int(12*cos(radians(v_angle)))

                    """ SHOULD BE 7 if SCALE is 1 """
                    if width >= 8.5*SCALE:
                        obstacles.append(sim.Obstacle(x , y))

                    if width < 8.5*SCALE:
                        obstacles.append(sim.GoalPost(x , y))

                if 'POS' in data_buffer:
                    data = data_buffer.split(',')
                    angle = int(data[2])
                    distance = int(data[3])*.8*SCALE

                    v_angle += angle
                    v_y += distance*cos(radians(v_angle))/5.5
                    v_x += distance*sin(radians(v_angle))/5.5

                    trace.append((v_x+center_x, v_y+center_y))
                    
                    #print angle,distance,v_x, v_y, v_angle
                    vortex.rotation = v_angle
                    #vortex.x, shapes[-1].y, shapes[-1].rotation = int(v_x), int(v_y ), int(v_angle)

                if 'BUMPER' in data_buffer:
                    x = int(v_x+center_x)
                    y = int(v_y+center_y)
                    

                    angle_offset = 45 if 'LEFT' in data_buffer else -45 
                    angle_offset = 0 if 'CENTER' in data_buffer else angle_offset

                    x += int(40*SCALE*sin(radians(v_angle+angle_offset)))
                    y += int(40*SCALE*cos(radians(v_angle+angle_offset)))

                    obstacles.append(sim.Boulder(x , y))
                    boulder = True

                if 'FINISHED' in data_buffer:
                    #print 'WE WON!'
                    found_finish = True

                if 'CLIFF' in data_buffer or 'BOUND' in data_buffer:
                    dangerous = 'CLIFF' in data_buffer
                    cliff = dangerous
                    bound = 'BOUND' in data_buffer

                    # Cliff = 1 Bound = 2

                    data = data_buffer.split(',')
                    left = int(data[4])
                    front_left = int(data[2])
                    front_right = int(data[3])
                    right = int(data[5])

                    sensors = [left, front_left, front_right, right]

                    #l;print 'L:',left,'FL:',front_left,'FR:',front_right,'R:',right

                    dangle = danger_angle(sensors, dangerous)

                    x = int(v_x+center_x + 30*SCALE*sin(radians(v_angle+dangle)))
                    y = int(v_y+center_y + 30*SCALE*cos(radians(v_angle+dangle)))

                    v_y -= 35*SCALE*cos(radians(v_angle))/5.5
                    v_x -= 35*SCALE*sin(radians(v_angle))/5.5

                    danger.append(sim.Boundary(x,y, dangerous))


            data_buffer = ''
            
        radar.ir_visible = ui_elements[1].checked
        radar.sonar_visible = ui_elements[0].checked
        radar.objects_visible = ui_elements[2].checked

        #sdl2.ext.fill(spriterenderer.surface, BLACK)
        
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
