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

V_COM_OUT = 'COM8'
baud = 57600
bytesize = 8
parity = 'None'


def run():
    port = serial.Serial(V_COM_OUT, baudrate=baud, writeTimeout=8, stopbits=serial.STOPBITS_TWO)
    #port.write('Hello!\n\r')

    send_data = vortex_pb2.sensor_data()
    send_data.timestamp = 123

    for num in random.sample(range(5,100), 90):
        send_data.ir_data_array.append(num)

    print 'Sensor data: ',send_data.ir_data_array
    
    data_string = send_data.SerializeToString()

    print 'Data Bytes:',len(data_string)
    port.write(str(len(data_string))+'\n')



    bytes_written = port.write(data_string)


    print 'Sent', bytes_written,'bytes'


    #port.write(data_string)

    # with open('out.txt', 'wb') as out_file:
    #     out_file.write(data_string)



def send_message(port, message):
    s = message.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    port.write(packed_len + s)



if __name__ == '__main__':
    run()