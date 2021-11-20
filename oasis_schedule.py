# Read user directives and app names txt files and generate a crontab file

# Importing the CronTab class from the module
import os
from crontab import CronTab

# Creating an object from the class
# Using the root user
# cron = CronTab(user="pi")

# Optional: Using the current user
cron = CronTab(user=True)

# create commands
local_python = 'python'

script_name = 'welcome.py'
syslog = 'sysout.log'
boot1 = '{} {}/{} >> {}/{}'.format(local_python, os.getcwd(),
                                   script_name, os.getcwd(), syslog)

script_name = 'orchards_time.py'
syslog = 'sysout.log'
boot2 = '{} {}/{} >> {}/{}'.format(local_python, os.getcwd(),
                                   script_name, os.getcwd(), syslog)

script_name = 'orchards_time.py'
datadir = 'data_today'
datalog = 'timestamp.log'
command1 = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), datadir, datalog)

script_name = 'light_sensor.py'
datadir = 'data_today'
datalog = 'lightdata.log'
command2 = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), datadir, datalog)

script_name = 'moisture_sensor.py'
datadir = 'data_today'
datalog = 'moistdata.log'
command3 = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), datadir, datalog)


script_name = 'temperature_sensor.py'
datadir = 'data_today'
datalog = 'tempdata.log'
command4 = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), datadir, datalog)


script_name = 'humidity_sensor.py'
datadir = 'data_today'
datalog = 'humdata.log'
command5 = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), datadir, datalog)


script_name = 'pressure_sensor.py'
datadir = 'data_today'
datalog = 'presdata.log'
command6 = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), datadir, datalog)

# create jobs
start_job0 = cron.new(command=boot1)
start_job1 = cron.new(command=boot2)
sense_job1 = cron.new(command=command1)
sense_job2 = cron.new(command=command2)
sense_job3 = cron.new(command=command3)
sense_job4 = cron.new(command=command4)
sense_job5 = cron.new(command=command5)
sense_job6 = cron.new(command=command6)

# assign schedule
start_job0.every_reboot()
start_job1.every_reboot()

sense_frequency = 1
sense_job1.minute.every(sense_frequency)
sense_job2.minute.every(sense_frequency)
sense_job3.minute.every(sense_frequency)
sense_job4.minute.every(sense_frequency)
sense_job5.minute.every(sense_frequency)
sense_job6.minute.every(sense_frequency)

# Clean existing jobs
# cron.write('output.tab')
# cron.remove_all()
# cron.remove(job)
# cron.remove(job2)

# clean and write to cron table
cron.write()
