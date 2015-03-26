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
import struct

V_COM_IN = 'COM6'
baud = 57600
bytesize = 8
parity = 'None'
read_timeout = 10


def run():

	port = serial.Serial(V_COM_IN, baudrate=baud, timeout=read_timeout, stopbits=serial.STOPBITS_TWO)

	print "Listening..."

	# bytes_to_read = int(port.readline())
	# print 'Reading', bytes_to_read,'bytes'

	# data_string = port.read(bytes_to_read)

	# print 'Read', len(data_string),'bytes'
	# print data_string

	#	sensor_data.ParseFromString(data_string)

	print len(port.read(4))

	#sensor_data = get_message(port, vortex_pb2.sensor_data)


	print sensor_data.ir_data_array[0]


def get_message(port, msgtype):
    """ Read a message from a socket. msgtype is a subclass of
        of protobuf Message.
    """
    len_buf = port.read(4)
    msg_len = struct.unpack('>L', len_buf)[0]
    msg_buf = port.read(msg_len)

    msg = msgtype()
    msg.ParseFromString(msg_buf)
    return msg

if __name__ == '__main__':
	run()