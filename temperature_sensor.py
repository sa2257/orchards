#!/usr/bin/env python

import sys
from orchards_time import time_now


def gpio_read():
    # Initial the dht device, with data pin connected to:
    # dhtDevice = adafruit_dht.DHT22(board.D4)
    import board
    import adafruit_dht

    # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
    # This may be necessary on a Linux single board computer like the Raspberry Pi,
    # but it will not work in CircuitPython.
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

    except Exception as error:
        dhtDevice.exit()
        raise error


def grove_read():
    from bme_280_sensor import readBME280All

    try:
        temperature, pressure, humidity = readBME280All()
    except:
        print('Error finding temperature sensor!')
        return -1
    else:
        #print('Detecting temperature...')
        return temperature


if __name__ == '__main__':
    sensor_value = grove_read()
    #tempdata_string = 'Temperature value: {0} C'.format(sensor_value)
    tempdata_string = '{},{0}'.format(time_now(), sensor_value)
    print(tempdata_string)
    sys.exit()
