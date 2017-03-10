#!/usr/bin/python

import serial
import datetime
import time
import syslog
import traceback
import sys
import arrow
import os
import subprocess
import string
import paho.mqtt.publish as publish

DEVNULL = open(os.devnull, 'wb')

# http://stackoverflow.com/a/33211980
def log_traceback(ex, ex_traceback=None):
        try:
            if ex_traceback is None:
                ex_traceback = ex.__traceback__
            tb_lines = [ line.rstrip('\n') for line in
                    traceback.format_exception(ex.__class__,ex,ex_traceback)]
            for line in tb_lines:
                syslog.syslog(line)
        except:
            syslog.syslog("Unhandled exception with sending exception to syslog")


lastReadTime = arrow.utcnow()

while 1:

    line = sys.stdin.readline()

    if line.startswith('20'):
        try:
            parts = line.split(',')
            date = parts[0]
            channel = parts[3]
            battery = parts[4]
            humidity = parts[9]
            deviceid = parts[21]
            temperature = parts[22]

            syslog.syslog('Channel: ' + channel + " Temp: " + str(temperature) + " Humidity: " + str(humidity) + " Battery: " + battery)
            # TODO: syslog.syslog(debugMessage)
            lastReadTime = arrow.utcnow()
            nowFormatted = time.strftime('%Y-%m-%d %H:%M:%S')

            for whitespace_character in string.whitespace:
                channel = channel.replace(whitespace_character,'')

            for whitespace_character in string.whitespace:
                temperature = temperature.replace(whitespace_character,'')

            for whitespace_character in string.whitespace:
                humidity = humidity.replace(whitespace_character,'')

                #p rint response

            # Publish to mqtt
            msgs = [
                {'topic':"home/humidity" + channel, 'payload':str(humidity)},
                {'topic':"home/temperature" + channel, 'payload':str(temperature)},
                {'topic':"home/lastupdateraw" + channel, 'payload':str(datetime.datetime.now())},
                {'topic':"home/battery" + channel, 'payload':battery}]
            publish.multiple(msgs, hostname="amelia")

            if (len(channel) > 0 and len(temperature) > 0 and len(humidity) > 0 and int(humidity) > 20 and float(temperature) > 60.0 and float(temperature) < 100.0):

                # Wait 10 seconds then retry
                time.sleep(10)

        except Exception as ex:
            _, _, ex_traceback = sys.exc_info()
            log_traceback(ex, ex_traceback)
            time.sleep(1)
            continue
