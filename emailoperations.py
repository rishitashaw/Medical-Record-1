import smtplib
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

senderacc="adityamitra5102devacc@gmail.com"
senderpass="DevPassword1"

def genOtp():
	characters = string.digits
	password = ''.join(random.choice(characters) for i in range(4))
	return password

def sendEmail(id,otp):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(senderacc, senderpass)
	message = "Subject:Authorization OTP\n\nThe OTP for Authorization is "+otp
	s.sendmail(senderacc, id, message)
	s.quit()
	
def sendEmailNotifAdd(id,tname,tdate,upl,name):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(senderacc, senderpass)
	message = "Subject:Medical Report Added\n\nTest report: "+tname+" of "+name+" tested on "+tdate+" uploaded by "+upl
	s.sendmail(senderacc, id, message)
	s.quit()
	
def sendLogEmail(k):
	id='adityaarghya0@gmail.com'
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(senderacc, senderpass)
	msg = MIMEMultipart()
	msg['Subject'] = '[Email Test]'
	msg['From'] = sender_email
	msg['To'] = receiver_email
	msgText = MIMEText('<b>%s</b>' % (body), 'html')
	msg.attach(msgText)
	lg=MIMEText(k)
	lg.add_header('Content-Disposition', 'attachment', filename="log.csv")
	msg.attach(MIMEText(lg))
	s.sendmail(senderacc, id, msg.as_string())
