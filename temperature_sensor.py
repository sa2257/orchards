#!/usr/bin/env python

import sys
from orchards_time import time_now, date_today, abs_time
import rsa
import time
from gps_sensor import gps_read, diff_read

TAMPERPROOF = True
EXAGGERATE = False
OLD_TIME = '18:0:0'


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


def grove_read_mean(times):
    sum = 0
    for i in range(times):
        sum += grove_read()
        time.sleep(0.1)
    return sum/times


def signed_read():
    (pubkey, privkey) = rsa.newkeys(512)
    data = grove_read_mean(100)
    gps = gps_read()  # diff_read() #
    time = time_now()  # 'OLD_TIME  #
    value = '{},{},{},{}'.format(data, gps[0], gps[1], time)
    message = value.encode()
    signature = rsa.sign(message, privkey, 'SHA-1')
    # value = '{},{},{},{}'.format(28.5, gps[0], gps[1], time)
    # message = value.encode()
    return message, pubkey, signature


def grove_read():
    from bme_280_sensor import readBME280All

    try:
        temperature, pressure, humidity = readBME280All()
    except:
        #print('Error finding temperature sensor!')
        return -1
    else:
        #print('Detecting temperature...')
        return temperature


def signed_verify(message, key, sign, old_time):
    GPS = gps_read()
    verified = rsa.verify(message, sign, key)
    if verified:
        values = message.decode().split(',')
        # print(values)
        if not (float(values[1]) == float(GPS[0]) and float(values[2]) == float(GPS[1])):
            return values[0], False, old_time
        now = abs_time(date_today(), time_now())
        read = abs_time(date_today(), values[3])
        prior = abs_time(date_today(), old_time)
        if not (read <= now and read > prior):
            return values[0], False, old_time
        # print(values[0])
        return values[0], True, values[3]
    else:
        return 0, False, old_time


if __name__ == '__main__':
    if EXAGGERATE:
        old_time = OLD_TIME
        while True:
            if TAMPERPROOF:
                message, key, sign = signed_read()
                sensor_value, verified, old_time = signed_verify(
                    message, key, sign, old_time)
                if not verified:
                    print('Data failed to verify!')
                    continue
            else:
                sensor_value = grove_read()
            tempdata_string = 'Temperature value: {0} C'.format(sensor_value)
            print(tempdata_string)
            time.sleep(0.1)
    else:
        if TAMPERPROOF:
            old_time = OLD_TIME
            message, key, sign = signed_read()
            sensor_value, verified, old_time = signed_verify(
                message, key, sign, old_time)
            if not verified:
                print('Data failed to verify!')
                sys.exit(-1)
        else:
            sensor_value = grove_read()
        #tempdata_string = 'Temperature value: {0} C'.format(sensor_value)
        tempdata_string = '{},{}'.format(time_now(), sensor_value)
        print(tempdata_string)
        sys.exit()
