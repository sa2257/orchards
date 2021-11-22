# Monitor sensor variation, battery level and user directives txt and generate energy policy
import csv

sensor_list = ['time', 'light', 'moist', 'temp', 'hum', 'pres']
file_list = ['data_today/timestamp.log', 'data_today/lightdata.log',
             'data_today/moistdata.log', 'data_today/tempdata.log', 'data_today/humdata.log', 'data_today/presdata.log']
live_list = ['time', 'string', 'string', -1,  -1, -1]
diff_list = [0, 0, 0, 0, 0, 0]


def read_data(datafile):
    with open(datafile, 'r') as f:
        rows = csv.reader(f)
        data = []
        for row in rows:  # reversed didn't work, no did len
            data.append(float(row[1]))
        try:
            avg = sum(data) / len(data)
        except:
            return None
        return avg


def read_item(datafile):
    with open(datafile, 'r') as f:
        rows = csv.reader(f)
        data = 0
        for row in rows:
            data = float(row[1])  # len and [][] didn't work
        return data


def check_liveness(sensor):
    # We hope the sensor is live
    i = sensor_list.index(sensor)
    past = read_data(file_list[i])
    if past == live_list[i]:
        return False
    return True


def check_diffness(sensor):
    # We hope the sensor values are different
    i = sensor_list.index(sensor)
    past = read_data(file_list[i])
    last = read_item(file_list[i])
    if past * (1 - diff_list[i]) < last < past * (1 + diff_list[i]):
        return False
    return True
