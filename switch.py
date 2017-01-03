#!/usr/bin/python

import serial, time, sys, os, syslog
import paho.mqtt.client as mqtt


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

def connectSerial():
    try:
        ser1 = serial.Serial('/dev/ttyS0',9600,timeout=1)
        ser1.bytesize = serial.EIGHTBITS
        ser1.parity = serial.PARITY_NONE
        ser1.rtscts = True
        return ser1
    except Exception as ex:
        syslog.syslog("Could not connect on /dev/ttyS0")
        _, _, ex_traceback = sys.exc_info()
        log_traceback(ex, ex_traceback)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
        syslog.syslog("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("home/tvswitch")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

        ser = connectSerial()
        #ser.open()

        syslog.syslog(msg.topic+" "+str(msg.payload))
        input = msg.payload

        syslog.syslog("Switching to " + input)

        if input == '1':
                ser.write('\x04')
                time.sleep(0.05)
                ser.write('\xfb')
                time.sleep(0.05)
                ser.write('\xd5')
                time.sleep(0.05)
                ser.write('\x7b')
                time.sleep(0.05)
                ser.flush()
                os.system("omxplayer -o local /home/pi/XboxOne.mp3")

        elif input == '2':
                ser.write('\x05')
                time.sleep(0.05)
                ser.write('\xfa')
                time.sleep(0.05)
                ser.write('\xd5')
                time.sleep(0.05)
                ser.write('\x7b')
                time.sleep(0.05)
                ser.flush()
                os.system("omxplayer -o local /home/pi/FireTV.mp3")

        elif input == '3':
                ser.write('\x06')
                time.sleep(0.05)
                ser.write('\xf9')
                time.sleep(0.05)
                ser.write('\xd5')
                time.sleep(0.05)
                ser.write('\x7b')
                time.sleep(0.05)
                ser.flush()
                os.system("omxplayer -o local /home/pi/Xbox360.mp3")

        elif input == '4':
                ser.write('\x07')
                time.sleep(0.05)
                ser.write('\xf8')
                time.sleep(0.05)
                ser.write('\xd5')
                time.sleep(0.05)
                ser.write('\x7b')
                time.sleep(0.05)
                ser.flush()
                os.system("omxplayer -o local /home/pi/NES.mp3")

        ser.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("amelia", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_forever()

ser.close()
