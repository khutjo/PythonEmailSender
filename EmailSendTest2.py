#!/usr/bin/python
import smtplib
import time
import socket
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.IN)
GPIO.setup(3, GPIO.IN)

# sender email login
username   = 'khutjo0005@gmail.com'
password   = 'dbljlhtteuknuuuc'
# email formating
toaddrs    = 'khutjo0001@gmail.com'
replyto    = 'noreply@noreply.com'
subject    = 'Power Alert'

# power outage mesage
# there are three condition 1 and 2 for normal power outage and return
# condition 3 for in case backup power fails

def poweroutagemsg(state):
	if state == 1:
		msg = 'There was a power outage at '
	elif state == 2:
		msg  = 'Power returned at '
	elif state == 3:
		msg = 'Backup power failure at '
	elif state == 4:
		msg = 'Backup power returned at '
	return msg

# Sending the mail  
def sendemail(state):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	content=poweroutagemsg(state)
	times=datetime.now()
	strdate=times.strftime('%H:%M %d %B %Y')
	mailtext='From: '+replyto+'\nTo: '+replyto+'\n'
	mailtext=mailtext+'Subject:'+subject+'\n\n'+content+strdate
	#print mailtext
	server.sendmail(replyto, toaddrs, mailtext)
	server.quit()

def internet(host="8.8.8.8", port=53, timeout=3):
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		print 'we good'
		return True
	except socket.error as ex:
    		print(ex)
		return False

while internet() == False:
	sleep(10)
runstate = False
failure = False

sleep(10)
while True:
	if GPIO.input(16)==0 and runstate == False: 
		print 'Power UP'
		sendemail(2)
		runstate = True
	if GPIO.input(16)==1 and runstate == True:
		print 'Power DOWN'
		sendemail(1)
		runstate = False

	if GPIO.input(3)==0 and failure == False:
		print 'Backup UP'
		sendemail(4)
		failure = True
	if GPIO.input(3)==1 and failure == True:
		print 'Backup BOWN'
		sendemail(3)
		failure = False
	sleep(1)
#sendemail(1)
#	sleep(60)
#sendemail(2)
#	sleep(60)
#	sendemail(3)
