#!/usr/bin/env python

import sys
from orchards_time import time_now
# https://www.seeedstudio.com/blog/2020/01/08/what-is-a-light-sensor-types-uses-arduino-guide/
# https://docs.microsoft.com/en-us/windows/win32/sensorsapi/understanding-and-interpreting-lux-values


def grove_read():
    from grove_light_sensor_v1_2 import GroveLightSensor
    # connect to analog pin 0(slot A0)
    pin = 0
    try:
        sensor = GroveLightSensor(pin)
    except:
        print('Error finding light sensor!')
        return -1
    else:
        #print('Detecting light...')
        return sensor.light


if __name__ == '__main__':
    sensor_value = grove_read()
    #tempdata_string = 'Light value: {0} lux'.format(sensor_value)
    tempdata_string = '{},{0}'.format(time_now(), sensor_value)
    print(lightdata_string)
    sys.exit()
