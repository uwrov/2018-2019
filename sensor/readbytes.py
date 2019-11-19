import serial
import time
import struct

if __name__ == '__main__':
    ser = serial.Serial('COM3', 115200, timeout=6)
    # for i in range(25):
    #     bs = b''
    #     for j in range(4):
    #         bs += ser.read()
    #     print(struct.unpack('f', bs))
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