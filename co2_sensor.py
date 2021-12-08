import sys
import os
from orchards_time import time_now
import time

EXAGGERATE = False
SECURITY = False


def grove_read():
    from grove_light_sensor_v1_2 import GroveLightSensor
    # connect to analog pin 4(slot A4) which is none existent
    pin = 4
    try:
        sensor = GroveLightSensor(pin)
    except:
        #print('Error finding CO2 sensor!')
        return -1
    else:
        #print('Detecting CO2...')
        return -1  # sensor.light


def grove_read_mean(times):
    sum = 0
    for i in range(times):
        sum += grove_read()
        time.sleep(0.1)
    return sum/times


if __name__ == '__main__':
    if EXAGGERATE:
        while True:
            sensor_value = grove_read()
            co2data_string = 'CO2 value: {0} %'.format(sensor_value)
            print(co2data_string)
            time.sleep(0.1)
    else:
        sensor_value = grove_read_mean(100)
        if SECURITY:
            os.system('sudo timeout 5s optee_example_sign_sensor')
        co2data_string = '{},{}'.format(time_now(), sensor_value)
        print(co2data_string)
        sys.exit()
