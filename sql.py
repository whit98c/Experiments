import serial
import datetime
import pymssql
import time
import syslog
import traceback
import sys

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

while 1:
    try:
        ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)
        conn = pymssql.connect(server='server.database.windows.net', user='user@server', password='password', database='weather')

        while 1:
            response = ser.readline()
            cursor = conn.cursor()

            if len(response) > 0:
                nowFormatted = time.strftime('%Y-%m-%d %H:%M:%S')

                try:
                    channel,temperature,humidity = response.split(",")
                except Exception as ex:
                    _, _, ex_traceback = sys.exc_info()
                    log_traceback(ex, ex_traceback)
                    time.sleep(1)
                    continue

                if (len(channel) > 0 and len(temperature) > 0 and len(humidity) > 0 and humidity > 20 and temperature > 60 and temperature < 100):
                    syslog.syslog(response)
                    try:
                        cursor.execute("INSERT Entries (RecordDate, Channel, TemperatureInF, HumidityInPercent) OUTPUT INSERTED.EntryID VALUES ('" + nowFormatted + "'," + channel + ", " + temperature + ",
" + humidity + ")")
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

        time.sleep(30)

