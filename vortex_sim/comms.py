""" Communication file """

import serial
import vortex_pb2
import random
import struct

def send_message(port, message):
    s = message.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    port.write(packed_len + s)

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