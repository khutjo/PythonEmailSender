#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN)
GPIO.setup(16,GPIO.IN)

while True:
	if GPIO.input(16)==1:
		print 'power source 1 active'
	else:
		print 'power source 1 down'
	if GPIO.input(3)==1:
		print 'power source 2 active'
	else:
		print 'power source 2 down'
	time.sleep(1)

