#!/usr/bin/env python

import sys
import os
from orchards_time import time_now
import time

EXAGGERATE = False
SECURITY = False
GPS = [42.514419, -76.467538]
DIFF_GPS = [42.444125, -76.462797]
# https://learn.adafruit.com/adafruit-ultimate-gps/circuitpython-parsing


def ultimate_uart():

    import serial
    import pynmea2
    # while True:
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()
    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)
        print(gps)
        return [lat, lng]


def gps_read():
    return GPS
    # return ultimate_uart()


def diff_read():
    return DIFF_GPS


def grove_read():
    return gps_read()


def grove_read_mean(times):
    gps_first = grove_read()
    for i in range(times):
        gps_drop = grove_read()
        time.sleep(0.1)
    return gps_first


if __name__ == '__main__':
    if EXAGGERATE:
        while True:
            sensor_value = grove_read()
            gpsdata_string = 'GPS value: {}:{} %'.format(
                sensor_value[0], sensor_value[1])
            print(gpsdata_string)
            time.sleep(0.1)
    else:
        sensor_value = grove_read_mean(100)
        if SECURITY:
            os.system('sudo optee_example_sign_sensor')
        gpsdata_string = '{},{}:{}'.format(
            time_now(), sensor_value[0], sensor_value[1])
        print(gpsdata_string)
        sys.exit()
