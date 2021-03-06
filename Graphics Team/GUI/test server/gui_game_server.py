import json
import random
import math
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import matplotlib
import matplotlib.pyplot as plt
import base64
import operator

#need to disable to use plt.show()
matplotlib.use('Agg')

HOST_IP = "localhost"
HOST_PORT = "4000"

DECK_FILE = "deck.txt"
ACTION_FILE = "action_cards.txt"

MAX_TURNS = 10

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")
# list of all cards
market_deck = []

# list of all used cards
stock_graveyard = []
action_graveyard = []

# list of players with their respective hand and money
player_list = []

# list of card in available in market
market_cards = []

# what turn it is in the game. ends at turn 10
turn_index = 1
# what player's turn it is in the turn
player_index = -1

# list of unique company names
company_names = set()

fluctuation_deck = []
stock_market = {}

action_deck = []

playing_game = False
show_results = False

client_id_generator = 1

BASE_PRICE = 3
xaxis = [1]

stocks_over_time = {}
end_player_results = []



class Player:
    def __init__(self, name, id=-1):
        self.name = name
        self.ready = 0
        self.money = 100
        self.stock_hand = []
        self.action_hand = []
        self.id = id

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

    def to_dict(self):
        return {
            "name": self.name,
            "ready": self.ready,
            "money": self.money,
            "stock_hand": [obj.__dict__ for obj in self.stock_hand],
            "action_hand": self.action_hand,
            "id": self.id
        }


class StockCard:
    def __init__(self, name, amount, scalar):
        self.company = name
        self.amount = amount
        self.scalar = scalar
        self.price = 0

    def update_price(self, market_val):
        self.price = math.ceil(int(self.amount) * float(self.scalar) * int(market_val))
        if self.price == 0:
            self.price = BASE_PRICE


    def __str__(self):
        return self.company + " " + self.amount + " " + str(self.price)


class MarketCard:
    def __init__(self):
        self.change_in_stock = {}

class Player_Results:
    def __init__(self, id, net_worth, rank):
        self.name = get_player_by_id(id).name
        self.id = id
        self.net_worth = net_worth
        self.rank = rank

# Game Rules
# Each turn you can buy a stock or a bond
# Each turn you can sell to the general market or trade with a player
# Winner is person with most money!
# rules to be extended

# creates the deck of cards by reading the deck.txt file. Each line corresponds
# to a new cards with the order: comany amount price.
# The deck size is 50
def check_to_start():
    global player_list
    if len(player_list) < 2:
        send_error("Not enough players")
    else:
        for player in player_list:
            if player.ready == 0:
                return
        init_game()  #start the game internaly on the server
        send_game_data()

def create_deck():
    with open(DECK_FILE) as file:
        lines = file.readlines()
        for line in lines:
            details = line.split(' ')
            company_names.add(details[0])
            market_deck.append(StockCard(details[0], details[1], details[2]))
        for i in range(20):
            card = MarketCard()
            for company in company_names:
                card.change_in_stock[company] = random.randint(-5, 5)
            fluctuation_deck.append(card)
    with open(ACTION_FILE) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            action_deck.append(line)


def shuffle_decks():
    random.shuffle(market_deck)
    random.shuffle(action_deck)


# resets the Game
def return_all_cards():
    global stock_graveyard, market_deck, market_cards, action_deck, action_graveyard
    for p in player_list:
        stock_graveyard += p.stock_hand
        p.money = 100
        p.stock_hand = []
        action_graveyard += p.action_hand
        p.action_hand = []
    market_deck += stock_graveyard + market_cards
    action_deck += action_graveyard
    stock_graveyard = []
    market_cards = []
    action_graveyard = []
    random.shuffle(action_deck)
    for player in player_list:
        for i in range(0, 5):
            player.action_hand.append(action_deck.pop())
    for name in company_names:
        stock_market[name] = 5


def add_player(name, id=-1):
    player_list.append(Player(name, id))


def change_stock():
    global fluctuation_deck, stock_market, xaxis
    change_card = fluctuation_deck.pop()
    for name in change_card.change_in_stock:
        stock_market[name] += change_card.change_in_stock[name]
        if stock_market[name] < 0:
            stock_market[name] = 0
        stocks_over_time[name].append(stock_market[name])
    xaxis.append(int(turn_index))
    update_market_card_price()


def update_market_card_price():
    for card in market_cards:
        card.update_price(stock_market[card.company])


def next_turn():
    global market_deck, market_cards, turn_index, player_index

    if turn_index > (MAX_TURNS - 1) and player_index >= len(player_list) - 1:
        end_game()
    else:
        while len(market_cards) < 5:
            market_cards.append(market_deck.pop(0))

        update_market_card_price()

        if player_index < len(player_list) - 1:
            player_index += 1
        else:
            player_index = 0
            turn_index += 1
            if turn_index == MAX_TURNS:
                send_pop_up("Last Turn!")
            change_stock()

        create_stock_graph()


def buy_card(move):
    global market_cards
    if move >= 0 and move < len(market_cards):
        card = market_cards.pop(move)
        if player_list[player_index].money >= int(card.price):
            player_list[player_index].money -= int(card.price)
            player_list[player_index].stock_hand.append(card)
            return 1;
        else:
            market_cards.append(card)
            return 0;
    else:
        return 0;


def sell_card(move):
    global market_cards
    if move >= 0 and move < len(player_list[player_index].stock_hand):
        card = player_list[player_index].stock_hand.pop(move)
        stock_graveyard.append(card)
        card.update_price(stock_market[card.company])
        player_list[player_index].money += int(card.price)
        return 1;
    else:
        return 0;

def print_market_cards():
    for card in market_cards:
        print(card.company + " " + str(card.amount) + " " + str(card.price), end=" | ")

def init_stock_record():
    for name in company_names:
        stocks_over_time[name] = [5]

# API Methods

# Request format: HOST_IP:port/getCards
# Request type: GET
# Returned Data Format: JSON
# Description: Returns current cards in the market in JSON Format
# Example Response: [{"Company": "Amazoom", "Amount": "1", "Price": "3"}]
@sio.on("Get Market")
def send_market_cards():
    emit('Market Cards', [ob.__dict__ for ob in market_cards], broadcast=True)
    return True


# Request format: HOST_IP:port/getPlayers
# Request type: GET
# Returned Data Format: JSON
# Description: Returns the player's current cards and money in JSON Format
# Example Response: [{"Name": "Andrew", "Money": "100", "Hand": [...]}]
@sio.on("Get Players")
def send_players_data():
    emit('Player List', [ob.to_dict() for ob in player_list], broadcast=True)
    return True

@sio.on("Get Stock Market")
def send_stock_market():
    emit('Stock Market', stock_market, broadcast=True)
    return True


@sio.on("Get Player Index")
def send_player_index():
    emit('Player Index', player_index, broadcast=True)
    emit('Game Turn', turn_index, broadcast=True)
    return True

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
    player = get_player_by_id(data["id"])
    player.ready = 1
    check_to_start()
    send_players_data()


@sio.on("Not Ready")
def set_not_ready(data):
    global player_ready
    player = get_player_by_id(data["id"])
    player.ready = 0
    send_players_data()

def get_player_by_id(id):
    for x in player_list:
        if x.id == id:
            return x
    return None

# To be implemented
def action_phase():
    global playing_game
    print(player_list[player_index].name + " its your turn! What is your action? ")
    print(player_list[player_index])
    action = input()
    if action == "exit":
        return False
    if int(action) != -1:
        action_card = player_list[player_index].action_hand.pop(int(action))
        print(player_list[player_index])
        print(player_list[player_index].name + " just played " + action_card)
        return True
# move represents the market card the player wants to buy
# if move == -1 then the player wants to skip buying a cards
# 0 represents the first card in the market, 1 represents the second card etc...
# def market_phase():
#     print(player_list[player_index].name + " what stock do you want to buy? ")
#     print_market_cards()
#     buy_move = input()
#     buy_move = int(buy_move)
#     buy_card(buy_move)
#     print_market_cards()
#     print(player_list[player_index].name + " what stock do you want to sell? ")
#     print(player_list[player_index])
#     sell_move = input()
#     sell_move = int(sell_move)
#     sell_card(sell_move)
#     print(player_list[player_index])


# move represents the market card the player wants to buy
# if move == -1 then the player wants to skip buying a cards
# 0 represents the first card in the market, 1 represents the second card etc...
@sio.on("Buy Card")
def buy_player_card(data):
    if data["id"] == player_list[player_index].id:
        if(buy_card(int(data["target"])) != 1):
            send_error("Not Enough Money!")
    send_game_data()


@sio.on("Sell Card")
def sell_player_card(data):
    if data["id"] == player_list[player_index].id:
        if(sell_card(int(data["target"])) != 1):
            send_error("Error when selling!")
    send_game_data()

@sio.on("End Turn")
def end_turn(data):
    if data["id"] == player_list[player_index].id:
        next_turn()
    else:
        send_error("Not your turn!")
    send_game_data()

def send_error(msg):
    emit("error", {"message": msg })

def send_pop_up(msg):
    print("POPPING UP!")
    emit("Pop Up", {"message": msg }, broadcast=True)

@sio.on("Get Game State")
def send_game_state():
    emit("Game State", {"state": playing_game, "results": show_results}, broadcast=True)

@sio.on("Update Request")
def send_game_data():
    send_market_cards()
    send_players_data()
    send_stock_market()
    send_player_index()
    send_game_state()

@sio.on("Get Stock Graph")
def create_stock_graph():
    try:
        plt.close()
    except Exception as e:
        print()
    for name in stocks_over_time:
        stock = plt.plot(xaxis, stocks_over_time[name], label=name)
    plt.legend(loc='upper left')
    plt.xticks(xaxis)
    plt.xlabel("Stock Per Turn", fontsize=20)
    plt.ylabel("Stock Price", fontsize=20)
    plt.title("Stonks Go Zoom", fontsize=20)
    plt.grid()
    plt.savefig('figure.png')
    #plt.show()
    image = open('figure.png', 'rb').read()
    img = base64.b64encode(image);
    emit("Stock Graph", {'image': img}, broadcast=True)

def init_game():
    global playing_game, player_index, turn_index
    turn_index = 1
    player_index = -1
    shuffle_decks()
    init_stock_record()
    return_all_cards()
    next_turn()
    playing_game = True

def end_game():
    global playing_game, show_results
    show_results = True
    calc_results()
    #player_list.clear()
    send_game_state()
    send_results()

@sio.on("Reset Server")
def reset_server():
    global playing_game, show_results, xaxis, stocks_over_time
    return_all_cards()
    show_results=False
    playing_game=False
    player_list.clear()
    end_player_results.clear()
    xaxis = [1]
    stocks_over_time = {}
    send_game_data()

@sio.on("Get Results")
def send_results():
    emit("End Results", [p.__dict__ for p in end_player_results], broadcast=True)

def calc_results():
    global end_player_results
    player_net_worth = {}
    rank = 1
    for player in player_list:
        total = 0
        for stock in player.stock_hand:
            total = total + int(stock.amount) * int(stock_market[stock.company])
        total = total + player.money
        player_net_worth[player.id] = total
    sorted_d = dict(sorted(player_net_worth.items(), key=operator.itemgetter(1),reverse=True))
    for player in sorted_d:
        end_player_results.append(Player_Results(player, sorted_d[player], rank))
        rank = rank + 1


def test():
    create_deck()
    init_stock_record()
    shuffle_decks()
    return_all_cards()
    next_turn()
    next_turn()
    next_turn()
    #create_stock_graph()
    sio.run(app, host=HOST_IP, port=HOST_PORT)
    create_stock_graph()

def main():
    create_deck()
    sio.run(app, host=HOST_IP, port=HOST_PORT)

main()
#test()
