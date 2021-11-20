# Read user directives and app names txt files and generate a crontab file

# Importing the CronTab class from the module
import os
from crontab import CronTab

# Creating an object from the class
# Using the root user
cron = CronTab(user="pi")


# Using the current user
#my_cron = CronTab(user=True)

# Creating an object from the class into a file
#file_cron = CronTab(tabfile="filename.tab")

# Creating a new job
#job = cron.new(command='echo hello_world')

# Setting up restrictions for the job
# The job takes place once every 5 minutes
# job.minute.every(5)

# The job takes place once every four hours
# job.hour.every(4)

# The job takes place on the 4th, 5th, and 6th day of the week.
#job.day.on(4, 5, 6)

# Clearing the restrictions of a job
# job.clear()

# cron.write()
filename = 'sysout.log'
command = 'echo hello_world >> {}/{}'.format(os.getcwd(), filename)
job = cron.new(
    command=command)
command2 = 'pwd >> {}/{}'.format(os.getcwd(), filename)
job2 = cron.new(
    command=command2)
job.minute.every(1)
job2.minute.every(1)
cron.write()
