# Read user directives and app names txt files and generate a crontab file

# Importing the CronTab class from the module
import os
import sys
from crontab import CronTab

# Creating an object from the class
# Using the root user
# cron = CronTab(user="pi")

# Optional: Using the current user
cron = CronTab(user=True)

# create commands
local_python = 'python'


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
    sense.append(command)

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
    command = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
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

    return boot, heart, sense


def run_orchards(option):
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

    sense_frequency = 1
    if(option > 0):
        for i, each in enumerate(heart):
            heart_job[i] = cron.new(command=each)
            heart_job[i].minute.every(sense_frequency)

    if(option > 1):
        for i, each in enumerate(sense):
            sense_job[i] = cron.new(command=each)
            sense_job[i].minute.every(sense_frequency)

    # Clean existing jobs
    # cron.write('output.tab')
    # cron.remove_all()
    # cron.remove(job)
    # cron.remove(job2)

    # clean and write to cron table
    cron.write()


def run_aware(option):
    cron.write()


def run_live(option):
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
