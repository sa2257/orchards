import os
import sys
from crontab import CronTab

# Using the current user
cron = CronTab(user=True)


def create_command():
    script_name = 'optee_config.py'
    command = '{} {}/{} {} {}'.format('python', os.getcwd(),
                                      script_name, '--option', '1')

    return command


def schedule_make():
    command = create_command()

    job = cron.new(command=command)
    job.every_reboot()

    # clean and write to cron table
    cron.write()


def run_make():
    # run cmake commands from optee_client
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Initial settings for OPTEE')
    parser.add_argument('--option', metavar='string', required=True,
                        help='options are 0 and 1')
    args = parser.parse_args()

    if(args.option == '0'):
        schedule_make()
    else:  # '1'
        run_make()
    sys.exit()
