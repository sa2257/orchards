#!/usr/bin/env python

import os
import time
import datetime

EXAGGERATE = False
SECURITY = False

# Return current date


def date_today():
    datetime_object = datetime.datetime.now()
    date_string = "{}-{}-{}".format(datetime_object.year,
                                    datetime_object.month, datetime_object.day)
    return date_string

# Return current time


def time_now():
    datetime_object = datetime.datetime.now()
    time_string = "{}:{}:{}".format(datetime_object.hour,
                                    datetime_object.minute, datetime_object.second)
    return time_string


def abs_time(date, time):
    _date = date.split('-')
    _time = time.split(':')
    abs_days = int(_date[0]) * 365 + int(_date[1]) * 31 + int(_date[2])
    abs_secs = int(_time[0]) * 3600 + int(_time[1]) * 60 + int(_date[2])
    return abs_days * 24 * 3600 + abs_secs


def time_read(times):
    time_first = time_now()
    for i in range(times):
        time_drop = time_now()
        time.sleep(0.01)
    return time_first


# Main function
if __name__ == "__main__":
    if EXAGGERATE:
        while True:
            datetime_string = "Timestamp: {} {}".format(
                date_today(), time_now())
            print(datetime_string)
            time.sleep(0.1)
    else:
        if SECURITY:
            os.system('sudo timeout 5s optee_example_sign_sensor')
        datetime_string = "Timestamp: {} {}".format(
            date_today(), time_read(6000))  # time_now())
        print(datetime_string)
