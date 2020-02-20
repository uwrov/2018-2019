from bottle import route, run, request


consoletext = "Hello"

@route("/console")
def getCommand():
	return consoletext

@route("/console", method="post")
def postToConsole():
	text_to_add = request.forms.get("console")
	consoletext += text_to_add
	print("consoletext")


@route("/error", method="post)
def addError():
	error_message = request.forms.get("error_message")
	
	

run(host="localhost", port=4000)


