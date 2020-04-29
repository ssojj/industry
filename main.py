import json, requests, os, keyboard

#clear the console
def clear():
	os.system('cls')

#print the help message
def help():
	clear()
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
		+ ' all face cards are worth $10.\n')
	
	print('1. Play')
	print('2. Help')
	print('Esc. Exit')
	print('Press a key.')

#main loop
def main():
	state = 'menu'
	hand = []
	housing = 0
	offices = 0
	banks = 0
	factories = 0
	time = 0
	score = 0
	deck_id = ""
	request = None
	
	clear()
	print('Industry\n')
	print('1. Play')
	print('2. Help')
	print('Esc. Exit')
	print('Press a key.')
	
	while (state != 'end'):
	
		#menu
		while (state == 'menu'):
			event = keyboard.read_event()
			if(event.event_type == 'down'):
				if (event.name == '1'):
					state = 'setup'
				elif (event.name == '2'):
					help()
				elif (event.name == 'esc'):
					state = 'end'
					
		if (state == 'setup'):
			score = 0
			time = 10
			housing = 0
			offices = 1
			banks = 0
			facotires = 1
			
			request = requests.get('https://deckofcardsapi.com/api/deck/new/')
			
			state = 'play'
		
		#play
		while (state == 'play'):
			clear()
			print('Industry\n')
			
main()
