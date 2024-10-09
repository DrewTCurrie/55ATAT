import sys
import uuid

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:lovering@127.0.0.1/ptctest")
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
    AttendeeInitials = sqlalchemy.Column(sqlalchemy.String(length=256))


class Admininstrator(Base):
        __tablename__ = 'Administrators'
        ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        UserName = sqlalchemy.Column(sqlalchemy.String(length=32))
        Password = sqlalchemy.Column(sqlalchemy.String(length=32))


class AttendanceEvent(Base):
      __tablename__ = 'CurrentAttendanceEvents'
      EventUUID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
      ID = sqlalchemy.Column(sqlalchemy.String(length = 24))
      AttendeeInitials = sqlalchemy.Column(sqlalchemy.String(length=256))
      Timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP, default=datetime.now())
      Absent = sqlalchemy.Column(sqlalchemy.Boolean, default = False)
      TIL_Violation = sqlalchemy.Column(sqlalchemy.Integer, default = 0)
      AdminInitials = sqlalchemy.Column(sqlalchemy.String(length=256))
      Comment = sqlalchemy.Column(sqlalchemy.String(length=256))

def main():
    Base.metadata.create_all(engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    Session = Session()

    EventID = 0
    NewEvent = AttendanceEvent(EventUUID=str(EventID), ID="11111", AttendeeInitials="SaLo1",Timestamp=datetime(2024, 9, 10, 9, 30, 0),Absent=True,AdminInitials="SaLo1",Comment="TestCommnet")
    Session.add(NewEvent)
    Session.commit()


if __name__ == '__main__':
    sys.exit(main())