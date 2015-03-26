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

V_COM_OUT = 'COM8'
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
    
    data = [200 for x in xrange(90)]

    add_object(data, 6.6, 60, 120) 
    add_object(data, 9.2, 70, 60)   

    detect_objects(data, 1, 10)

    send_data.sonar_data_array.extend(data)

    #print 'Sensor data: ',send_data.ir_data_array

    data_string = send_data.SerializeToString()

    #print 'Data Bytes:',len(data_string)
    #port.write(str(len(data_string))+'\n')

    send_message(port, send_data)

    #bytes_written = port.write(data_string)


    #print 'Sent', bytes_written,'bytes'


    #port.write(data_string)

    # with open('out.txt', 'wb') as out_file:
    #     out_file.write(data_string)

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


        print on_object

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
    port.write(packed_len + s)


def rnd(float):
    return int(round(float))


if __name__ == '__main__':
    run()