#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import time
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = round(((temp_c * 9.0 / 5.0) + 32.0), 1) + 1.7
        return temp_f

def set_temp():
    output = ""
    pool = ""
    hottub = ""
    for each_device in glob.glob(base_dir + '28*'):
        device_file = each_device + '/w1_slave'
        device_id = each_device.replace(base_dir, "")
        temperature = read_temp(device_file)
        accentuate = ' is at '
        if temperature > 75:
                accentuate = ' is an inviting '
        if temperature > 95:
                accentuate = ' is a soothing '
        if temperature < 60:
                accentuate = ' is a chilly '
        if device_id == '28-041636e1d6ff':
                pool = "{\"name\":\"pool\",\"dState\":\"" + accentuate + str(temperature) + "° F\",\"dEx\":\"Monkey says the \",\"dImg\":\"pool\",\"id\":\"" + str(device_id) + "\",\"temp\":\"" + str(temperature) + "\"}"
        if device_id == '28-041636e1c5ff':
                hottub = "{\"name\":\"hot tub\",\"dState\":\"" + accentuate + str(temperature) + "° F\",\"dEx\":\"Monkey says the \",\"dImg\":\"hottub\",\"id\":\"" + str(device_id) + "\",\"temp\":\"" + str(temperature) + "\"}"
    outputjson = "[%s,%s]" % (pool, hottub)
    pooljson = "[%s]" % pool
    hottubjson = "[%s]" % hottub
    f = open('/home/pi/thermometer/pool.txt', 'w')
    print >> f, pooljson  # or f.write('...\n')
    f.close()
    f = open('/home/pi/thermometer/hottub.txt', 'w')
    print >> f, hottubjson  # or f.write('...\n')
    f.close()
    f = open('/home/pi/thermometer/temperatures.txt', 'w')
    print >> f, outputjson  # or f.write('...\n')
    f.close()

while True:
    set_temp()
    time.sleep(1800)
