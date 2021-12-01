#!/usr/bin/env python

import sys
from orchards_time import time_now
# https://www.seeedstudio.com/blog/2020/01/08/what-is-a-light-sensor-types-uses-arduino-guide/
# https://docs.microsoft.com/en-us/windows/win32/sensorsapi/understanding-and-interpreting-lux-values
import time
import stress

EXAGGERATE = False


def grove_read():
    from grove_light_sensor_v1_2 import GroveLightSensor
    # connect to analog pin 0(slot A0)
    pin = 0
    try:
        sensor = GroveLightSensor(pin)
    except:
        #print('Error finding light sensor!')
        return -1
    else:
        #print('Detecting light...')
        return sensor.light


def grove_read_mean(times):
    sum = 0
    for i in range(times):
        sum += grove_read()
        time.sleep(0.1)
    return sum/times


if __name__ == '__main__':
    if EXAGGERATE:
        # stress.stress() # Run this without waiting for return
        while True:
            sensor_value = grove_read()
            lightdata_string = 'Light value: {0} lux'.format(sensor_value)
            print(lightdata_string)
            time.sleep(60)
    else:
        sensor_value = grove_read_mean(100)
        stress.stress()
        # lightdata_string = 'Light value: {0} lux'.format(sensor_value)
        lightdata_string = '{},{}'.format(time_now(), sensor_value)
        print(lightdata_string)
        sys.exit()
