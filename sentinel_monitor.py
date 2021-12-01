# Monitor sensor variation, battery level and user directives txt and generate energy policy
import csv
import os

sensor_list = ['time', 'light', 'moist', 'temp', 'hum', 'pres']
dir_name = 'SA01-2021-11-21'
file_list = ['timestamp.log', 'lightdata.log',
             'moistdata.log', 'tempdata.log', 'humdata.log', 'presdata.log']
live_list = ['time', -1, -1, -1,  -1, -1]
diff_list = [0, 0, 0, 0, 0, 0]
history_file = 'sentinel.csv'


def read_data(datafile):
    datapath = '{}/{}'.format(dir_name, datafile)
    print(datapath)
    with open(datapath, 'r') as f:
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
    datapath = '{}/{}'.format(dir_name, datafile)
    with open(datapath, 'r') as f:
        rows = csv.reader(f)
        data = 0
        for row in rows:
            data = float(row[1])  # len and [][] didn't work
        return data


def read_history(sensor):
    # https://stackoverflow.com/questions/33858989/how-to-read-a-csv-into-a-dictionary-in-python
    if not os.stat(history_file).st_size == 0:
        with open(history_file, newline='') as histfile:
            reader = csv.reader(histfile)
            # next(reader)
            results = list(reader)  # pull in each row as a key-value pair

        for val in results:
            if val[0] == sensor:
                return val[1], val[2], val[3], val[4]

    return None, None, None, None


def write_to_history(sensor, live, diff, like, frequency):
    # https://pythonspot.com/save-a-dictionary-to-a-file/
    if not os.stat(history_file).st_size == 0:
        with open(history_file, newline='') as histfile:
            reader = csv.reader(histfile)
            # next(reader)
            results = list(reader)  # pull in each row as a key-value pair

        if_found = False
        for item in results:
            if item[0] == sensor:
                item[1] = live
                item[2] = diff
                item[3] = like
                item[4] = frequency
                if_found = True

        if not if_found:
            results.append([sensor, live, diff, like, frequency])

    else:
        results = [[sensor, live, diff, like, frequency]]

    # open file for writing, "w" is writing
    w = csv.writer(open(history_file, "w"))

    # loop over dictionary keys and values
    for val in results:
        # write every key and value to file
        w.writerow([val[0], val[1], val[2], val[3], val[4]])


def new_policy(old_policy):
    #curr_policy = old_policy.split(" ")

    if old_policy == '1':
        new_policy = 5
    elif old_policy == '5':
        new_policy = 30
    elif old_policy == '30':
        new_policy = 60
    elif old_policy == '60':
        new_policy = 300
    elif old_policy == '300':
        new_policy = 1440
    elif old_policy == '1440':
        new_policy = -1
    else:
        new_policy = 1

    if new_policy == 1:
        policy = '* * * * *'
    elif new_policy == 5:
        policy = '*/5 * * * *'
    elif new_policy == 30:
        policy = '*/30 * * * *'
    elif new_policy == 60:
        policy = '0 * * * *'
    elif new_policy == 300:
        policy = '* */5 * * *'
    elif new_policy == 1440:
        policy = '0 0 * * *'
    else:
        policy = '-1'

    return policy, new_policy


def change_status():
    pass


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


def monitor_liveness(sensor, isAble, rate):
    toggle = False
    like = 5  # max check atm is 5 times
    policy = None
    isLive = check_liveness(sensor)
    wasLive, wasDiff, wasLike, wasRead = read_history(sensor)
    policy_in_min = 1 if wasRead is None else wasRead

    if isLive and isAble:
        pass
    elif isLive and not isAble:
        toggle = True
        if rate == 'delayed':
            like = 0
    elif not isLive and isAble:
        if rate == 'simple':
            toggle = True
        elif rate == 'delayed':
            toggle = change_status(wasLive, wasLike)
            like += like
        else:  # 'gradual'
            policy, policy_in_min = new_policy(wasRead)
    else:
        pass

    write_to_history(sensor, isLive ^ toggle, None, like, policy_in_min)
    return toggle, policy


def monitor_diffness(sensor, isAble, rate):
    toggle = False
    like = 5  # max check atm is 5 times
    policy = None
    isDiff = check_diffness(sensor)
    wasLive, wasDiff, wasLike, wasRead = read_history(sensor)
    policy_in_min = 1 if wasRead is None else wasRead

    if isDiff and isAble:
        pass
    elif isDiff and not isAble:
        toggle = True
        if rate == 'delayed':
            like = 0
    elif not isDiff and isAble:
        if rate == 'simple':
            toggle = True
        elif rate == 'delayed':
            toggle = change_status(wasDiff, wasLike)
            like += like
        else:  # 'gradual'
            policy, policy_in_min = new_policy(wasRead)
    else:
        pass

    write_to_history(sensor, isDiff ^ toggle, None, like, policy_in_min)
    return toggle, policy
