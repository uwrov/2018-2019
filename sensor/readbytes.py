import serial
import struct

if __name__ == '__main__':
    ser = serial.Serial('COM3')
    # print(ser.read().decode('ascii'))
    for i in range(25):
        bs = b''
        for j in range(4):
            bs += ser.read()
        print(struct.unpack('f', bs))