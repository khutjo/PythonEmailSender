#!/usr/bin/python
import smtplib
import time
import socket
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.IN)


# sender email login
username   = 'emmpoweralert@gmail.com'
password   = 'qglhxahvhamuqsjc'
# email formating
toaddrs    = ['khutjo0001@gmail.com', 'khutjo0005@gmail.com']
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
	return msg

def gettime():
	time=datetime.now()
	strdate=time.strftime("%H:%M %d %B %Y")
	return strdate

# Sending the mail  
def sendemail(msg):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(username,password)
		mailtext='From: '+replyto+'\nTo: '+replyto+'\n'
		mailtext=mailtext+'Subject:'+subject+'\n\n'+msg
		#print mailtext
		server.sendmail(replyto, toaddrs, mailtext)
		server.quit()
		return False
	except:
		return True

runstate=False
sendtooutput=False
errorstate=False
alertmsg='null'

#print sendemail("hello khutjo this is a test")

while True:

	if GPIO.input(8)==0 and runstate == True:
		alertmsg = poweroutagemsg(1) + gettime()
		runstate=False
		sendtooutput=True

	if GPIO.input(8)==1 and runstate == False:
		alertmsg = poweroutagemsg(2) + gettime()
		sendtooutput=True
		runstate=True

	if sendtooutput==True:
		print alertmsg
		print "message sent"
		sendtooutput=False
		errorstate=sendemail(alertmsg)

	while errorstate==True:
		print "we have an error", alertmsg
		errorstate=sendemail(alertmsg)
		sleep(5)

sleep(1)
