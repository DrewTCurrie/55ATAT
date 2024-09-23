# Peachtree Pediatric Therapy Center Attendance Tracking System

## Introduction

Peachtree Pediatric Therapy Center (PTC) requires an automated attendance tracking system to streamline clinic operations and ensure proper patient care. This README.md provides an overview of the system's objectives, features, implementation details, and constraints.

## Objectives

1. **Accurate Tracking**: Track arrival and departure times of attendees with minimal administrative oversight.
2. **Automated Reporting**: Generate Attendee attendance reports, customizable based on various criteria.
3. **Security and Compliance**: Ensure HIPAA compliance and robust protection of sensitive data.
4. **Reliability**: Provide a reliable system with minimal maintenance requirements.

## Features

### Attendance Tracking
- Attendee account creation with role-based categorization.
- Accurate timestamping of attendance events.
- Ability to handle at least 200 unique attendance events per day.
- Administrator override for attendance event errors.
- Self-triggering attendance events for Attendees.
- Interface for check-in, allowing Attendees to check-in within 1 minute of entering the building.
- Audible and visual notifications for successful and unsuccessful attendance events.
- Tracking of Tarde, Absent, Incomplete, and Late (TAIL) violations. 

### Reporting
- Export attendance records in PTC administrator accepted format.
- Customizable attendance reports based on Attendee ID, Date, Event type, and Attendee Role.
- Automatic creation of attendance reports once a week.
- Real-time creation of reports on administrative requests.
- Monthly attendance records for archival use.

### Security and Compliance
- Physical and digital security measures to protect sensitive data.
- HIPAA compliance including double password protection or physical system securing.
- User consent for data collection and access to their data.
- Encryption of sensitive data at rest and in transit.

## Implementation Details

### Technologies Used
- **Backend**: Python with Flask
- **Frontend**: ReactJS and NodeJS
- **Database**: MariaDB

## Constraints

- HIPAA obligations must be followed.
- Standalone system with minimal maintenance requirements.
- System Prototyping budget not to exceed $300, excluding provided hardware.
- Maintenance should be completable by someone with little technical experience no more than once a week.
