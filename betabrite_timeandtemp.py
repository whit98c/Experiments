#!/usr/bin/python

import time
import datetime
import alphasign
import pyowm
import paho.mqtt.publish as publish

def hexdump(src, length=16, sep='.'):
        FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
        lines = []
        for c in xrange(0, len(src), length):
                chars = src[c:c+length]
                hex = ' '.join(["%02x" % ord(x) for x in chars])
                if len(hex) > 24:
                        hex = "%s %s" % (hex[:24], hex[24:])
                printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or sep) for x in chars])
                lines.append("%08x:  %-*s  |%s|\n" % (c, length*3, hex, printable))
        print ''.join(lines)


def main():
        sign = alphasign.Serial()
        sign.connect()
        sign.clear_memory()

        # Set the time

        timeString = alphasign.String(size=100, label="1")
        tempString = alphasign.String(size=100, label="2")
        humiString = alphasign.String(size=100, label="3")

#        helloText = alphasign.Text("%s %sF %s%%" %(timeString.call(), 
#                tempString.call(), 
#                humiString.call()), label="A", mode=alphasign.modes.HOLD)
        helloText = alphasign.Text("%s%s %s%sF %s%s%%" %(alphasign.colors.DIM_RED, timeString.call(), 
                alphasign.colors.YELLOW, tempString.call(), 
                alphasign.colors.ORANGE, humiString.call()), label="A", mode=alphasign.modes.HOLD)
        sign.allocate((timeString,tempString,humiString,helloText))
        sign.set_run_sequence((helloText,))
        sign.write(timeString)
        sign.write(tempString)
        sign.write(humiString)
#	sign.write('Hubstream')
        sign.write(helloText)

        while True:

		try:
                	owm = pyowm.OWM('163f58185b28688d805dae724b718025')
                	observation = owm.weather_at_place('Rockville,MD')
                	w = observation.get_weather()
                	currTemp = int(w.get_temperature('fahrenheit').get('temp'))
                	humidity = w.get_humidity()

                	currentTime = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M")
                	stringData = currentTime

                	timeString.data = currentTime
                	tempString.data = currTemp
                	humiString.data = humidity

                	sign.write(timeString)
                	sign.write(tempString)
                	sign.write(humiString)

		#readString = alphasign.Packet("%s%s%s" % (alphasign.constants.READ_TEXT, 'A', ''))
		#sign.write(readString)
		#readBytes = sign._conn.readline()
		#hexdump(readBytes)
		#print readBytes
		#readBytes = readBytes[33:-6]
		#hexdump(readBytes)
		#print readBytes

			readString = alphasign.Packet("%s%s%s" % (alphasign.constants.READ_STRING, '1', ''))
			sign.write(readString)
			readBytes = sign._conn.readline()
		#hexdump(readBytes)
		#print readBytes
			readBytes = readBytes[33:-6]
		#hexdump(readBytes)
		#print readBytes
			onSignNow = readBytes

			readString = alphasign.Packet("%s%s%s" % (alphasign.constants.READ_STRING, '2', ''))
			sign.write(readString)
			readBytes = sign._conn.readline()
		#hexdump(readBytes)
		#print readBytes
			readBytes = readBytes[33:-6]
		#hexdump(readBytes)
		#print readBytes
			onSignNow = onSignNow + " " + readBytes + "F"

			readString = alphasign.Packet("%s%s%s" % (alphasign.constants.READ_STRING, '3', ''))
			sign.write(readString)
			readBytes = sign._conn.readline()
		#print readBytes
		#hexdump(readBytes)
			readBytes = readBytes[33:-6]
		#hexdump(readBytes)
		#print readBytes
			onSignNow = onSignNow + " " + readBytes + "%"

		#hexdump(readBytes)
		#sign.write('Hubstream')
			#print onSignNow
			publish.single("home/signtext", onSignNow, hostname='amelia');

               		time.sleep(10)

		except:
			time.sleep(30)
if __name__ == "__main__":
        main()
