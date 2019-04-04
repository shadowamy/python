import serial
import sys

try:
    ser = serial.Serial('COM4', 9600)
except Exception, e:
    print 'open serial failed.'
    exit(1)
#print 'The temprature is'
count = 0
while True:
    s = ser.read()
    ser.write(s)
    # write to stdout and flush it
    sys.stdout.write(s)
    sys.stdout.flush()
    count += 1
    if count >=2 :
        break


# ser.write(s)
# write to stdout and flush it
# sys.stdout.write(s)
# sys.stdout.flush()
