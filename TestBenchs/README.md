# Peachtree Pediatric Therapy Center Attendance Tracking System

## Data Management Sub-System Test Benches

The Data Management Sub-System within the TestBenches folder contains scripts for testing database performance and data collection. These scripts facilitate the creation of test data for evaluating the efficiency and effectiveness of the database structure and management processes.

### Files Included

1. **CreateAttendees.py**: This script generates a specified number of attendees as JSON files based on user input. These JSON files simulate attendee data with random roles.

2. **AttendeeToDatabase.py**: This script utilizes CreateAttendees.py to generate a specified number of attendees and adds them to the "Attendees" table within the "PTCBozeman" MariaDB database structure. This enables the automatic creation of attendees in the database for testing purposes.

