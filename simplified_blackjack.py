#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Start by importing the random module for dealing.
import random

#Define global variables and the boolean condition to make the game run
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King','Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

#Define the Card class
class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank+ " of "+self.suit
    
#Create the Deck, shuffle, and deal
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return "The deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
#Create the Hand and adjust for Aces
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card) #from Deck.deak --> single Card(suit,rank)
        self.value += values[card.rank]
        
        #tracking aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        
        #Ace is already considered to be an 11
        #If total value > 21 and we still have an Ace, change the Ace to = 1 instead
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
#Considering the money, we start with a total of 100 and add or subtract the bet from that.
class Chips:
    
    def __init__(self,total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
#Define the game functions now
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("How many chips are ya bettin pardner? "))
        except:
            print("Sorry bout that, try again with one'a them integers up to 100.")
        else:
            if chips.bet > chips.total:
                print("Fraid the House won't cover that bet for ya. You only have {}".format(chips.total))
            else:
                break
                
#Make the player take a single card hit
def hit(deck,hand):
    
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
    
#Ask the player if they want to hit or stand
#This is just one method that made sense and seemed clear to me.
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input("Hit or stand? Enter h or s. \n")
        
        if x[0].lower() == 'h':
            hit(deck,hand)
            
        elif x[0].lower() == 's':
            print("Player says Stand. Dealer's turn.")
            playing = False
        
        else:
            print("Sorry Pardner, I don't speak your language. Type s or h to stand or hit. \n")
            continue
            
        break
        
#Show some or all of the cards
def show_some(player,dealer):
    
    print("\nDealer's Hand:")
    print(" <card hidden> ")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep = '\n ')
    
def show_all(player,dealer):
    
    print("\nDealer's Hand", *dealer.cards, sep = '\n ')
    print("Dealer's Hand = ", dealer.value)
    print("Player's Hand", *player.cards, sep = '\n ')
    print("Player's Hand = ", player.value)
    
#Define winning, losing, and tying conditions
def player_busts(player,dealer,chips):
    print("Sorry pal, yer busted.")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("It's yer lucky day! We have a winner!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("The House is bust. Player wins!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("It just ain't yet lucky night. The House wins.")
    chips.lose_bet()
    
def push(player,dealer):
    print("You tied with the House. That right there is called a 'push.'")
    
#This is the long part - game logic.

while True:
    # Print an opening statement
    print("Howdy! Welcome to Blackjack. Yer bankroll is 100 chips. This will be reset as your total every game.")

    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
         
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
    
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    #This is a casino rule called "soft 17"
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
     
        # Show all cards
        show_all(player_hand,dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
           
    # Inform Player of their chips total 
    print("\n Your total bankroll for this game is: {}".format(player_chips.total))
    
    # Ask to play again
    new_game = input("Go another round, Pardner? y/n \n")
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for the game, then. See ya round.")

        break



# In[ ]:




