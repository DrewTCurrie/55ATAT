import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:X%i7us7tCMg9bmKQp&9rD&@127.0.0.1/PTCBozeman")
Base = declarative_base()

class Attendee(Base):
    __tablename__ = 'Attendees'
    ID = sqlalchemy.Column(sqlalchemy.String(length=24), primary_key =True)
    Client = sqlalchemy.Column(sqlalchemy.Boolean, default =False)
    Employee = sqlalchemy.Column(sqlalchemy.Boolean, default =False)
    ABA_Earlychildhood = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    ABA_Teen = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Occupational_Therapy = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Speech_Therapy = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Administrator = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    Employee_SPOT = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Employee_BCBA = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Employee_RBT = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Employee_Other = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    AttendeeInitials = sqlalchemy.Column(sqlalchemy.String(length=6))


class Admininstrator(Base):
        __tablename__ = 'Administrators'
        ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        UserName = sqlalchemy.Column(sqlalchemy.String(length=32))
        Password = sqlalchemy.Column(sqlalchemy.String(length=32))


class AttendanceEvent(Base):
      __tablename__ = 'CurrentAttendanceEvents'
      EventUUID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
      ID = sqlalchemy.Column(sqlalchemy.String(length = 24))
      AttendeeInitials = sqlalchemy.Column(sqlalchemy.String(length=6))
      Timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP, default=datetime.now())
      Absent = sqlalchemy.Column(sqlalchemy.Boolean, default = False)
      TIL_Violation = sqlalchemy.Column(sqlalchemy.Integer, default = 0)
      AdminInitials = sqlalchemy.Column(sqlalchemy.String(length=6))
      Comment = sqlalchemy.Column(sqlalchemy.String(length=256))

class ArchivalEvent(Base):
      __tablename__ = 'ArchivalEvents'
      EventUUID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
      ID = sqlalchemy.Column(sqlalchemy.String(length = 24))
      AttendeeInitials = sqlalchemy.Column(sqlalchemy.String(length=6))
      Timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP, default=datetime.now())
      Absent = sqlalchemy.Column(sqlalchemy.Boolean, default = False)
      TIL_Violation = sqlalchemy.Column(sqlalchemy.Integer, default = 0)
      AdminInitials = sqlalchemy.Column(sqlalchemy.String(length=6))
      Comment = sqlalchemy.Column(sqlalchemy.String(length=256))
