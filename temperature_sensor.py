#!/usr/bin/env python

import time
import sys


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
    from grove_helper import SlotHelper
    from grove_light_sensor_v1_2 import GroveLightSensor
    sh = SlotHelper(SlotHelper.ADC)
    pin = sh.argv2pin()

    sensor = GroveLightSensor(pin)

    print('Detecting light...')
    while True:
        print('Light value: {0}'.format(sensor.light))
        time.sleep(1)


if __name__ == '__main__':
    grove_read()
    sys.exit()
