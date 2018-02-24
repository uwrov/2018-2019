### Communication between robot and surface system
### Raspberry Pi  <-->  Surface computer w/ Moz. Firefox and HTML GUI

import json
from bottle import get, put, route, run, template
from math import trunc


def test_transform(value):
    return "look at me! I work!" + value

# transform sensors Python dict. to JS object. and send to surface on request
@get('/sensor')
def getsensor():
    return json.dumps(sensors)

# @get('/motor/<motor>/<value>')
# # Expects motor arguement to be motor numbers as indicated in the motor diagram
# # in internal_communication.py and value to be a float between -1 and 1,
# # where -1 is reverse full thrust and 1 is forward full thrust.
# def compute_and_set_motor_speed(motor, value):
#     sendMotorSignal(motor - 1,  # decrease motor by one to get index of motor in array Motors[] aboard the Arduino
#                     trunc(value * 256) + 128)  # scale to 8-bit byte


# For input on moving left and right ("strafing")
@get("/movement/dpad-x/<gamepadValue>")
def strafe_left_right(gamepadValue):
    DPad_X = gamepadValue

# Moving forward and backward
@get("/movement/dpad-y/<gamepadValue>")
def strafe_forward_backward(gamepadValue):
    DPad_Y = gamepadValue

# Rotating
@get("/movement/right-joystick-x/<gamepadValue>")
def rotate_robot(gamepadValue):
    Motor_Joystick_X = gamepadValue

# Accelerating forward, somewhat in direction of of rotation
@get("/movement/right-joystick-y/<gamepadValue>")
def accelerate_forward_backward(gamepadValue):
    Motor_Joystick_Y = gamepadValue

# Moving up and down
@get("/movement/right-trigger/<gamepadValue>")
def vertical_movement(gamepadValue):
    print(gamepadValue)
    # insert means to store value

run(host='localhost', port=8085)
