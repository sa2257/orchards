#!/usr/bin/env python

import sys
from orchards_time import time_now
import time
# https://en.wikipedia.org/wiki/Water_content#Soil_moisture_measurement sunction pressure

EXAGGERATE = False


def grove_read():
    from grove_moisture_sensor import GroveMoistureSensor
    # connect to analog pin 2(slot A2)
    pin = 2
    try:
        sensor = GroveMoistureSensor(pin)
    except:
        #print('Error finding moisture sensor!')
        return -1
    else:
        #print('Detecting moisture...')
        return sensor.moisture


def grove_read_mean(times):
    sum = 0
    for i in range(times):
        sum += grove_read()
        time.sleep(0.1)
    return sum/times


if __name__ == '__main__':
    if EXAGGERATE:
        while True:
            sensor_value = grove_read()
            moistdata_string = 'Moisture value: {0} (-)kPa'.format(
                sensor_value)
            print(moistdata_string)
            time.sleep(55)
    else:
        sensor_value = grove_read()
        #moistdata_string = 'Moisture value: {0} (-)kPa'.format(sensor_value)
        moistdata_string = '{},{}'.format(time_now(), sensor_value)
        print(moistdata_string)
        sys.exit()
