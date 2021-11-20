#!/usr/bin/env python

import sys


def welcome(version):
    print("Welcome to {}!".format(version))
    return 0


# Main function
if __name__ == "__main__":
    version = "Orchards"  # Farmbeats, Green-TEE, Sentinel, Oasis
    welcome(version)
    sys.exit()
