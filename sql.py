import serial
import datetime
import pymssql
import time
import syslog
import traceback
import sys
import arrow
import os
import subprocess


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

def connectSerial():
    try:
        ser1 = serial.Serial('/dev/ttyACM0',115200,timeout=1)
        return ser1
    except Exception as ex:
        syslog.syslog("Could not connect on /dev/ttyACM0")
        _, _, ex_traceback = sys.exc_info()
        log_traceback(ex, ex_traceback)
        try:
            ser1 = serial.Serial('/dev/ttyACM1',115200,timeout=1)
            return ser1
        except Exception as ex:
            syslog.syslog("Could not connect on /dev/ttyACM1")
            _, _, ex_traceback = sys.exc_info()
            log_traceback(ex, ex_traceback)

while 1:
    try:

        # Wait 30 seconds on startup
        #time.sleep(30)

        ser = connectSerial()

        conn = pymssql.connect(server='xxx.database.windows.net', user='', password='', database='weather')
        lastReadTime = arrow.utcnow()

        while 1:

            try:
                currentTime = arrow.utcnow()

                # If no response in last 30 seconds, retry the serial connection
                if (currentTime > (lastReadTime + datetime.timedelta(seconds=60))):
                    syslog.syslog("Nothing coming through on serial, retrying connection")

                    try:
                        ser.close()
                    except:
                        syslog.syslog("Could not close old connection")

                    # Reset USB device
                    p = subprocess.call(['/home/pi/usbreset','/dev/bus/usb/001/007'], stdout=DEVNULL, stderr=DEVNULL)
                    ser = connectSerial()

                    lastReadTime = arrow.utcnow()

            except Exception as ex:
                _, _, ex_traceback = sys.exc_info()
                log_traceback(ex, ex_traceback)
                time.sleep(1)
                continue
            #print "trying to read..."

            response = ser.readline()
            cursor = conn.cursor()

            if len(response) > 0:
                lastReadTime = arrow.utcnow()
                nowFormatted = time.strftime('%Y-%m-%d %H:%M:%S')

                try:
                    channel,temperature,humidity = response.split(",")
                except Exception as ex:
                    _, _, ex_traceback = sys.exc_info()
                    log_traceback(ex, ex_traceback)
                    time.sleep(1)
                    continue

                #print channel
                #print temperature
                #print humidity

                if (len(channel) > 0 and len(temperature) > 0 and len(humidity) > 0 and int(humidity) > 20 and float(temperature) > 60.0 and float(temperature) < 100.0):
                    syslog.syslog(response)
                    try:
                        cursor.execute("INSERT Entries (RecordDate, Channel, TemperatureInF, HumidityInPercent) OUTPUT INSERTED.EntryID VALUES ('" + nowFormatted + "'," + channel + ", " + temperature + ", " + humidity + ")")
                        row = cursor.fetchone()
                        while row:
                            syslog.syslog("Inserted Entry ID : " + str(row[0]))
                            row = cursor.fetchone()
                        conn.commit()
                    except Exception as ex:
                        _, _, ex_traceback = sys.exc_info()
                        log_traceback(ex, ex_traceback)
                        try:
                            conn.rollback()
                            conn = pymssql.connect(server='pao9exwntp.database.windows.net', user='paulwhit@pao9exwntp', password='c3R2pUAm', database='weather')
                        except Exception as ex:
                            _, _, ex_traceback = sys.exc_info()
                            log_traceback(ex, ex_traceback)
                            time.sleep(1)

                    # Wait 10 seconds then retry
                    time.sleep(10)

    except Exception as ex:
        try:
            _, _, ex_traceback = sys.exc_info()
            log_traceback(ex, ex_traceback)
        except:
            syslog.syslog("Unhandled exception trying to collect exception information -sigh")

        #time.sleep(30)

