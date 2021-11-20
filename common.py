#!/usr/bin/env python

# importing libraries
import os
from orchards_time import date_today


def create_folder():
    # define node name
    node_name = "SA01"
    # generating date in format
    date = date_today()
    folder_name = node_name+"-{}".format(date)

    print("Creating folder {}".format(folder_name))

    # creating directories
    os.mkdir(folder_name)


def delete_folder(folder_name):
    os.rmdir(folder_name)


# Main function
if __name__ == "__main__":
    create_folder()