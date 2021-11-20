#!/usr/bin/env python

import sys


def grove_read():
    from bme_280_sensor import readBME280All

    try:
        temperature, pressure, humidity = readBME280All()
    except:
        print('Error finding pressure sensor!')
        return -1
    else:
        #print('Detecting pressure...')
        return pressure


if __name__ == '__main__':
    sensor_value = grove_read()
    presdata_string = 'Pressure value: {0} hPa'.format(sensor_value)
    print(presdata_string)
    sys.exit()
