from flask import Flask
from flask_mail import Mail, Message

def SendWeeklyReport(app, mail, fileName):
    print("Sending weekly report!")
    msg = Message(subject='Weekly attendance report', sender='55atatattendance@gmail.com', recipients=['drewcurt6@gmail.com'])
    msg.body = "Weekly report of attendance at PTC"
    with app.open_resource("xlsx/"+fileName, "rb") as ReportFile:
        msg.attach("xlsx/"+fileName, "report/xlsx", ReportFile.read())
    mail.send(msg)


def SendMonthlyReport(app, mail, fileName):
    msg = Message(subject='Monthly attendance report', sender='55atatattendance@gmail.com', recipients=['drewcurt6@gmail.com'])
    msg.body = "Monthly report of attendance at PTC. It is recommended to save this report for archival use. Attendance events older than 2 months are deleted."
    with app.open_resource("xlsx/"+fileName, "rb") as ReportFile:
        msg.attach("xlsx/"+fileName, "report/xlsx", ReportFile.read())
    mail.send(msg)