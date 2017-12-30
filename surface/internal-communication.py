### Communication between different parts inside the robot ---
### Arduino - Raspberry Pi

import serial
from time import clock, sleep
from thread import start_new_thread

# Data Headers
HEADER_KEY_OUT_1 = 17
HEADER_KEY_OUT_2 = 151
HEADER_KEY_IN_1 = 74
HEADER_KEY_IN_2 = 225
HEADER_KEY_PNEUMATICS = 100
HEADER_KEY_LIGHT = 101
HEADER_KEY_PING = 102
HEADER_KEY_QUERY_MOTOR_SPEED = 103
HEADER_KEY_HOLD_ON = 110
HEADER_KEY_HOLD_OFF = 111

PACKET_SIZE = 4

# Communication
ser = None

pingTime = -1
pingStartTime = 0

WAIT_TIME = 0.1
CONNECT_DELAY = 4

# Sensors
sensors = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0}

# Motor values sent to Arduino
# Stores values between 0 and 255
# Value of 128 is the motors' zero value
motors = {0 : 128, 1: 128, 2: 128, 3: 128, 4: 128, 5: 128}


# THE BOT
#
#     FRONT
#
#  1 /_____\ 2
#    |     |
#    |  5  |
#    |  6  |
#    |_____|
#  4 \     / 3


# Set up serial communication and start data reading thread
# Returns -1 if an error occurred during serial connection 
# Returns 0 otherwise
# On Unix-like systems, serialPort is the name of the serial device file
def arduinoSetup(serialPort):
    global ser

    try:
        ser = serial.Serial(serialPort)
    except (OSError, serial.SerialException):
        print "arduinoSetup: Serial '" + str(serialPort) + "' did not connect"
        return -1
    
#    start_new_thread(__updateData__, ())
    return 0

# ser.write() normally takes a string; we instead provide an array of bytes of out choosing
def writePacket(dataByte1, dataByte2):
    ser.write(bytearray([HEADER_KEY_OUT_1, HEADER_KEY_OUT_2,
                         dataByte1, dataByte2]))


# Read a character from serial, convert into a byte and return byte.
# ser.read() normally returns a character;
# ord() converts the character into its character code,
# which is the byte the Arduino sent
def __readByte__(ser):
    return ord(ser.read())

# Reads all available packets and returns the number of packets read.
def readAllPackets():
    totalPacketsRead = 0
    global pingStartTime, pingEndTime, pingTime
    while ser.inWaiting() >= PACKET_SIZE:   # Do we have enough bytes to make a packet?
        # Are the headers correct?  (Is the packet uncorrupted?)
        if __readByte__(ser) == HEADER_KEY_IN_1 and __readByte__(ser) == HEADER_KEY_IN_2:
            totalPacketsRead += 1
            controlByte = __readByte__(ser)
            dataByte = __readByte__(ser)
            # Packet was for pinging?
            if controlByte == HEADER_KEY_PING:
                # compute time it took to get a response from the robot
                pingEndTime = clock()
                pingTime = pingEndTime - pingStartTime
                print("Ping interval " + str(pingTime) + " received at " + str(pingEndTime))
            elif controlByte == HEADER_KEY_QUERY_MOTOR_SPEED:
                print("Motor speed: " + str(__readByte__(ser)))
            else:
                # controlByte is assumed to be the sensor number
                # dataByte assumed to be the value read from sensor
                sensors[controlByte] = dataByte
    return totalPacketsRead

def sendPing():
    global pingStartTime

    pingStartTime = clock()
    # Zeros are garbage data
    writePacket(HEADER_KEY_PING, 0)

def getPingTime():
    return pingTime

# Tells Arduino to change its LED's state
def toggleLED():
    # Zeros are garbage data
    writePacket(HEADER_KEY_LIGHT, 0)

# Abstraction.  Send a packet telling the Arduino to change the speed of the indicated motor to that indicated by the speed byte
def sendMotorSignal(motorNumber, motorSpeedByte):
    writePacket(motorNumber, motorSpeedByte)


