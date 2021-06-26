# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 21:08:04 2021

@author: mpaquette
"""
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr

class EmailSenderClass:
    
    def __init__(self):
        """ """
        self.logaddr = "maxime.fm.paquette@gmail.com"
        self.fromaddr = "Marla Singer"# alias
        self.password = "dgrp bgyu tkyl mhil"#
        
        self.email_html="""<html>
                  <head>
                  </head>
                  <body>
                    <p style ="margin: 5px 0;line-height: 25px;">Hi {},<br>
                    <br>
                    {}
                    <br>
                    <br>
                    kiss,<br>
                    {} <br>
                    </p>
                  </body>
                </html>
                """
        
    def sendMessageViaServer(self,toaddr,msg):
        # Send the message via local SMTP server.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.logaddr, self.password)
        text = msg.as_string()
        server.sendmail(self.fromaddr, toaddr, text)
        server.quit()
            
                
    def sendHtmlEmailTo(self,destName,destinationAddress,msgBody,subject):
        #Message setup
        msg = MIMEMultipart()
         
        msg['From'] =  "Me<"+self.fromaddr+">"
        msg['To'] = destinationAddress
        msg['Subject'] = subject
        
        #hostname=sys.platform
        hostname = "S. Marla"
        
            
        txt = self.email_html
        
        txt=txt.format(destName,msgBody,hostname)
        
        #Add text to message
        msg.attach(MIMEText(txt, 'html'))
        
        print("Send email from {} to {}".format(self.fromaddr,destinationAddress))
        self.sendMessageViaServer(destinationAddress,msg)


def mail_sender(to_name,to_mail,msgbody,subject):

    email= EmailSenderClass()
    email.sendHtmlEmailTo(to_name,to_mail,msgbody,subject)
    