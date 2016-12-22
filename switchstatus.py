import serial, time

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

ser = serial.Serial()
ser.port = "/dev/ttyS0"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.rtscts = True

ser.open()

foundStarter = False
while foundStarter == False:
        skip = ser.read(1)
        for c in xrange(0, len(skip), 16):
                chars = skip[c:c+16]
                if chars[0] == '\x62':
                        ser.read(13)
                        foundStarter = True

out = ser.read(14)

for c in xrange(0, len(out), 16):
        chars = out[c:c+16]
        if chars[0] != '\x62':
                print 'Not the right starter thing'
                continue

        mema = chars[1]
        memb = chars[2]
        srca = chars[5]
        srcb = chars[6]
        power = chars[10]

        if (srcb == '\x01'):
                print 'Xbox One'
        elif (srcb == '\x02'):
                print 'Fire TV'
        elif (srcb == '\x04'):
                print 'Xbox 360'
        elif (srcb == '\x08'):
                print 'Number 4'

#hexdump(out)

ser.close()
