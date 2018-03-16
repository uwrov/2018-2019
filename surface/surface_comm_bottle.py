### Communication between robot and surface system
### Raspberry Pi  <-->  Surface computer w/ Moz. Firefox and HTML GUI

import json
from bottle import get, put, route, run, template
import bottle  ## looks peculiar
from math import trunc

# Joystick state variables

controller_state = {"lstick-x" : 0, "lstick-y" : 0, "rstick-x" : 0, "rstick-y" : 0, "dpad-x" : 0, "dpad-y" : 0, "rtrigger" : -1}

def state_of(component):
    return controller_state[component]

def store_state(component, state):
    # component is the key (a string) for the dictionary controller_state.
    # state is a string that represents a float (the joystick value
    # transmitted from the web interface)
    controller_state[component] = float(state)


# global Motor_Joystick_X
# global Motor_Joystick_Y
# global DPad_X
# global DPad_Y
# global Right_Trigger

# Motor_Joystick_X = 0
# Motor_Joystick_Y = 0
# DPad_X = 0
# DPad_Y = 0

def test_transform(value):
    return "look at me! I work!" + value

# transform sensors Python dict. to JS object. and send to surface on request
@get('/sensor')
def getsensor():
    # This line allows web pages from other domains (or static files)
    # to access this via Ajax.  It must be included in each handler function
    # in order for the web interface to communicate at all.
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
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
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("dpad-x", gamepadValue)

# Moving forward and backward
@get("/movement/dpad-y/<gamepadValue>")
def strafe_forward_backward(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("dpad-y", gamepadValue)

# Rotating
@get("/movement/right-joystick-x/<gamepadValue>")
def rotate_robot(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rstick-x", gamepadValue)

# Accelerating forward, somewhat in direction of of rotation
@get("/movement/right-joystick-y/<gamepadValue>")
def accelerate_forward_backward(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rstick-y", gamepadValue)

# Moving up and down
@get("/movement/right-trigger/<gamepadValue>")
def vertical_movement(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rtrigger", gamepadValue)


# This form starts the web server (run() is from bottle)
# run(host='localhost', port=8085)
