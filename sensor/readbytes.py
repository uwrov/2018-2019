import serial
import time
import struct
# Read acceleromoter output from arduino, 
# expects output to be in space separated string.
def read_string(ser):
    ser.flushInput()
    # Wait a little bit for data to be written to serial
    time.sleep(.25)
    reading = ser.readline().split()
    result = None
    
    if len(reading) == 3:
        result = "x: " + reading[0].decode('ascii') + \
                 ", y: " + reading[1].decode('ascii') + \
                 ", z: " + reading[2].decode('ascii')
    else:
        result = "poopoo"
    
    return result

if __name__ == '__main__':
    ser = serial.Serial('COM3', 115200, timeout=6)
    while True:
        print(read_string(ser))