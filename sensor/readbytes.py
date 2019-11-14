import serial


if __name__ == '__main__':
    ser = serial.Serial('COM3')

    for i in range(100):
        print(ser.read())