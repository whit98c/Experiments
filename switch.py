import serial, time, sys

ser = serial.Serial()
ser.port = "/dev/ttyS0"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.rtscts = True

ser.open()

input = sys.argv[1]
print "Switching to " + input

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

ser.close()

