#!/usr/bin/env python

import sys


def grove_read():
    from bme_280_sensor import readBME280All

    try:
        temperature, pressure, humidity = readBME280All()
    except:
        print('Error finding humidity sensor!')
        return -1
    else:
        #print('Detecting humidity...')
        return humidity


if __name__ == '__main__':
    sensor_value = grove_read()
    humdata_string = 'Humidity value: {0} %'.format(sensor_value)
    print(humdata_string)
    sys.exit()