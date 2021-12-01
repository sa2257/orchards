# Read user directives and app names txt files and generate a crontab file

# Importing the CronTab class from the module
import os
import sys
from crontab import CronTab
# https://pypi.org/project/python-crontab/
from sentinel_monitor import check_liveness, monitor_liveness, check_diffness, monitor_diffness

# Creating an object from the class
# Using the root user
# cron = CronTab(user="pi")

# Optional: Using the current user
cron = CronTab(user=True)

# create commands
local_python = 'python'
super_python = 'python3'
sensor_list = ['light', 'moist', 'temp', 'hum', 'pres', 'gps', 'co2']


def remove_command(command):
    grep_tab = cron.find_command(command)
    for item in grep_tab:
        cron.remove(item)


def reschedule_command(command, frequency):
    grep_tab = cron.find_command(command)
    for item in grep_tab:
        # assign new schedule
        if frequency == '-1':
            item.every_reboot()
        else:
            # item.minute.every(frequency)
            item.setall(frequency)


def is_Able(command):
    grep_tab = cron.find_command(command)
    for item in grep_tab:
        if item.is_enabled():
            return True
    return False


def disable_command(command):
    grep_tab = cron.find_command(command)
    for item in grep_tab:
        if item.is_enabled():
            item.enable(False)


def enable_command(command):
    grep_tab = cron.find_command(command)
    for item in grep_tab:
        if not item.is_enabled():
            item.enable()


def toggle_command(command):
    # https://stackoverflow.com/questions/62741775/python-crontab-find-existing-cron-jobs-is-giving-wrong-result

    grep_tab = cron.find_command(command)
    # for item in cron:
    for item in grep_tab:
        print(item)
        if item.is_enabled():
            item.enable(False)
        else:
            item.enable()


def create_commands():
    boot = []
    heart = []
    sense = []

    script_name = 'welcome.py'
    syslog = 'sysout.log'
    command = '{} {}/{} >> {}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), syslog)
    boot.append(command)

    script_name = 'orchards_time.py'
    syslog = 'sysout.log'
    command = '{} {}/{} >> {}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), syslog)
    boot.append(command)

    script_name = 'heartbeat.py'
    syslog = 'sysout.log'
    command = '{} {}/{} >> {}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), syslog)
    heart.append(command)

    script_name = 'orchards_time.py'
    datadir = 'data_today'
    datalog = 'timestamp.log'
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    heart.append(command)

    script_name = 'light_sensor.py'
    datadir = 'data_today'
    datalog = 'lightdata.log'
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    sense.append(command)

    script_name = 'moisture_sensor.py'
    datadir = 'data_today'
    datalog = 'moistdata.log'
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    sense.append(command)

    script_name = 'temperature_sensor.py'
    datadir = 'data_today'
    datalog = 'tempdata.log'
    command = '{} {}/{} >> {}/{}/{}'.format(super_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    sense.append(command)

    script_name = 'humidity_sensor.py'
    datadir = 'data_today'
    datalog = 'humdata.log'
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    sense.append(command)

    script_name = 'pressure_sensor.py'
    datadir = 'data_today'
    datalog = 'presdata.log'
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    sense.append(command)

    script_name = 'gps_sensor.py'
    datadir = 'data_today'
    datalog = 'gpsdata.log'
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    sense.append(command)

    script_name = 'co2_sensor.py'
    datadir = 'data_today'
    datalog = 'co2data.log'
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                            script_name, os.getcwd(), datadir, datalog)
    sense.append(command)

    return boot, heart, sense


def run_orchards(option):
    # Clean existing jobs
    cron.remove_all()

    boot, heart, sense = create_commands()

    boot_job = [None] * len(boot)
    heart_job = [None] * len(heart)
    sense_job = [None] * len(sense)
    if(option > -1):
        for i, each in enumerate(boot):
            # create jobs
            boot_job[i] = cron.new(command=each)
            # assign schedule
            boot_job[i].every_reboot()

    sense_frequency = '* * * * *'
    if(option > 0):
        for i, each in enumerate(heart):
            heart_job[i] = cron.new(command=each)
            heart_job[i].setall(sense_frequency)

    if(option > 1):
        for i, each in enumerate(sense):
            sense_job[i] = cron.new(command=each)
            sense_job[i].setall(sense_frequency)

    # clean and write to cron table
    cron.write()
    # cron.write('output.tab') # if want to maintain copy


def run_aware(option):
    # check for sensors from time to time and run
    boot, heart, sense = create_commands()

    for i, each in enumerate(sensor_list):
        if option == 0:
            if check_diffness(each):
                enable_command(sense[i])  # need a sophisticated command
            else:
                disable_command(sense[i])
        else:
            isAble = is_Able(sense[i])
            switch, policy = monitor_diffness(each, isAble)
            if switch:
                toggle_command(sense[i])
            elif policy is not None:
                reschedule_command(sense[i], policy)
            else:
                pass

    cron.write()


def run_live(option):
    # check if sensors are alive and only run if
    boot, heart, sense = create_commands()

    for i, each in enumerate(sensor_list):
        if option == 0:
            if check_liveness(each):
                enable_command(sense[i])  # need a sophisticated command
            else:
                disable_command(sense[i])
        else:
            isAble = is_Able(sense[i])
            switch, policy = monitor_liveness(each, isAble)
            if switch:
                toggle_command(sense[i])
            elif policy is not None:
                reschedule_command(sense[i], policy)
            else:
                pass

    cron.write()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Schedule tasks in DA node')
    parser.add_argument('--mode', metavar='string', required=True,
                        help='mode options are orchards, liveonly and aware')
    parser.add_argument('--option', metavar='string', required=True,
                        help='options are none, lifebeat, heartbeat and sense')
    args = parser.parse_args()
    option = 0
    if(args.option == 'sense'):
        option = 2
    elif(args.option == 'none'):
        option = -1
    elif(args.option == 'heartbeat'):
        option = 1
    else:  # 'lifebeat'
        option = 0
    if(args.mode == 'aware'):
        run_aware(option)
    elif(args.mode == 'liveonly'):
        run_live(option)
    else:  # 'orchards'
        run_orchards(option)
    sys.exit()
