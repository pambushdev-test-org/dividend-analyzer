import pandas as pd
import smtplib
import ssl
import os
import logging
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

logging.basicConfig(filename='logs.txt', encoding='utf-8', 
					format='%(asctime)s %(message)s', datefmt='%Y/%m/%d/ %I:%M:%S %p', 
					level=logging.DEBUG)

def send_email_report(data):
	EMAIL_DIR = config('EMAIL_DIR')
	email_txt = open(os.path.join(EMAIL_DIR, 'email_txt.txt')).read()
	email_html = open(os.path.join(EMAIL_DIR, 'email_html.html')).read()

	# Place data as an html table inside the html of email_html. Replacing via placeholder {data}.
	email_html = email_html.replace(r'{data}', data.to_html())

	port = config('PORT')
	password = config('PASS')
	sender = config('SENDER')
	receiver = config('RECEIVER')
	subject = 'Dividend Report'

	# Create a secure SSL context
	context = ssl.create_default_context()

	message = MIMEMultipart('alternative')
	message['Subject'] = subject
	message['From'] = sender
	message['To'] = receiver

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(email_txt, 'plain')
	part2 = MIMEText(email_html, 'html')	

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)
	message.attach(part2)

	try:
		with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
			server.login(sender, password)
			#server.set_debuglevel(1)
			server.sendmail(sender, receiver, message.as_string())
		print('Report successfully emailed to client.', flush=True)
	except Exception as err:
		print('An error occurred while sending the email report.', flush=True)		
		traceback.print_exc()