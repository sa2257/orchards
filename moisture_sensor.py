#!/usr/bin/env python

import sys
# https://en.wikipedia.org/wiki/Water_content#Soil_moisture_measurement sunction pressure


def grove_read():
    from grove_moisture_sensor import GroveMoistureSensor
    # connect to analog pin 2(slot A2)
    pin = 2
    try:
        sensor = GroveMoistureSensor(pin)
    except:
        print('Error finding moisture sensor!')
        return -1
    else:
        #print('Detecting moisture...')
        return sensor.moisture


if __name__ == '__main__':
    sensor_value = grove_read()
    moistdata_string = 'Moisture value: {0} (-)kPa'.format(sensor_value)
    print(moistdata_string)
    sys.exit()
