import smtplib
import random
import string
import pandas
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import *

senderacc="adityamitra5102devacc@gmail.com"
senderpass="DevPassword1"
server='smtp.gmail.com'
port=587

def genOtp():
	characters = string.digits
	password = ''.join(random.choice(characters) for i in range(4))
	return password

def sendEmail(id,otp):
	s = smtplib.SMTP(server,port)
	s.starttls()
	s.login(senderacc, senderpass)
	message = "Subject:Authorization OTP\n\nThe OTP for Authorization is "+otp
	s.sendmail(senderacc, id, message)
	s.quit()
	
def sendEmailLink(id,lnk,ua):
	s = smtplib.SMTP(server,port)
	s.starttls()
	s.login(senderacc, senderpass)
	message = "Subject:Authorization Link\n\nOpen this link from the device you are trying to log in. \n"
	message=message+"If you are not trying to log in, ignore this mail and do not forward it to anyone \n"
	message=message+"Please be sure you recognize this device\n"
	message=message+"Browser: "+ua.browser+"\n"
	message=message+"Platform: "+ua.platform+"\n"
	message=message+lnk
	s.sendmail(senderacc, id, message)
	s.quit()
	
def sendEmailNotifAdd(id,tname,tdate,upl,name):
	s = smtplib.SMTP(server,port)
	s.starttls()
	s.login(senderacc, senderpass)
	message = "Subject:Medical Report Added\n\nTest report: "+tname+" of "+name+" tested on "+tdate+" uploaded by "+upl
	s.sendmail(senderacc, id, message)
	s.quit()
	
def sendLogEmail(k, recid='adityaarghya0@gmail.com'):
	s = smtplib.SMTP(server,port)
	s.starttls()
	s.login(senderacc, senderpass)
	df=pandas.read_csv(io.StringIO(k), sep=",")
	MESSAGE = MIMEMultipart('alternative')
	MESSAGE['subject'] = 'Medical Report Logs'
	MESSAGE['To'] = recid
	MESSAGE['From'] = senderacc
	HTML_BODY = MIMEText(df.to_html(), 'html')
	MESSAGE.attach(HTML_BODY)
	s.sendmail(senderacc, recid, MESSAGE.as_string())
	s.quit()
