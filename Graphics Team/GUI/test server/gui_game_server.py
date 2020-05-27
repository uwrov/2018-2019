# import json
import random
import math
# from flask import Flask, render_template
# from flask_socketio import SocketIO, send, emit


# from bottle import route

HOST_IP = "localhost"
HOST_PORT = "4000"

DECK_FILE = "deck.txt"
ACTION_FILE = "action_cards.txt"

# app = Flask(__name__)
# sio = SocketIO(app)

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
turn_index = 0
# 0 = buying phase 1 = selling phase
turn_phase = 0
# what player's turn it is in the turn
player_index = 0

# list of unique company names
company_names = set()

fluctuation_deck = []
stock_market = {}

action_deck = []


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 20
        self.stock_hand = []
        self.action_hand = []

    def __str__(self):
        return str(self.name + " " + str(self.money) + " " + str(self.stock_tostring()) + " " +
                   str(self.action_tostring()))

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


class StockCard:
    def __init__(self, name, amount, scalar):
        self.company = name
        self.amount = amount
        self.scalar = scalar
        self.price = 0

    def update_price(self, market_val):
        self.price = math.ceil(int(self.amount) * int(self.scalar) * int(market_val))

    def __str__(self):
        return self.company + " " + self.amount + " " + str(self.price)


class MarketCard:
    def __init__(self):
        self.change_in_stock = {}


# Game Rules
# Each turn you can buy a stock or a bond
# Each turn you can sell to the general market or trade with a player
# Winner is person with most money!
# rules to be extended

# creates the deck of cards by reading the deck.txt file. Each line corresponds
# to a new cards with the order: comany amount price.
# The deck size is 50

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


def print_deck():
    for card in market_deck:
        print(card.company, card.amount, card.price)
    for card in fluctuation_deck:
        print(card.change_in_stock)


def shuffle_decks():
    random.shuffle(market_deck)
    random.shuffle(action_deck)


# resets the Game
def set_up_game():
    global stock_graveyard, market_deck, market_cards, action_deck, action_graveyard
    for p in player_list:
        stock_graveyard += p.stock_hand
        p.money = 20
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


def add_player(name):
    player_list.append(Player(name))


# move represents the market card the player wants to buy
# if move == -1 then the player wants to skip buying a cards
# 0 represents the first card in the market, 1 represents the second card etc...
def market_phase():
    global turn_phase
    global market_cards
    print(player_list[player_index].name + " what stock do you want to buy? ")
    print_market_cards()
    buy_move = input()
    buy_move = int(buy_move)
    buy_card(buy_move)
    print_market_cards()
    print(player_list[player_index].name + " what stock do you want to sell? ")
    print(player_list[player_index])
    sell_move = input()
    sell_move = int(sell_move)
    sell_card(sell_move)
    print(player_list[player_index])


def buy_card(move):
    global turn_phase
    global market_cards
    if turn_phase == 0:
        if move != -1 and move < len(market_cards):
            card = market_cards.pop(move)
            if player_list[player_index].money >= int(card.price):
                player_list[player_index].money -= int(card.price)
                player_list[player_index].stock_hand.append(card)
                turn_phase = 1
            else:
                market_cards.append(card)
        else:
            turn_phase = 1


def sell_card(move):
    global turn_phase
    global market_cards
    if turn_phase == 1:
        if move != -1 and move < len(player_list[player_index].stock_hand):
            card = player_list[player_index].stock_hand.pop(move)
            print(card)
            price = card.amount * card.scalar + market_v
            print(card)
            player_list[player_index].money += int(card.price)
            turn_phase = 1
        else:
            turn_phase = 2


def begin_turn():
    global market_deck
    global market_cards
    global turn_index
    global player_index
    global turn_phase

    while len(market_cards) < 5:
        market_cards.append(market_deck.pop(0))

    turn_phase = 0
    if player_index < len(player_list) - 1:
        player_index += 1
    else:
        player_index = 0
        turn_index += 1
        change_stock()


def change_stock():
    global fluctuation_deck
    global stock_market
    change_card = fluctuation_deck.pop()
    for name in change_card.change_in_stock:
        stock_market[name] += change_card.change_in_stock[name]
    update_market_card_price()


def update_market_card_price():
    for card in market_cards:
        card.update_price(stock_market[card.company])


def print_stock_market():
    print(stock_market)


def action_phase():
    print(player_list[player_index].name + " its your turn! What is your action? ")
    print(player_list[player_index])
    action = input()
    if action == "exit":
        return
    if action != 0:
        action_card = player_list[player_index].action_hand.pop(int(action) - 1)
        print(player_list[player_index])
        print(player_list[player_index].name + " just played " + action_card)


def intro():
    print("Market Cards")
    print("--------------------")
    print_market_cards()
    print("--------------------")
    print()

    print("Players: name, money, stocks, actions")
    print("--------------------")
    for player in player_list:
        print(player)
    print("--------------------")
    print()


def print_market_cards():
    for card in market_cards:
        # print(card.company, card.amount, card.price, end=" ")
        print(card.company + " " + str(card.amount) + " " + str(card.price), end=" | ")


# API Methods

# Request format: HOST_IP:port/getCards
# Request type: GET
# Returned Data Format: JSON
# Description: Returns current cards in the market in JSON Format
# Example Response: [{"Company": "Amazoom", "Amount": "1", "Price": "3"}]
# @sio.on("Get Market")
# def get_market_cards():
#     emit('Market Cards', json.dumps(market_cards))
#     return True


# Request format: HOST_IP:port/getPlayers
# Request type: GET
# Returned Data Format: JSON
# Description: Returns the player's current cards and money in JSON Format
# Example Response: [{"Name": "Andrew", "Money": "100", "Hand": [...]}]
# @sio.on("Get Player")
# def get_players_data():
#     emit('Market Cards', json.dumps(player_index))
#     return True
#
#
# @route('/makeAction')
# def can_make_action():
#     return
#
#
# @route('/getStockMarket')
# def get_stock_market():
#     return
#
#
# @route('/getPlayerTurn')
# def get_player_index():
#     return int(player_index)


def main():
    global player_index
    create_deck()
    shuffle_decks()
    add_player('Justin')
    add_player('Andrew')
    add_player('Alex')
    add_player('Chris')

    set_up_game()
    intro()
    playing_game = True

    change_stock()
    while playing_game:
        begin_turn()
        update_market_card_price()
        print_stock_market()
        action_phase()
        market_phase()
        print(player_list[player_index])
        print()


#
    # worth $3
#  boomerberg 1 1       3
#   boomerberg 2 0.9    6
#   boomerberg 3 0.8
#

    print("End results:")
    print("--------------------")
    for player in player_list:
        print(player)
    print("--------------------")
    print()


main()
