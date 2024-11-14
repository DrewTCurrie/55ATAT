from flask import Flask
from flask_mail import Mail, Message

def SetupCredentials(app):
    app.config['MAIL_SERVER']= 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = '55atatattendance@gmail.com'
    app.config['MAIL_PASSWORD'] = 'pndi aaii gzsy kark '
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
