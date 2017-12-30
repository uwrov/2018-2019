import glob, math, numpy, serial, sys
# cv2, 
# import cv2.cv as cv
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
HEADER_KEY_HOLD_ON = 103
HEADER_KEY_HOLD_OFF = 104

# Communication
ser = None

pingTime = -1
pingStartTime = 0

WAIT_TIME = 0.1
CONNECT_DELAY = 4

# Sensor values received from Arduino
sensor1Name = 0
sensor2Name = 1
sensors = {sensor1Name : 0, sensor2Name : 0}

# Motor values sent to Arduino
# Stores values between 0 and 254
motors = {1: 127, 2: 127, 3: 127, 4: 127, 5: 127, 6: 127}

ROTATION_SCALE = 0.5
MOTOR_ANGLE = math.sqrt(2) / 2
SCALE = 127

# Image
cam1 = None
cam2 = None

#DESIRED_IMAGE_SIZE = {'width':300, 'height':200}
DESIRED_IMAGE_SIZE = {'width':640, 'height':480}
IMAGE_SIZE = {'width':640, 'height':480}
image = None



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
# Returns 0 if an error occurred during serial connection 
# Returns 1 otherwise
def arduinoSetup(serialPort):
    global ser

    try:
        ser = serial.Serial(serialPort)
    except (OSError, serial.SerialException):
        print "arduinoSetup: Serial '" + str(serialPort) + "' did not connect"
        return 0
    
    start_new_thread(__updateData__, ())
    return 1


# Updates the sensor data and ping time from the Arduino. Runs on
# a separate thread after setup runs
def __updateData__():
    global motors, sensors
    global pingTime, pingStartTime
    
    sleep(CONNECT_DELAY) # damn servos

    while True:
        sleep(WAIT_TIME)

        # Write motor values to the Arduino
        for i in range(0, 6):
            ser.write([HEADER_KEY_OUT_1, HEADER_KEY_OUT_2, i, motors[i+1]])

        # Check for new packets from Arduino
        # Packets should be received in sets of 4 bytes
        while ser.inWaiting() >= 4:
            if __readByte__(ser) == HEADER_KEY_IN_1 and __readByte__(ser) == HEADER_KEY_IN_2:
                sensorName = __readByte__(ser)
                sensorValue = __readByte__(ser)
                # Check if sent packet is returned ping
                if sensorName == HEADER_KEY_PING:
                    pingEndTime = clock()
                    pingTime = pingEndTime - pingStartTime
                else:
                    sensors[sensorName] = sensorValue


# Set the motor speeds based on the given joystick values
# Joystick values range between -1 and 1
def setMotors(xSpeed, ySpeed, zSpeed, rotation):
    __setZ__(zSpeed)
    m1, m2 = __getMotorTranslate__(xSpeed, ySpeed)
    __setMotorRotation__(rotation, m1, m2)


# Set the speed of the z direction (up/down) motors
def __setZ__(zSpeed):
    global motors

    zPow = int(zSpeed * SCALE) + SCALE
    motors[5] = motors[6] = zPow


# Set the speed of the x/y direction (up/down/left/right) motors
def __getMotorTranslate__(xSpeed, ySpeed):
    # Translate x/y coordinate values to motor coordinate values
    m1 = MOTOR_ANGLE * xSpeed + MOTOR_ANGLE * ySpeed
    m2 = MOTOR_ANGLE * ySpeed - MOTOR_ANGLE * xSpeed

    # Don't normalize values if both are 0
    m1_norm = m2_norm = 0
    if m1 != 0 or m2 != 0:
        m1_norm = m1 / abs(max(m1, m2)) * min(math.hypot(xSpeed, ySpeed), 1)
        m2_norm = m2 / abs(max(m1, m2)) * min(math.hypot(xSpeed, ySpeed), 1)
    return [m1_norm, m2_norm]


# Add the speed of rotation to the motor speeds
def __setMotorRotation__(rotation, m1, m2):
    global motors

    frontLeftPow = -m1 - ROTATION_SCALE * rotation
    frontRightPow = -m2 + ROTATION_SCALE * rotation
    backRightPow = m1 - ROTATION_SCALE * rotation
    backLeftPow = m2 + ROTATION_SCALE * rotation

    # Normalize the values if greater than 1
    maxPow = max(abs(frontLeftPow), abs(frontRightPow),
        abs(backRightPow), abs(backLeftPow))
    if maxPow > 1:
        frontLeftPow /= maxPow
        frontRightPow /= maxPow
        backRightPow /= maxPow
        backLeftPow /= maxPow

    motors[1] = int(frontLeftPow * SCALE) + SCALE
    motors[2] = int(frontRightPow * SCALE) + SCALE
    motors[3] = int(backRightPow * SCALE) + SCALE
    motors[4] = int(backLeftPow * SCALE) + SCALE




# Release the cameras and serial being used
# Run once program ends
def close():
    if ser:
        ser.close()
    if cam1:
        cam1.release()
    if cam2:
        cam2.release()
    cv2.destroyAllWindows()


# Change the state of the claw
# Switches between open and closed
def moveClaw():
    ser.write([HEADER_KEY_OUT_1, HEADER_KEY_OUT_2,
        HEADER_KEY_PNEUMATICS, 0])


# Writes a special byte that should trigger the Arduino light
# to turn on. Use to test communication with the Arduino
def testComm():
    # Zeros are garbage data
    ser.write([HEADER_KEY_OUT_1, HEADER_KEY_OUT_2,
        HEADER_KEY_LIGHT, 0])


# Writes a special byte that should be returned by the Arduino.
# Use to test ping times to the Arduino
def testPing():
    global pingStartTime

    pingStartTime = clock()
    # Zeros are garbage data
    ser.write([HEADER_KEY_OUT_1, HEADER_KEY_OUT_2,
        HEADER_KEY_PING, 0])


# Return the last recorded ping time
# -1 if no ping recorded yet
def getPing():
    return pingTime


# Read a byte from serial, and return the value.
def __readByte__(ser):
    return ord(ser.read())
