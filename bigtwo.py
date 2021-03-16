#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:56:52 2020

@author: vatnid
"""

# imports
import random
import os

# classes

class Card:    
    def __init__(self, s, r):
        self.suit = s # 0 = S, 1 = H, 2 = C, 3 = D
        self.rank = r # 1 = A, 11 = J, 12 = Q, 13 = K
        self.num = s * 13 + r
        self.name = to_name(s, r)
        self.sort = 0
        if r <= 2:
            self.sort = (r + 10) * 4
        else:
            self.sort = (r - 3) * 4
        self.sort += s*-1 + 4
        
class Player:
    def __init__(self, n):
        self.num = n
        self.deck = []


# functions
        
def to_name(s, r):
    suit = ""
    if s == 0:
        suit = "♠"
    elif s == 1:
        suit = "♥"
    elif s == 2:
        suit = "♣"
    elif s == 3:
        suit = "♦"
    rank = ""
    if r == 1:
        rank = "A"
    elif r == 11:
        rank = "J"
    elif r == 12:
        rank = "Q"
    elif r == 13:
        rank = "K"
    else:
        rank = str(r)
    return rank + suit

def sort_key(elem):
    return elem.sort

def sort(d):
    return sorted(d, key = sort_key)

def next_player(n):
    if n == 4:
        return 1
    else:
        return n + 1


# parse user input
def parse_input(user_input):
    output = []
    inputlist = user_input.split()
    
    for item in inputlist:
        output.append(you.deck[int(item)-1])
    
    output = sort(output)
    return output

def input_valid(user_input):
    
    if not user_input:
        return False
    
    inputlist = user_input.split()
    
    for item in inputlist:
        if not item.isdigit():
            return False
        if int(item) < 1 or int(item) > len(you.deck):
            return False
    
    return True

# combination functions
    
def same_rank(d):
    for i in range(1, len(d)):
        if d[i].rank != d[0].rank:
            return False
    return True

def same_suit(d):
    for i in range(1, len(d)):
        if d[i].suit != d[0].suit:
            return False
    return True

def same_length(d):    
    return len(d) == len(lastplayed[-1])

def is_pair(d):
    return len(d) == 2 and same_rank(d)

def is_toak(d):
    return len(d) == 3 and same_rank(d)

def is_foak(d):
    if len(d) != 5:
        return False
    
    return same_rank(d[0:4]) or same_rank(d[1:])

def is_straight(d):
    if len(d) != 5:
        return False
    
    # 10JQKA
    if d[0].rank == 10 and d[1].rank == 11 and \
    d[2].rank == 12 and d[3].rank == 13 and d[4].rank == 1:
        return True
    
    for i in range(1, len(d)):
        if d[i-1].rank + 1 != d[i].rank:
            return False
    return True
        
def is_flush(d):
    return len(d) == 5 and same_suit(d)

def is_full_house(d):
    if len(d) != 5:
        return False
    return (is_pair(d[0:2]) and is_toak(d[2:])) or \
    (is_toak(d[0:3]) and is_pair(d[3:]))

def is_royal_flush(d):
    return is_straight(d) and is_flush(d)

def get_rank(d):
    # 0 = straight, 1 = flush, 2 = full house, 3 = FOAK, 4 = royal flush
    if len(d) != 5:
        return -1
    if is_royal_flush(d):
        return 4
    elif is_foak(d):
        return 3
    elif is_full_house(d):
        return 2
    elif is_flush(d):
        return 1
    elif is_straight(d):
        return 0   
    else:
        return -1

def is_bigger(d):
    if not lastplayed:
        return True
    
    if prev_player == you:
        return True
    
    prev_deck = lastplayed[-1]
    
    if not same_length(d):
        return False
    
    if len(d) == 1 or len(d) == 2 or len(d) == 3:
        return d[-1].sort > prev_deck[-1].sort
    
    
    if len(d) == 5:
        lastplayed_rank = get_rank(prev_deck)
        d_rank = get_rank(d)
        
        if d_rank > lastplayed_rank:
            return True
        elif d_rank < lastplayed_rank:
            return False
        else:
            if is_straight(d) or is_flush(d):
                return d[-1].sort > prev_deck[-1][-1].sort
            if is_full_house(d):
                if is_toak(prev_deck[0:3]):
                    temp_deck = prev_deck[0:3]
                else:
                    temp_deck = prev_deck[2:]
                if is_toak(d[0:3]):
                    return d[2] > temp_deck[-1]
                else:
                    return d[-1] > temp_deck[-1]
            if is_foak(d):
                if same_rank(prev_deck[0:4]):
                    temp_deck = prev_deck[0:4]
                else:
                    temp_deck = prev_deck[1:]
                if is_foak(d[0:4]):
                    return d[3] > temp_deck[-1]
                else:
                    return d[-1] > temp_deck[-1]
                

def combo_valid(d):
    
    # single
    if len(d) == 1:
        return True
    
    # pair
    if len(d) == 2:
        return is_pair(d)
       
    # three of a kind
    if len(d) == 3:
        return is_toak(d)

    # five cards
    if len(d) == 5:
        if is_royal_flush(d):
            return True
        if is_foak(d):
            return True
        if is_straight(d):
            return True
        if is_flush(d):
            return True
        if is_full_house(d):
            return True
    
    return False
        
    
# print functions

def pdeck(d):
    for i in range(len(d)):
        print(d[i].name, end = " ")

def pnumbers(d):
    for i in range(len(d)):
        print(str(i+1) + " ", end = "")
        if i <= 8:
            print(" ", end = "")
        if d[i].rank == 10:
            print(" ", end = "")

def pdebug():
    print(" ~~~~~~~~~~~~~~~~~~~ DEBUG ZONE ~~~~~~~~~~~~~~~~~~~")
    for i in range(1, 5):
        print("Player " + str(i) + ": ", end = "")
        pdeck(player[i].deck)
        print()
    print(" ~~~~~~~~~~~~~~~~~~~ DEBUG ZONE ~~~~~~~~~~~~~~~~~~~")

def display():
    pdebug()
    print()
    #print("You are Player " + str(you.num))
    print("Current turn: Player " + str(turn))
    if lastplayed:
        print("Last played: ", end = "")
        pdeck(lastplayed[-1])
        print(" by Player " + str(prev_player.num))
        print()
    print("Your cards:")
    pdeck(you.deck)
    print()
    pnumbers(you.deck)
    print("← Enter these numbers below")
    print()
    

###############################################

os.system("clear")

# initialize game variables
turn = 1

# initialize deck
deck = []
for i in range(4):
    for j in range(1, 14):
        deck.append(Card(i, j))

# remember 3 of diamonds
tod = deck[41]

# initialize last played
lastplayed = []

# initialize players
player = []
player.append(Player(0)) # placeholder player
prev_player = player[0] # previous player
for i in range(1, 5):
    player.append(Player(i))
#you = player[random.randint(1, 4)] # random player



# shuffle cards
random.shuffle(deck)

# deal cards
i = 1
while deck:
    player[i].deck.append(deck.pop(0))
    i = next_player(i)

# sort cards
for i in range(1, 5):
    player[i].deck = sort(player[i].deck)


# start game

for i in range(1,5):
    if tod in player[i].deck:
        turn = i
    
you = player[turn]
game_end = False
while not game_end:
    you = player[turn]
    turn_end = False
    os.system("clear")
    display()
    while not turn_end:
            user_input = input("Enter cards (separated by space) or type \"pass\":\n")
            if user_input == "pass":
                turn = next_player(turn)
                turn_end = True
            elif input_valid(user_input):
                playing = parse_input(user_input)
                print("You played: ", end = "")
                pdeck(playing)
                print()
                if combo_valid(playing):
                    if is_bigger(playing):
                        prev_player = you
                        lastplayed.append(playing)
                        for item in playing:
                            if item in you.deck:
                                you.deck.remove(item)
                        turn = next_player(turn)
                        turn_end = True
                        if not you.deck:
                            game_end = True
                    else:
                        print("Non-matching combination! Try again.")
                else:
                    print("Invalid combination! Try again.")
            else:
                print("Invalid input! Try again.")
else:
    print("Game over! Player " + str(you.num) + " won.")