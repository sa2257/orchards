#!/usr/bin/env python

import sys
from orchards_time import time_now
import time

EXAGGERATE = False


def grove_read():
    from bme_280_sensor import readBME280All

    try:
        temperature, pressure, humidity = readBME280All()
    except:
        #print('Error finding humidity sensor!')
        return -1
    else:
        #print('Detecting humidity...')
        return humidity


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
            humdata_string = 'Humidity value: {0} %'.format(sensor_value)
            print(humdata_string)
            time.sleep(0.1)
    else:
        sensor_value = grove_read_mean(100)
        #humdata_string = 'Humidity value: {0} %'.format(sensor_value)
        humdata_string = '{},{}'.format(time_now(), sensor_value)
        print(humdata_string)
        sys.exit()
