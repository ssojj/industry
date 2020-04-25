import json
import requests
import os
import keyboard

def help():
	os.system('cls')
	print('Industry\n')
	
	print('SET UP: To start the game you are dealt three cards. Each suit '
		+ 'is given a name: spades are offices, diamons are factories, '
		+ 'hearts are housing, and clubs are banks. You start with an '
		+ ' office and factory in play.\n\nTHE TURN: If able, you can pay'
		+ ' to play cards into your city. In this game, cards can be '
		+ 'discarded as money or built as buildings. You may build a '
		+ 'number of buildings on your turn as the number of factories'
		+ 'you have, and each building costs $10, but it $1 cheaper '
		+ 'for each bank played. At the end of each turn you draw '
		+ 'cards equal to the number of offices you have. Housing has '
		+ 'no special function, but is worth double points at the end '
		+ 'of the game.\n\nSPENDING: To use cards as currency, discard '
		+ 'cards until you pay the cost of the building, aces are worth '
		+ '$1, numbers are worth thier amount (ex: a 7 is worth $7), and'
		+ ' all face cards are worth $10.')
	
	print('1. Play')
	print('2. Help')
	print('Esc. Exit')
	print('Press a key.')

def menu(event):
	if (event.name == '1'):
		print('play')
	elif (event.name == '2'):
		help()

def main():
	os.system('cls')
	print('Industry\n')
	print('1. Play')
	print('2. Help')
	print('Esc. Exit')
	print('Press a key.')
	
	keyboard.on_press(menu)
	while True():
	
	
main()
