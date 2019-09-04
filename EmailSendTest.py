import smtplib
# start talking to the SMTP server for Gmail
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.ehlo()
# now login as my gmail user
username='khutjo0005@gmail.com'
password='nzmveaxumafdbukg'
s.login(username,password)
# the email objects
replyto='khutjo0005@gmail.com' # where a reply to will go
sendto='khutjo0001@gmail.com' # list to send to
sendtoShow='khutjo0005@gmail.com' # what shows on the email as send to
subject='Test from pysmtp' # subject line
content='Hello, this is a test of the system.\nHows it going\nMe' # content 
# compose the email. probably should use the email python module
mailtext='From: '+replyto+'\nTo: '+sendtoShow+'\n'
mailtext=mailtext+'Subject:'+subject+'\n'+content
# send the email
s.sendmail(replyto, sendto, mailtext)
# we’re done
rslt=s.quit()
# print the result
print('Sendmail result=' + str(rslt[1]))