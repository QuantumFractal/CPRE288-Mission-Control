# Main application for Mission Control

import serial

ser = serial.Serial(port='COM8', baudrate=9600, stopbits=serial.STOPBITS_TWO)

ser.write("Hello!")
