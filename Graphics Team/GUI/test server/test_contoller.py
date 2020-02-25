from bottle import route, run, template, request

contoller_values = ["a" = 0; "b" = 1; "x" = 2; "y" = 3; "r_x" = 4; "r_y" = 5; "l_x" = 6; "l_y" = 7];

@route('/controller')
def get_comments():
	return render_data() + '''
			<form action="/comment" method="post">
				a: <input name="a" type="button" />
				Name: <input name="name" type="text" />
				<input value="Submit" type="submit" />
			</form>
		'''

@route('/controller', method="post")
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




@route('/controller', method="post")
def post_controller():
	if type="button":
		return
	else:
		return

run(host='localhost', port=8080)
