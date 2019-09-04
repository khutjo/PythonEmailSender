import smtplib

# Specifying the from and to addresses

fromaddr = 'khutjo0005@gmail.com'
toaddrs  = 'khutjo0001@gmail.com'

# Writing the message (this message will appear in the email)

msg = 'Enter you message here'

# Gmail Login

username = 'khutjo0005@gmail.com'
password = 'nzmveaxumafdbukg'

# Sending the mail  

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)

replyto=’khutjo0005@gmail.com’ # where a reply to will go
sendto='khutjo0001@gmail.com' # list to send to
sendtoShow=’khutjo0005@gmail.com’ # what shows on the email as send to
subject=’Test from pysmtp’ # subject line
content=”Hello, this is a test of the system.\nHows it going\nMe” # content 
# compose the email. probably should use the email python module
mailtext=’From: ‘+replyto+’\nTo: ‘+sendtoShow+’\n’
mailtext=mailtext+’Subject:’+subject+’\n’+content
# send the email
server.sendmail(replyto, sendto, mailtext)


#server.sendmail(fromaddr, toaddrs, msg)
server.quit()