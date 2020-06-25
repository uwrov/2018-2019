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


@sio.on("Create Player")
def create_player(data):
    global player_list, player_ready
    player = get_player_by_id(data["id"])
    if player is None:
        temp = Player(data["name"], data["id"])
        player_list.append(temp)
        emit("Player List", [ob.__dict__ for ob in player_list])
    else:
        player.name = data["name"]
        emit("Player List", [ob.__dict__ for ob in player_list])


@sio.on("connect")
def conn():
    global client_id_generator, player_ids
    emit ('connected', client_id_generator)
    client_id_generator += 1


@sio.on("Ready")
def set_ready (data):
    global player_ready
    player_ready[data["id"]] = 1


@sio.on("Not Ready")
def set_not_ready (data):
    global player_ready
    player = get_player_by_id(data["id"])
    player.ready[data["id"]] = 0


@sio.on("Get Players")
def send_players_data():
    emit('Player Data', [ob.__dict__ for ob in player_list])
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
