from bottle import get, put, route, run, template, request
import bottle, json

HOST_IP = "localhost"

list_commands = []

# user inputs a command name and commands with assigned values.
# each command value pair should be assigned with a ":" and all_separated
# by commas.
# Example:   speed:10,direction:up
@route('/test_command')
def get_form():
	return render_commands() + '''
			<form action="/commands" method="post">
				Name: <input name="name" type="text" />
				Params: <input name="params" type="text">
				<input value="Post" type="Submit">
			</form>
		'''

# Request format: HOST_IP:port/commands
# Request type: GET
# Returned Data Format: JSON
# Description: Returns the name and command in JSON Format
# Example Response: [{"Name": "movement", "speed": "10", "direction": "north"}]
@route('/commands')
def get_commands():
	return json.dumps(list_commands)

# Request format: HOST_IP:port/commands
# Request type: POST
# Returned Data Format: Plain Text
# Description: Stores the commands into the list_commands based on the get command
# Example Request: Name: movement | Param: speed:10,direction:north
# Example Response: [{'Name': 'movement', 'speed': '10', 'direction': 'north'}]
@route('/commands', method="post")
def change_state():
    name = request.forms.get('name')
    params = request.forms.get('params')
    separateParams = params.split(',')
    try:
    	all_separated = []
    	for rule in separateParams:
    	    all_separated.append(rule.split(':'))
    except:
    	bottle.error
    all_separated.insert(0, ["Name", name])
    try:
        store_command(all_separated)
    except:
        bottle.HTTPError
    return get_commands()

# Description: deletes the previous and the stores the new command
# 			   into the list_commands as a key and value.
def store_command(separated):
	temp = {}
	list_commands.clear()
	for pair in separated:
		temp[pair[0].strip()] = pair[1].strip()
	list_commands.append(temp)

# Description: prints out what command is stored in the list_commands
def render_commands():
    result = "<p>"
    for index in list_commands:
        result += str(index) + "<br>"
    result += "</p>"
    return result

run(host=HOST_IP, port=8080)
