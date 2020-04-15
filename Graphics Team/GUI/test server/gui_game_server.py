from bottle import get, put, route, run, template
import bottle, json


HOST_IP = "localhost"
HOST_PORT = "4000"

players = []
turn_index = 0

class Player:
	def init(name):
		self.name = name
		self.money = 100

class Items:
	def init(name, price):
		self.name = name
		self.price = price

market_items = []


#	Game Rules
#	Each turn you can buy a stock or a bond
#	Each turn you can sell to the general market or trade with a player
#	Winner is person with most money!
#	rules to be extended




