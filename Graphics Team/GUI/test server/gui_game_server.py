from bottle import get, put, route, run, template
import bottle, json, random

HOST_IP = "localhost"
HOST_PORT = "4000"

DECK_FILE = "deck.txt"

# list of all cards
deck = []

#list of all used cards
graveyard = []

# list of players with their respective hand and money
player_list = []

# list of card in available in market
market_cards = []

# what turn it is in the game. ends at turn 10
turn_index = 0
# 0 = buying phase 1 = selling phase
turn_phase = 0;
# what player's turn it is in the turn
player_index = 0;


class Player:
	def __init__(self, name):
		self.name = name
		self.money = 20
		self.hand = []


class Card:
	def __init__(self, name, amount, price):
		self.company = name
		self.amount = amount
		self.price = price

#	Game Rules
#	Each turn you can buy a stock or a bond
#	Each turn you can sell to the general market or trade with a player
#	Winner is person with most money!
#	rules to be extended

# creates the deck of cards by reading the deck.txt file. Each line corresponds
# to a new cards with the order: comany amount price.
# The deck size is 50
def create_deck():
	with open(DECK_FILE) as file:
		lines = file.readlines()
		for line in lines:
			details = line.split(' ')
			deck.append(Card(details[0], details[1], details[2]))


def print_deck():
	for card in deck:
		print(card.company, card.amount, card.price, sep =' ')


def shuffle_deck():
	random.shuffle(deck)


# resets the Game
#
def start_game():
	for p in player_list:
		graveyard += p.hand
		p.money = 20
		p.hand = []
	deck += graveyard + market_cards
	graveyard = []
	market_cards = []
	for i in range(0,5):
		market_cards.append(deck.pop(0))
	turn_index = 1
	player_index = 0


def add_player(name):
	player_list.append(Player(name))

# move represents the market card the player wants to buy
# if move == -1 then the player wants to skip buying a cards
# 0 represents the first card in the market, 1 represents the second card etc...
def market_phase(move):
	if turn_phase = 0:
		if move != -1 and move < len(market_cards):
			player = player_list[player_index]
			card = market_cards.pop(move)
			if player.money >= card.price:
				player.money -= card.price
				player.hand.append(card)
				turn_phase = 1
			else:
				market_cards.append(card)
		else:
			turn_phase = 1



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


def main():
	create_deck()
	shuffle_deck()
	print_deck()
