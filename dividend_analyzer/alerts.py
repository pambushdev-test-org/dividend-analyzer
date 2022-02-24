import pandas as pd
import smtplib
import ssl
import logging
import traceback
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import PARENT_DIR, EMAIL_VARS

# Color cells green for positive values and red for negative
def color_cell(cell):
	match cell:
		# Some cells are strings (ticker, timestamp), ignore these
		case cell if type(cell) == str:
			return cell
		case cell if cell > 0:
			return f'<div style="color: green">{cell}</div>'
		case cell if cell < 0:
			return f'<div style="color: red">{cell}</div>'
		case _:
			return f'<div>{cell}</div>'

def send_email_report(data):
	EMAIL_DIR = os.path.join(PARENT_DIR, 'email') # email templates
	email_txt = open(os.path.join(EMAIL_DIR, 'email_txt.txt')).read()
	email_html = open(os.path.join(EMAIL_DIR, 'email_html.html')).read()
	
	# Setup and apply formatting to color cells of report table
	fmt = {}
	for i in data.columns[:]:
		fmt[i] = lambda cell: color_cell(cell)

	# Place data as an html table inside the html of email_html. Replacing via placeholder {data}.
	rendered_data = data.to_html(formatters=fmt, escape=False)
	email_html = email_html.replace(r'{data}', rendered_data)

	port 		= 465
	password 	= EMAIL_VARS['PASS']
	sender 		= EMAIL_VARS['SENDER']
	receiver 	= EMAIL_VARS['RECEIVER']
	subject 	= 'Dividend Report'

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