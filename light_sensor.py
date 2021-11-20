#!/usr/bin/env python

import sys
import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor


def read_sensor():
    # connect to analog pin 2(slot A2)
    pin = 2
    try:
        sensor = GroveLightSensor(pin)
    except:
        print('Error finding sensor!')
        return -1
    else:
        print('Detecting light...')
        while True:
            print('Light value: {0}'.format(sensor.light))
            time.sleep(100)


if __name__ == '__main__':
    read_sensor()
    sys.exit()
