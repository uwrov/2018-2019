### Communication between robot and surface system
### Raspberry Pi  <-->  Surface computer w/ Moz. Firefox and HTML GUI

import json
from bottle import get, put, route, run, template
import bottle  ## looks peculiar
from math import trunc, sqrt

class Vector3:
	def __init__(self, x: float = 0.0,
					   y: float = 0.0,
					   z: float = 0.0):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other: 'Vector3') -> 'Vector3':
		if type(other) == Vector3:
			return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other: 'Vector3') -> 'Vector3':
		if type(other) == Vector3:
			return  Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, other) -> 'Vector3':
		if type(other) == float or type(other) == int:
			return Vector3(self.x * other, self.y * other, self.z * other)

	def __truediv__(self, other: 'Vector3' or 'int' or 'float') -> 'Vector3':
		if type(other) == float or type(other) == int:
			return Vector3(self.x / other, self.y / other, self.z / other)

	def normalize(self) -> 'Vector3':
		magnitude = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
		if magnitude == 0:
			return Vector3.zero()
		return self / magnitude;

	def zero() -> 'Vector3':
		return Vector3(0.0, 0.0, 0.0)

auto_mode = 0;
position = Vector3.zero()
velocity = Vector3.zero()
acceleration = Vector3.zero()

target = Vector3.zero()

# Joystick state variables

controller_state = {"rb": 0, "lb": 0, "dup": 0, "ddown": 0, "dleft":0, "dright":0,
	"leftstick": 0, "rightstick": 0, "lstick-x" : 0, "lstick-y" : 0, "rstick-x" : 0, "rstick-y" : 0,
	"ltrigger" : 0, "rtrigger" : 0, "update-required": False,
	"lock_x" : 0, "lock_y" : 0, "lock_z" : 0,
	"target" : Vector3.zero(), "position" : Vector3.zero(),
	"lateral_motor_speeds": [128, 128, 128, 128], "vert_motor_byte": 128}

def state_of(component):
    return controller_state[component]

def store_state(component, state):
    # component is the key (a string) for the dictionary controller_state.
    # state is a string that represents a float (the joystick value
    # transmitted from the web interface)
    controller_state[component] = (state)
    controller_state["update-required"] = True

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


# For input on moving left and right ("strafing")
@get("/movement/dleft/<gamepadValue>")
def strafe_left(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("dleft", gamepadValue)

@get("/movement/dright/<gamepadValue>")
def strafe_right(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("dright", gamepadValue)

# Moving forward and backward
@get("/movement/dup/<gamepadValue>")
def strafe_forward(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("dup", gamepadValue)

@get("/movement/ddown/<gamepadValue>")
def strafe_backwards(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("ddown", gamepadValue)

# Rotating
@get("/movement/right-joystick-x/<gamepadValue>")
def rotate_robot(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rstick-x", gamepadValue)

# Accelerating forward, somewhat in direction of of rotation
@get("/movement/right-joystick-y/<gamepadValue>")
def rotate_robot_forward(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rstick-y", gamepadValue)

#Strafing
@get("/movement/left-joystick-x/<gamepadValue>")
def strafe_robot_side(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("lstick-x", gamepadValue)

# Accelerating forward, somewhat in direction of of rotation
@get("/movement/left-joystick-y/<gamepadValue>")
def strafe_robot_forward(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("lstick-y", gamepadValue)

# Changing Speed
@get("/movement/rt/<gamepadValue>")
def speed_fine(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rtrigger", gamepadValue)

@get("/movement/lt/<gamepadValue>")
def speed_coarse(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("ltrigger", gamepadValue)

	# Moving up and down
@get("/movement/rb/<gamepadValue>")
def vertical_movement_down(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rb", gamepadValue)

@get("/movement/lb/<gamepadValue>")
def vertical_movement_up(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("lb", gamepadValue)

@get("/movement/lstick/<gamepadValue>")
def resetMotorsLeft(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("leftstick", gamepadValue)

@get("/movement/rstick/<gamepadValue>")
def resetMotorsRight(gamepadValue):
    bottle.response.set_header("Access-Control-Allow-Origin", "*")
    store_state("rightstick", gamepadValue)




# This form starts the web server (run() is from bottle)
# run(host='localhost', port=8085)
