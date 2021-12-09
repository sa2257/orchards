#!/usr/bin/env python

import sys
import os
from orchards_time import time_now
import time

EXAGGERATE = False
SECURITY = False


def grove_read():
    from bme_280_sensor import readBME280All

    try:
        temperature, pressure, humidity = readBME280All()
    except:
        #print('Error finding pressure sensor!')
        return -1
    else:
        #print('Detecting pressure...')
        return pressure


def grove_read_mean(times):
    sum = 0
    for i in range(times):
        sum += grove_read()
        time.sleep(0.01)
    return sum/times


if __name__ == '__main__':
    if EXAGGERATE:
        while True:
            sensor_value = grove_read()
            presdata_string = 'Pressure value: {0} hPa'.format(sensor_value)
            print(presdata_string)
            time.sleep(0.1)
    else:
        sensor_value = grove_read_mean(6000)
        if SECURITY:
            os.system('sudo timeout 5s optee_example_sign_sensor')
        #presdata_string = 'Pressure value: {0} hPa'.format(sensor_value)
        presdata_string = '{},{}'.format(time_now(), sensor_value)
        print(presdata_string)
        sys.exit()
