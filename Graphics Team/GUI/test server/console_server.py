import bottle
from bottle import route, run, request, response

consoleOutput = "Console\n"


@route("/getArg")
def getArg():
	response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
	bottle.response.headers['Access-Control-Allow-Origin'] = '*'
	
	return "test"


@route("/getOutput")
def getCommand():
	response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
	bottle.response.headers['Access-Control-Allow-Origin'] = '*'
	return consoleOutput

@route("/console", method="post")
def postToConsole():
	global consoleOutput
	print("p1")
	text_to_add = str(request.forms.get("t"))
	print("p2")
	consoleOutput += "$>" + text_to_add + "\n"
	print("done with post")
	


@route("/error", method="post")
def addError():
	error_message = request.forms.get("error_message")
	consoleOutput += "\n" + "$>" + error_message
	global currArgument
	currArgument+=1
        



	
	

run(host="localhost", port=4000, debug=True)


