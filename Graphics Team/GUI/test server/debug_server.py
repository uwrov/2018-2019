### Communication between robot and surface system
### Raspberry Pi  <-->  Surface computer w/ Moz. Firefox and HTML GUI

import json
from bottle import get, put, route, run, template, request
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
list_commands = [

]

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

@route('/controller')
def get_controller():
	return render_data() + '''
			<form action="/controller" method="post">
				Name: <input name="name" type="text" />
				Value: <input name="value" type="number">
				<input value="Post" type="Submit">
			</form>
		'''
@route('/command')
def get_command():
	return render_commands() + '''
			<form action="/command" method="post">
				Name: <input name="name" type="text" />
				Param1: <input name="param1" type="number">
                Param2: <input name="param2" type="number">
                Param3: <input name="param3" type="number">
                Param4: <input name="param4" type="number">
				<input value="Post" type="Submit">
			</form>
		'''
@route('/command', method="post")
def change_state():
    name = request.forms.get('name')
    param1 = request.forms.get('param1')
    param2 = request.forms.get('param2')
    param3 = request.forms.get('param3')
    param4 = request.forms.get('param4')
    try:
        store_command(name, param1, param2, param3, param4)
    except:
        bottle.HTTPError
    return get_command()

def store_command(name, param1, param2, param3, param4):
    # component is the key (a string) for the dictionary controller_state.
    # state is a string that represents a float (the joystick value
    # transmitted from the web interface)
    list_commands.extend([[name, param1, param2, param3, param4]])

def render_commands():
    result = "<p>"
    for index in list_commands:
        result += str(index) + "<br>"
    result += "</p>"
    return result

@get('/sensor')
def getsensor():
    return json.dumps(sensors)

# For input on moving left and right ("strafing")
@route('/controller', method="post")
def change_state():
	name = request.forms.get('name')
	value = request.forms.get('value')
	try:
	    store_state(name, value)
	except:
		bottle.HTTPError
	return get_controller()

def render_data():
	result = "<p>";
	for key in controller_state:
		result += key + " = " + str(controller_state[key]) + "<br>"
	result += "</p>"
	return result

run(host='localhost', port=8080)
