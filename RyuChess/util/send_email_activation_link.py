import smtplib

from email.message import EmailMessage

message = EmailMessage()
message.set_content('Please click on the link to activate your account')

me = 'harshit11541@gmail.com'
you = 'harshit11541@gmail.com'

message['Subject'] = 'Welcome To RyChess'
message['From'] = me
message['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost:8001')
s.send_message(message)
s.quit()