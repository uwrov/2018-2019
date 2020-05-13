from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def test_connect():
    send("hello", namespace='/')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('message', {'hello': "Hello"})
    return True

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    return True

@socketio.on('connect')
def connect_handler():
    print('received message: ' + message)
    send("You connected!")

if __name__ == '__main__':
    socketio.run(app, host="localhost", port="8080")



# server is at localhost:8080

# ws://localhost:8080
# http://
