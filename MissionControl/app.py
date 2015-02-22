# Main application for Mission Control

import serial, os

incoming_COM = 'COM4'
outgoing_COM = 'COM8'

# Vortex Settings
vCOM = COM2
vBaud = 38600
vBits = serial.STOPBITS_TWO

#Setup serial port
ser = serial.Serial(port=outgoing_COM, baudrate=9600, stopbits=serial.STOPBITS_TWO)


is_running = True

while(is_running):
	ser.write(ser.read())
