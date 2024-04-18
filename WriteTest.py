import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import sys
import uuid
from datetime import datetime

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://Drew:AMDr0cks@127.0.0.1/PTCBozeman")
Base = declarative_base()


class AttendanceEvent(Base):
      __tablename__ = 'CurrentAttendanceEvents'
      EventUUID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
      ID = sqlalchemy.Column(sqlalchemy.Integer)
      AttendeeInitials = sqlalchemy.Column(sqlalchemy.String(length=6))
      Timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP, default=datetime.now())


def main():
    Base.metadata.create_all(engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    Session = Session()
    
    EventID = uuid.uuid4()
    NewEvent = AttendanceEvent(EventUUID = str(EventID), ID = "9121272", AttendeeInitials = "DrCu1")
    Session.add(NewEvent)
    Session.commit()

if __name__ == '__main__':
        sys.exit(main())