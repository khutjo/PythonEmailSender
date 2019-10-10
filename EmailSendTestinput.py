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

errorcase = False

# power outage mesage
# there are three condition 1 and 2 for normal power outage and return
# condition 3 for in case backup power fails

def poweroutagemsg(state):
	if state == 1:
		msg = 'There was a power outage at '
	elif state == 2:
		msg  = 'Power returned at '
	return msg

def getDateTime():
	times=datetime.now()
	strdate=times.strftime('%H:%M %d %B %Y')
	return strdate

# Sending the mail  
def sendemail(content):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(username,password)
		mailtext='From: '+replyto+'\nTo: '+replyto+'\n'
	        mailtext=mailtext+'Subject:'+subject+'\n\n'+content
		server.sendmail(replyto, toaddrs, mailtext)
		server.quit()
		return True
	except:
		return False

def getInternetCheck(host="8.8.8.8", port=53, timeout=3):
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except socket.error as ex:
		print(ex)
		return False

runstate = False
errortime = ""

def checkbeforesend(caller):
	global errorcase
	global errortime

	msg = poweroutagemsg(caller)
	print  errorcase
	if errorcase == True:
		timestamp = errortime
	else:
		timestamp = getDateTime()
		print msg+timestamp
	themail = sendemail(msg+timestamp)

	print " email sender state "

	print  themail
	if  themail:
        	print("Alert sent")
		errorcase = False
		return True
	else:
		errorcase = True

	if errorcase == True:
		errorcase = True
		errortime = timestamp
		return False

while True:
	print getInternetCheck()
	sendresult = True

	frominput = raw_input("just do it")
	if frominput == "yes" and runstate == False: 
        	print 'Power UP'
	        runstate = True
        	sendresult = checkbeforesend(1)
	if frominput == "no" and runstate == True:
        	print 'Power DOWN'
	        runstate = False
        	sendresult = checkbeforesend(2)
	
	while sendresult == False:
		while getInternetCheck() == False:
			print "retrying"
			sleep(300)
		if runstate == True:
			print "sending a"
			sendresult = checkbeforesend(1)
		if runstate == False:    
			print "sending b"
			sendresult = checkbeforesend(2)
	sleep(1)
