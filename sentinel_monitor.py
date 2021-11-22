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


def read_history(sensor):
    # https://stackoverflow.com/questions/33858989/how-to-read-a-csv-into-a-dictionary-in-python
    with open('sentinel.csv', newline='') as histfile:
        reader = csv.reader(histfile)
        next(reader)
        results = dict(reader)  # pull in each row as a key-value pair

    for key, val_live, val_diff, val_like, val_freq in results.items():
        if key == sensor:
            print(key)
            return val_live, val_diff, val_like, val_freq

    return None, None, None, None


def write_to_history(sensor, live, diff, like, frequency):
    # https://pythonspot.com/save-a-dictionary-to-a-file/
    with open('sentinel.csv', newline='') as histfile:
        reader = csv.reader(histfile)
        next(reader)
        results = dict(reader)  # pull in each row as a key-value pair

    for key, val_live, val_diff, val_like, val_freq in results.items():
        if key == sensor:
            val_live = live
            val_diff = diff
            val_like = like
            val_freq = frequency

    # open file for writing, "w" is writing
    w = csv.writer(open("sentinel.csv", "w"))

    # loop over dictionary keys and values
    for key, val_live, val_diff, val_like, val_freq in results.items():
        # write every key and value to file
        w.writerow([key, val_live, val_diff, val_like, val_freq])


def new_policy(old_policy):
    #curr_policy = old_policy.split(" ")

    if old_policy == 1:
        new_policy == 5
    elif old_policy == 5:
        new_policy == 30
    elif old_policy == 30:
        new_policy == 60
    elif old_policy == 60:
        new_policy == 300
    elif old_policy == 300:
        new_policy == 1440
    else:
        new_policy == -1

    if new_policy == 1:
        policy = '* * * * *'
    elif new_policy == 5:
        policy = '/5 * * * *'
    elif new_policy == 30:
        policy = '/30 * * * *'
    elif new_policy == 60:
        policy = '0 * * * *'
    elif new_policy == 300:
        policy = '* /5 * * *'
    elif new_policy == 1440:
        policy = '0 0 * * *'
    else:
        policy == '-1'

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


def monitor_liveness(sensor, isAble):
    switch = False
    like = 5  # max check atm is 5 times
    policy = None
    isLive = check_liveness(sensor)
    wasLive, wasDiff, wasLike, wasRead = read_history(sensor)

    if isLive and isAble:
        pass
    elif isLive and not isAble:
        switch = True
        # delayed change
        #like = 0
    elif not isLive and isAble:
        # simple policy
        switch = True
        # delayed change
        #switch = change_status(wasLive, wasLike)
        #like += like
        # gradual change
        policy, policy_in_min = new_policy(wasRead)
    else:
        pass

    write_to_history(sensor, isLive ^ switch, None, like, policy_in_min)
    return switch, policy
