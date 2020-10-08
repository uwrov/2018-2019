import json
import random
import math
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

#player ids generated on the server
client_id_generator = 1 #first id (increment by one)
# list of players with their respective hand and money
player_list = []

HOST_IP = "localhost"
HOST_PORT = "4000"

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")


class Player:
    def __init__(self, name, id=-1):
        self.id = id
        self.name = name
        self.ready = 0
        self.money = 20
        self.stock_hand = []
        self.action_hand = []


    def __str__(self):
        return str(self.name + " " + str(self.money) + " " + str(self.stock_tostring()) + " " +
                   str(self.action_tostring()) + " " + str(self.ready))


    def stock_tostring(self):
        hand = "["
        for card in self.stock_hand:
            hand += card.company + " " + str(card.amount) + " "
        return hand + "]"


    def action_tostring(self):
        hand = "["
        for card in self.action_hand:
            hand += card + ", "
        return hand[:-2] + "]"


@sio.on("Generate ID")
def gen_id():
    global client_id_generator, player_ids
    emit('ID Confirm', client_id_generator)
    client_id_generator += 1


@sio.on("Previous ID")
def confirm_id(id):
    player = get_player_by_id(int(id))
    if player is None:
        gen_id()
    else:
        emit('ID Confirm', id)



@sio.on("Create Player")
def create_player(data):
    global player_list, player_ready
    player = get_player_by_id(data["id"])
    if player is None:
        temp = Player(data["name"], data["id"])
        player_list.append(temp)
        send_players_data()
    else:
        player.name = data["name"]
        send_players_data()


@sio.on("Ready")
def set_ready(data):
    global player_ready
    print(data)
    player = get_player_by_id(data["id"])
    player.ready = 1
    send_players_data()


@sio.on("Not Ready")
def set_not_ready(data):
    global player_ready
    player = get_player_by_id(data["id"])
    player.ready = 0
    send_players_data()


@sio.on("Get Players")
def send_players_data():
    emit('Player List', [ob.__dict__ for ob in player_list], broadcast=True)
    return True


def get_player_by_id(id):
    for x in player_list:
        if x.id == id:
            return x
    return None


def main():
    sio.run(app, host=HOST_IP, port=HOST_PORT)


if __name__ == '__main__':
    main()
