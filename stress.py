#!/usr/bin/env python

from multiprocessing import Pool
from multiprocessing import cpu_count
import signal

stop_loop = 10000


def exit_chld(x, y):
    global stop_loop
    stop_loop = 0


def f(x):
    global stop_loop
    while stop_loop:
        x*x
        stop_loop -= 1


signal.signal(signal.SIGINT, exit_chld)


def stress():
    processes = cpu_count()
    #print('-' * 20)
    #print('Running load on CPU(s)')
    #print('Utilizing %d cores' % processes)
    #print('-' * 20)
    pool = Pool(processes)
    pool.map(f, range(processes))
