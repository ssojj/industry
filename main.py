import json, requests, os, keyboard

#clear the console
def clear():
	os.system('cls')

#print the help message
def print_help():
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
	
def print_menu():
	print('Industry\n')
	print('1. Play')
	print('2. Help')
	print('Esc. Exit')
	print('Press a key.')
	
def get_value(value):
	if (value == 'KING' or value == 'QUEEN' or value == 'JACK'):
		return 10
	elif (value == 'ACE'):
		return 1
	else:
		return int(value)

#main loop
def main():
	#variables
	need_help = False
	state = 'menu'
	hand = []
	housing = 0
	offices = 0
	banks = 0
	factories = 0
	build_actions = 0
	time = 0
	score = 0
	#One deck for testing make this empty before publishing
	deck_id = 'ytvib1mr6wi0' 
	request = None
	json = ''
	offset = 0
	
	while (state != 'end'):
	
		#menu
		while (state == 'menu'):
			#print main menu
			clear()
			if (need_help):
				print_help()
			else:
				print_menu()
			
			
			event = keyboard.read_event()
			#there are events on key down and key up
			#I only want down so players don't select
			#things on key up as well
			if(event.event_type == 'down'):
				if (event.name == '1'):
					state = 'setup'
				elif (event.name == '2'):
					need_help = True
				elif (event.name == 'esc'):
					state = 'end'
		
		#setup
		if (state == 'setup'):
			
			#go through a setup stage to reset variables and
			#comunicate with the API
			
			hand = []
			score = 2
			time = 20
			housing = 0
			offices = 1
			banks = 0
			factories = 1
			build_actions = 1
			
			if (deck_id):
				request = requests.get('https://deckofcardsapi.com/api/deck/' + deck_id + '/shuffle/')
			else:
				request = requests.get('https://deckofcardsapi.com/api/deck/new/')
				json = request.json()
				deck_id = json['deck_id']
				
			request = requests.get('https://deckofcardsapi.com/api/deck/' + deck_id + '/draw/?count=3')
			json = request.json()
			for each in json['cards']:
				hand.append(each)
				
			state = 'game'
		
		#game
		while (state == 'game'):
			#print information for the player
			clear()
			print('Industry\n')
			print('Turns left: ' + str(time) + ' | Build Actions left: ' + str(build_actions) + ' | Score: ' + str(score))
			print('Housing/Hearts: ' + str(housing) + ' | Offices/Spades: ' 
				+ str(offices) + ' | Banks/Clubs: ' + str(banks) 
				+ ' | Factories/Diamonds: ' + str(factories) + '\n')
				
			#fetch hand information
			hand_display = ''
			for card in hand:
				hand_display += card['code']
				hand_display += ', '
			hand_display = hand_display[:-2]
						
			print('Hand: ' + hand_display + '\n')
			if (build_actions > 0):
				print('1. Play a card\n2. End turn\nEsc. Exit game')
			else:
				print('1. End Turn\nEsc. Exit game') 
			
			#wait for player selection
			event = keyboard.read_event()
			if(event.event_type == 'down'):
				if (event.name == 'esc'):
					state = 'end'
				elif (event.name == '1'):
					if (build_actions > 0):
						state = 'play'
						offset = 0
					else:
						state = 'turn'
				elif (event.name == '2'):
					if (build_actions > 0):
						state = 'turn'
		
		while (state == 'play'):
			
			#variables
			temp_hand = []
			inner_state = None
			selection = []
			remaining_cost = 10
			arrow = '      '#6 spaces
			
			#rebuild hand so that we can change stuff
			#without effecting the original hand
			for each in hand:
				temp_hand.append(each)
		
			#print information for the player
			clear()
			print('Industry\n')
			print('Turns left: ' + str(time) + ' | Build Actions left: ' + str(build_actions) + ' | Score: ' + str(score))
			print('Housing/Hearts: ' + str(housing) + ' | Offices/Spades: ' 
				+ str(offices) + ' | Banks/Clubs: ' + str(banks) 
				+ ' | Factories/Diamonds: ' + str(factories) + '\n')
			

			#get cards 
			hand_display = ''
			for card in temp_hand:
				hand_display += card['code']
				hand_display += ', '
			hand_display = hand_display[:-2]
			
			#print the arrow to select a card
			print('Hand: ' + hand_display)
			for i in range(offset):
				arrow += '    '#4 spaces
			arrow += '^'
			print(arrow + '\n')
			print('Use the left and right arrow to select a card')
			print('1. Select card\n2. Cancel Selection\nEsc. Exit game')
			
			#wait for player choice
			event = keyboard.read_event()
			if(event.event_type == 'down'):
				if (event.name == 'esc'):
					state = 'end'
				elif (event.name == '1'):
					selection.append(temp_hand.pop(offset))
					offset = 0
					remaining_cost = 10 - banks
					inner_state = 'pay'
				elif (event.name == '2'):
					state = 'game'
				elif (event.name == 'right'):
					if (offset < len(temp_hand)-1):
						offset += 1
				elif (event.name == 'left'):
					if (offset > 0):
						offset -= 1
			
			
			while (inner_state == 'pay'):
				arrow = '      '#6 spaces
				payment = []
				if (remaining_cost < 0):
					remaining_cost = 0
				
				clear()
				print('Industry\n')
				print('Turns left: ' + str(time) + ' | Build Actions left: ' + str(build_actions) + ' | Score: ' + str(score))
				print('Housing/Hearts: ' + str(housing) + ' | Offices/Spades: ' 
					+ str(offices) + ' | Banks/Clubs: ' + str(banks) 
					+ ' | Factories/Diamonds: ' + str(factories) + '\n')
			
				#print payment information
				print('Card you are paying for: ' + selection[0]['code'])
				print('Remaining cost: ' + str(remaining_cost))
				
				#get payment 
				payment = ''
				for card in selection[1:]:
					payment += card['code']
					payment += ', '
				payment = payment[:-2]
				
				print('Cards you are using to pay: ' + payment)

				#get cards 
				hand_display = ''
				for card in temp_hand:
					hand_display += card['code']
					hand_display += ', '
				hand_display = hand_display[:-2]
			
				#print the arrow to select a card
				print('\nHand: ' + hand_display)
				for i in range(offset):
					arrow += '    '#4 spaces
				arrow += '^'
				print(arrow + '\n')
				print('Use the left and right arrow to select a card')
				if (remaining_cost <= 0):
					print('1. Confirm Payment\n2. Cancel Selection\nEsc. Exit game')
				else:
					print('1. Select card for payment\n2. Cancel Selection\nEsc. Exit game')
				
				#wait for player choice
				event = keyboard.read_event()
				if(event.event_type == 'down'):
					#exit game
					if (event.name == 'esc'):
						inner_state = None
						state = 'end'
					#move pointer right
					elif (event.name == 'right'):
						if (offset < len(temp_hand)-1):
							offset += 1
					#move pointer left
					elif (event.name == 'left'):
						if (offset > 0):
							offset -= 1
					#either select card or confrim selection
					elif (event.name == '1'):
						#check if cost it payed
						if (remaining_cost <= 0):
							#confirm selection and pay
							for each in selection:
								hand.remove(each)
							
							add_to_pile = ''
							for card in selection[1:]:
								add_to_pile += card['code']
								add_to_pile += ', '
							add_to_pile = payment[:-2]
							request = requests.get('https://deckofcardsapi.com/api/deck/' + deck_id + '/pile/discard/add/?cards=' + add_to_pile)
							
							if (selection[0]['suit'] == 'HEARTS'):
								housing += 1
								score += 2
							elif (selection[0]['suit'] == 'SPADES'):
								offices += 1
								score += 1
							elif (selection[0]['suit'] == 'CLUBS'):
								banks += 1
								score += 1
							else:
								factories += 1
								build_actions += 1
								score +=1
							
							build_actions -= 1
							
							inner_state = None
							state = 'game'
						else:
							#select card
							remaining_cost -= get_value(temp_hand[offset]['value'])
							selection.append(temp_hand.pop(offset))
							offset = 0
					elif (event.name == '2'):
						inner_state = None
						state = 'game'

		#maintence between turns
		while (state == 'turn'):
			#end the game if there are no turns left
			if (time <= 0):
				state = 'game_end'
			#setup for next turn otherwise
			else:
				#reduce time
				time -= 1
				
				#give correct amount of build actions for next turn
				build_actions = factories
				
				#draw cards
				request = requests.get('https://deckofcardsapi.com/api/deck/' + deck_id + '/draw/?count=' + str(offices))
				json = request.json()
				for each in json['cards']:
					hand.append(each)
				
				#start next turn
				state = 'game'
		
		while (state == 'game_end'):
			state = 'menu'
main()
