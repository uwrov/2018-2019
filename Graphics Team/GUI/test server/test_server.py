from bottle import route, run, template, request

comments = [];
controller_values = {"a": 0, "b": 0, "x": 0, "y": 0, "r_x": 0, "r_y": 0, "l_x": 0, "l_y": 0}

@route('/hello/<name>')
def index(name):
	return template('<b>Hello {{name}}</b>!', name=name)


@route('/comment')
def get_comments():
	return '''
			<form action="/comment" method="post">
				Comment: <input name="comment" type="text" />
				Name: <input name="name" type="text" />
				<input value="Submit" type="submit" />
			</form>
		'''

@route('/comment', method="post")
def post_comment():
	comment = request.forms.get('comment')
	name = request.forms.get('name')
	temp_com = [comment, name]
	comments.append(temp_com)

	return get_comments() + all_comments()

def all_comments():
	formatted = "";
	for comment in comments:
		formatted += "<p>" + comment[0] + "   - " + comment[1] + "</p>"
	return formatted


@route('/controller')
def get_controller():
	return render_data() + '''
			<form action="/controller" method="post">
				Name: <input name="name" type="text" />
				Value: <input name="value" type="number">
				<input value="Post" type="Submit">
			</form>
		'''

@route('/controller', method="post")
def post_controller():
	name = request.forms.get('name')
	value = request.forms.get('value')
	controller_values[name] = value
	return get_controller()

def render_data():
	result = "<p>";
	for key in controller_values:
		result += key + " = " + str(controller_values[key]) + "<br>"
	result += "</p>"
	return result

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

run(host='localhost', port=8080)
