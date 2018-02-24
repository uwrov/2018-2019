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
# # in internal-communication.py and value to be a float between -1 and 1,
# # where -1 is reverse full thrust and 1 is forward full thrust.
# def compute_and_set_motor_speed(motor, value):
#     sendMotorSignal(motor - 1,  # decrease motor by one to get index of motor in array Motors[] aboard the Arduino
#                     trunc(value * 256) + 128)  # scale to 8-bit byte

# For input on how to move left and right ("strafing")
@get("/movement/left-right/<gamepadValue>")
def straf_left_right(gamepadValue):
    # insert code to fire motors appropriately.


run(host='localhost', port=8085)
