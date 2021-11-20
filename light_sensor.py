#!/usr/bin/env python

import sys


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
    lightdata_string = 'Light value: {0}'.format(sensor_value)
    print(lightdata_string)
    sys.exit()
