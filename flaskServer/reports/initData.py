# initData - EELE488 Prototype
# Sam Lovering
# Last Updated 4/22/2024
#
# This file creates data for the purpose of prototyping "Generate Report"
#

import json
import string
import random
import datetime


#Creates a date and returns it as a string to create_random_data
def create_date():
    test_date1, test_date2 = datetime.date(2024, 4, 1), datetime.date(2024, 4, 30)
    res_dates = [test_date1]
    # loop to get each date till end date
    while test_date1 != test_date2:
        test_date1 += datetime.timedelta(days=1)
        res_dates.append(test_date1)
    return datetime.date.isoformat(random.choice(res_dates))


#Creates a time and returns it as a string to create_random_data
def create_time():
    test_time1, test_time2 = datetime.time(0, 0, 0), datetime.time(23, 0, 0)
    res_dates = [test_time1]
    # loop to get each date till end date
    while test_time1 != test_time2:
        test_time1 = (
                datetime.datetime.combine(datetime.date(1, 1, 1), test_time1) + datetime.timedelta(minutes=1)).time()
        res_dates.append(test_time1)
    return datetime.time.isoformat(random.choice(res_dates))


#Create an object of JSON data to send pack to xlsxTest
#This is done by creating a nested python dict, then using JSON.dump to convert it.
#Format {EventUUID: { AttendeeID: Initials: Date: Time:}
def create_random_data(max):
    #Create Date List
    test_date1, test_date2 = datetime.date(2024, 4, 1), datetime.date(2024, 4, 30)
    res_dates = [test_date1]
    # loop to get each date till end date
    while test_date1 != test_date2:
        test_date1 += datetime.timedelta(days=1)
        res_dates.append(test_date1)
    #Create Time List
    test_time1, test_time2 = datetime.time(0, 0, 0), datetime.time(23, 0, 0)
    res_times = [test_time1]
    # loop to get each date till end date
    while test_time1 != test_time2:
        test_time1 = (
                datetime.datetime.combine(datetime.date(1, 1, 1), test_time1) + datetime.timedelta(minutes=1)).time()
        res_times.append(test_time1)
    tempTable = {}

    for i in range(max):
        tempId = random.randint(1, 10000000000)
        tempInitials = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        tempDate =datetime.date.isoformat(random.choice(res_dates))
        tempTime = datetime.time.isoformat(random.choice(res_times))
        entry = {'AttendeeID': tempId, 'Initials': tempInitials, 'Date': tempDate, 'Time': tempTime}
        tempTable.update({i: entry})

    jsonData = json.dumps(tempTable)
    return jsonData


def create_manual_data():
    entry1 = {'AttendeeID': "99", 'Initials': "SaLo", "Date": "2024-04-16", 'Time': datetime.time.isoformat(datetime.time(10, 8, 0))}
    entry2 = {'AttendeeID': "1", 'Initials': "AaBb", "Date": "2024-04-17", 'Time': datetime.time.isoformat(datetime.time(11, 8, 0))}
    entry3 = {'AttendeeID': "4", 'Initials': "CcDd", "Date": "2024-04-18", 'Time': datetime.time.isoformat(datetime.time(12, 8, 0))}
    entry4 = {'AttendeeID': "66", 'Initials': "EeFf", "Date": "2024-04-19", 'Time': datetime.time.isoformat(datetime.time(13, 8, 0))}
    entry5 = {'AttendeeID': "55", 'Initials': "TtTt", "Date": "2024-04-20", 'Time': datetime.time.isoformat(datetime.time(14, 8, 0))}
    entry6 = {'AttendeeID': "32", 'Initials': "LlLl", "Date": "2024-04-21", 'Time': datetime.time.isoformat(datetime.time(15, 8, 0))}
    entry7 = {'AttendeeID': "56", 'Initials': "XxXx", "Date": "2024-04-22", 'Time': datetime.time.isoformat(datetime.time(16, 8, 0))}
    entry8 = {'AttendeeID': "98", 'Initials': "YyYy", "Date": "2024-04-23", 'Time': datetime.time.isoformat(datetime.time(17, 8, 0))}
    entry9 = {'AttendeeID': "192", 'Initials': "ZzZz", "Date": "2024-04-24", 'Time': datetime.time.isoformat(datetime.time(18, 8, 0))}
    entry10 = {'AttendeeID': "402", 'Initials': "VvVv", "Date": "2024-04-25", 'Time': datetime.time.isoformat(datetime.time(19, 8, 0))}
    return json.dumps({0: entry1, 1: entry2, 2: entry3, 3: entry4, 4: entry5, 5: entry6, 6: entry7, 7: entry8, 8: entry9,9: entry10})


if __name__ == "__main__":
    print("initData called with __main__")