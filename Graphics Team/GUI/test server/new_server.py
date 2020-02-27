from bottle import get, put, route, run, template, request
import bottle

list_commands = [

]

@route('/command')
def get_command():
	return render_commands() + '''
			<form action="/command" method="post">
				Name: <input name="name" type="text" />
				Params: <input name="params" type="text">
				<input value="Post" type="Submit">
			</form>
		'''
@route('/command', method="post")
def change_state():
    name = request.forms.get('name')
    params = request.forms.get('params')
    separated = find_params(params)
    separated.insert(0, name)
    try:
        store_command(separated)
    except:
        bottle.HTTPError
    return get_command()

def find_params(params):
	return params.split(',')

def store_command(separated):
    # component is the key (a string) for the dictionary controller_state.
    # state is a string that represents a float (the joystick value
    # transmitted from the web interface)
    list_commands.extend([separated])

def render_commands():
    result = "<p>"
    for index in list_commands:
        result += str(index) + "<br>"
    result += "</p>"
    return result

run(host='localhost', port=8080)
