#!/usr/bin/env python

# importing libraries
import os
import sys
from orchards_time import date_today


def create_folder():
    base_folder = 'data_today'
    isdir = os.path.isdir(base_folder)

    if isdir:
        # define node name
        node_name = "SA01"
        # generating date in format
        date = date_today()
        folder_name = node_name+"-{}".format(date)
        isdir = os.path.isdir(folder_name)
        if isdir:
            print("Folder {} already exists!".format(folder_name))
            return -1
        else:
            print("Creating folder {}".format(folder_name))
            # creating directories
            os.replace(base_folder, folder_name)

    os.mkdir(base_folder)
    return 0


def delete_folder(folder_name):
    os.rmdir(folder_name)


# Main function
if __name__ == "__main__":
    create_folder()
    sys.exit()
