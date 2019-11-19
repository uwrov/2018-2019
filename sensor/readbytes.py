import serial
import time
import struct
# Read acceleromoter output from arduino, 
# expects output to be in space separated string.
def read_string():
    ser = serial.Serial('COM3', 115200, timeout=6)
    while True:
        time.sleep(.25)
        ser.flushInput()
        reading = ser.readline().split()
        if len(reading) == 3:
            print("x: " + reading[0].decode('ascii') + 
                  ", y: " + reading[1].decode('ascii') +
                  ", z: " + reading[2].decode('ascii'))
        else:
            print("poop data")

if __name__ == '__main__':
    # ser = serial.Serial('COM3', 115200, timeout=6)
    # while True:
    #     time.sleep(0.25)
    #     ser.flushInput()
    #     out = ser.readline()
    #     if len(out) > 0:
    #         # print(out[0:-1])
    #         print(struct.unpack('f', out[0:-1]))
    read_string()