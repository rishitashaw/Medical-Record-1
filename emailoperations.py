import smtplib
import random
import string
import pandas
import io
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
	
def sendLogEmail(k, recid='adityaarghya0@gmail.com'):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(senderacc, senderpass)
	df=pandas.read_csv(io.StringIO(k), sep=",")
	MESSAGE = MIMEMultipart('alternative')
	MESSAGE['subject'] = 'Medical Report Logs'
	MESSAGE['To'] = recid
	MESSAGE['From'] = senderacc
	HTML_BODY = MIMEText(df.to_html, 'html')
	MESSAGE.attach(HTML_BODY)
	s.sendmail(senderacc, recid, MESSAGE.as_string())
	s.quit()
