#!/usr/bin/env python

import time
import datetime

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


# Main function
if __name__ == "__main__":
    datetime_string = "Timestamp: {} {}".format(date_today(), time_now())
    print(datetime_string)
