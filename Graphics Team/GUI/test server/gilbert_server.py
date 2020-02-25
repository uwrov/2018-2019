from bottle import get, put, route, run, template, request
import bottle, json

list_commands = []

@route('/test_command')
def get_form():
	return render_commands() + '''
			<form action="/commands" method="post">
				Name: <input name="name" type="text" />
				Params: <input name="params" type="text">
				<input value="Post" type="Submit">
			</form>
		'''

@route('/commands')
def get_commands():
	return json.dumps(list_commands)

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

def store_command(separated):
	temp = {}
	for pair in separated:
		temp[pair[0].strip()] = pair[1].strip()
	list_commands.append(temp)

def render_commands():
    result = "<p>"
    for index in list_commands:
        result += str(index) + "<br>"
    result += "</p>"
    return result

run(host='localhost', port=8080)
