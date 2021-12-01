import sys
from orchards_time import time_now
import time

EXAGGERATE = False
GPS = [42.514419, -76.467538]
DIFF_GPS = [42.444125, -76.462797]
# https://learn.adafruit.com/adafruit-ultimate-gps/circuitpython-parsing


def gps_read():
    return GPS


def diff_read():
    return DIFF_GPS


def grove_read():
    return gps_read()


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
            gpsdata_string = 'GPS value: {}:{} %'.format(
                sensor_value[0], sensor_value[1])
            print(gpsdata_string)
            time.sleep(0.1)
    else:
        sensor_value = grove_read_mean(100)
        gpsdata_string = '{},{}:{}'.format(
            time_now(), sensor_value[0], sensor_value[1])
        print(gpsdata_string)
        sys.exit()
