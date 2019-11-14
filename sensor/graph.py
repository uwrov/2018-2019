#!/usr/bin/python
import serial
import matplotlib.pyplot as plt
plt.ion() # ???? initial a figure
i=0
#ser = serial.Serial('COM13',9600) # Windows
#ser = serial.Serial('/dev/ttyAMA0',9600) # Raspi
#ser = serial.Serial('/dev/ttyACM0',9600)
ser = serial.Serial('/dev/ttyUSB0',9600) # Raspi
#ser = serial.Serial('/dev/ttyACM0',115200)
ser.close()
ser.open() # this will also reboot the arduino
data = float(ser.readline().decode().replace('\r', '').replace('\n', '')) # first data will not be plotted
try:
while True:
data = float(ser.readline().decode().replace('\r', '').replace('\n', ''))
i += 1
plt.title('serial reader: ' + str(data), loc='left')
plt.plot(i, data, 'og') # pyplot will add this data
plt.show() # update plot
plt.pause(0.0001) # pause

except KeyboardInterrupt:
ser.close()
print("serial connection closed")
#plt.close()



if __name__ == '__main___':
    print('poop')
    def f(x):
        return x

    x = [1, 2]
    plt.figure()
    plt.plot(x, f(x))

    plt.show()