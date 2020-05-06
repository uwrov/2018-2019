import json
import random

from bottle import route

HOST_IP = "localhost"
HOST_PORT = "4000"

DECK_FILE = "deck.txt"
ACTION_FILE = "action_cards.txt"

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
current_fluct = []

action_deck = []


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 20
        self.stock_hand = []
        self.action_hand = []

    def __str__(self):
        return str(self.name + " " + str(self.money) + " " + str(self.stock_hand) + " " + str(self.action_hand))


class StockCard:
    def __init__(self, name, amount, price):
        self.company = name
        self.amount = amount
        self.price = price

    def __str__(self):
        return self.company + " " + self.amount + " " + self.price


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
    market_deck += stock_graveyard + market_cards
    action_deck += action_graveyard
    stock_graveyard = []
    market_cards = []
    action_graveyard = []
    random.shuffle(action_deck)
    for player in player_list:
        for i in range(0, 5):
            player.action_hand.append(action_deck.pop())


def add_player(name):
    player_list.append(Player(name))


# move represents the market card the player wants to buy
# if move == -1 then the player wants to skip buying a cards
# 0 represents the first card in the market, 1 represents the second card etc...
def market_phase(move):
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
    print(market_cards)


def begin_turn():
    global market_deck
    global market_cards
    global turn_index
    global player_index

    while len(market_cards) < 5:
        market_cards.append(market_deck.pop(0))

    turn_index = 1
    player_index = 0


# API Methods

# Request format: HOST_IP:port/getCards
# Request type: GET
# Returned Data Format: JSON
# Description: Returns current cards in the market in JSON Format
# Example Response: [{"Company": "Amazoom", "Amount": "1", "Price": "3"}]
@route('/getCards')
def get_market_cards():
    return json.dumps(market_cards)


# Request format: HOST_IP:port/getPlayers
# Request type: GET
# Returned Data Format: JSON
# Description: Returns the player's current cards and money in JSON Format
# Example Response: [{"Name": "Andrew", "Money": "100", "Hand": [...]}]
@route('/getPlayers')
def get_players_data():
    return json.dumps(player_list)


@route('/makeAction')
def can_make_action():
    return


@route('/getStockMarket')
def get_stock_market():
    return


def main():
    global player_index
    create_deck()
    shuffle_decks()
    add_player('Justin')
    add_player('Andrew')
    add_player('Alex')
    add_player('Chris')
    set_up_game()
    begin_turn()

    print("Market Cards")
    print("--------------------")
    for card in market_cards:
        print(card.company, card.amount, card.price)

    print("--------------------")
    print()

    print("Players: name, money, stocks, actions")
    print("--------------------")
    for player in player_list:
        print(player)
    print("--------------------")
    print()

    playing_game = True

    while playing_game:
        print(player_list[player_index].name + " its your turn! What is your action? ")
        print(player_list[player_index])
        action = input()
        if action == "exit":
            break
        if action != 0:
            action_card = player_list[player_index].action_hand.pop(int(action) - 1)
            print(player_list[player_index])
            print(player_list[player_index].name + " just played " + action_card)

        print(player_list[player_index].name + " what stock do you want to buy? ")
        print(market_cards)
        stock = input()
        market_phase(int(stock))
        print(player_list[player_index])
        if player_index < len(player_list)-1:
            player_index += 1
        else:
            player_index = 0

    print("End results:")
    print("--------------------")
    for player in player_list:
        print(player)
    print("--------------------")
    print()


main()
