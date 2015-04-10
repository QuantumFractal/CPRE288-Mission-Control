'''
Bluetooth 57600
38400 speed (baud)
8 Data bits
No Parity
2 Stop bits
No flow control
'''

import serial
import vortex_pb2
import random
import struct
import sys
from math import fabs, degrees

V_COM_OUT = 'COM7'
baud = 57600
bytesize = 8
parity = 'None'


""" Sonar sensor is good at getting precise distances
    
    Ir sensor is good at getting sharp edges

    Basically, use IR to determine object width
    and use PING))) to determine distance
"""

def run():
    port = serial.Serial(V_COM_OUT, baudrate=baud, writeTimeout=8, stopbits=serial.STOPBITS_TWO)
    #port.write('Hello!\n\r')

    send_data = vortex_pb2.sensor_data()
    send_data.timestamp = 123

    #range_val = int(sys.argv[1])
    
    #random_data = [random.randint(fabs(108-range_val), 100+range_val) for x in xrange(90)]
    
    range_val = 20
    data = [random.randint(fabs(108-range_val), 100+range_val) for x in xrange(90)]

    add_object(data, 6.6, 60, 120) 
    add_object(data, 9.2, 70, 60)   

    for x,pt in enumerate(data):
        data_string = str(x)+','+str(pt)+','+str(pt-10)+'\n'
        port.write(data_string)

def detect_objects(array, range, slope):
    # Algorithm for detecting objects
    on_object = False

    for i in xrange(1, len(array)):
        m = (array[i]-array[i-1])/2
        
        if m < -1*slope:
            print "Found Falling Edge"
            on_object = True

        if m > slope:
            print "Found Rising Edge"
            on_object = False   

        #print on_object

def add_object(array, size, distance, angle):
    # Calculate angle range
    range = degrees((size)/distance)
    range = rnd(range/2)

    angle = rnd(angle/2)

    for x in xrange(angle-range, angle+range):
        array[x] = distance


def send_message(port, message):
    s = message.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    serial_string = packed_len + s

    port.write(serial_string)
    return serial_string


def rnd(float):
    return int(round(float))


if __name__ == '__main__':
    run()