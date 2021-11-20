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
filename = 'sysout.log'
command = 'echo hello_orchards >> {}/{}'.format(os.getcwd(), filename)
command2 = 'pwd >> {}/{}'.format(os.getcwd(), filename)

local_python = 'python'
script_name = 'orchards_time.py'
datadir = 'data_today'
datalog = 'timestamp.log'
command3 = '{} {}/{} >> {}/{}/{}'.format(local_python, os.getcwd(),
                                         script_name, os.getcwd(), datadir, datalog)

# create jobs
job = cron.new(command=command)
job2 = cron.new(command=command2)
job3 = cron.new(command=command3)

# assign schedule
job.minute.every(1)
job2.minute.every(1)
job3.minute.every(1)
# The job takes place once every 5 minutes
# job.minute.every(5)

# The job takes place once every four hours
# job.hour.every(4)

# The job takes place on the 4th, 5th, and 6th day of the week.
#job.day.on(4, 5, 6)

# Clearing the restrictions of a job
# job.clear()

# Clean existing jobs
# cron.write('output.tab')
# cron.remove_all()
# cron.remove(job)
# cron.remove(job2)

# clean and write to cron table
cron.write()
