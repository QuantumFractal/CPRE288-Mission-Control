""" Test receiver """

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

V_COM_IN = 'COM4'
baud = 57600
bytesize = 8
parity = 'None'
read_timeout = 10

port = serial.Serial(V_COM_IN, baudrate=baud, timeout=read_timeout, stopbits=serial.STOPBITS_TWO)

print "Listening..."

bytes_to_read = int(port.readline())
print 'Reading', bytes_to_read,'bytes'

data_string = port.read(bytes_to_read)

print 'Read', len(data_string),'bytes'
print data_string

sensor_data = vortex_pb2.sensor_data()

sensor_data.ParseFromString(data_string)

print sensor_data.ir_data_array