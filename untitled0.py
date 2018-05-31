# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 23:24:38 2018

@author: Robin
"""


from __future__ import unicode_literals
from __future__ import division
from poker import Suit
import time
import re
import random

list(Suit)  #Suit is a class 

Suit.CLUBS < Suit.DIAMONDS

from poker import Rank
list(Rank)      #Rank is a class 


from poker import Card
list(Card)
Card.make_random()

#Implementing a deck

deck = list(Card)
Card('As') > Card('Ks')

import random
random.shuffle(deck)

flop = [deck.pop() for __ in range(3)]
turn = deck.pop()
river = deck.pop()


#Operations with Hands and Combos

from poker.hand import Hand, Combo
 
a = list(Hand)
len(a)  #169 Hands 

Combo('7s6s') > Combo('6d5d')

#Ranges
from poker import Range
Range('XX').to_ascii()
print(Range('22+ A2+ KT+ QJs+ 32 42 52 62 72').to_ascii())



#Hand history parsing
from poker.room.pokerstars import PokerStarsHandHistory
# First step, only raw hand history is saved, no parsing will happen yet
hh = PokerStarsHandHistory(HAND1)

#hh = PokerStarsHandHistory.from_file('C:\\Users\\Robin\\Desktop\\pkr2\\poker-1\\tests\handhistory\\2hand.txt')

# You need to explicitly parse. This will parse the whole hh at once.
hh.parse()

#date in type: datetime
a = hh.date

#identification number of the hand
b = hh.ident

#what type was the game
c = hh.game_type

#what identification number has the tournament
d = hh.tournament_ident

#in what level, the hand appears
e = hh.tournament_level

#what currency 
f = hh.currency

#buy-in for the tournament
g = hh.rake

#what type of game was it 
h = hh.game

#what limit?
i = hh.limit

#how big was the small blind?
j = hh.sb

#how big was the big blind?
k = hh.bb

#date
l = hh.date

#what was the name of the table
m = hh.table_name

#how high is the amount of the maximum players?
n = hh.max_players

#which position was the button?
o = hh.button



##########     START TO ANALYZE THE HAND    ##########

dec = 1             #Number of our decision
addWe = 0           #what we have add to the pot so far
high = []           #empty list to get the highest amount being bet so far



#Hand history parsing
from poker.room.pokerstars import PokerStarsHandHistory
# First step, only raw hand history is saved, no parsing will happen yet
hh = PokerStarsHandHistory(HAND1)

#hh = PokerStarsHandHistory.from_file('C:\\Users\\Robin\\Desktop\\pkr2\\poker-1\\tests\handhistory\\2hand.txt')

# You need to explicitly parse. This will parse the whole hh at once.
hh.parse()

#who and where we are?
p = hh.hero



#what we have?
p.combo





#what is our position
p.seat

#what is our positon regarding to the button (utg, utg+1, etc.)
hh.button.seat
a = hh.players
aa = sum([a,a], [])

t = 0
for i in range(len(aa)):
    #i = 0
    if aa[i].seat == hh.button.seat:
        t = 0
    else:
        if 'Empty Seat' not in a[i].name:
            if aa[i].name != hh.hero.name:
                t += 1
            else:
                t = t + 1
                break


#how many players are on the table at the moment
pl = 0
for i in range(hh.max_players):
    if 'Empty Seat' not in a[i].name:
        pl += 1



#add further q/ positions
#if q == 7:
#    if t == 1:
#        pos = 'SB'    
#    if t == 2: 
#        pos = 'BB'
#    if t == 3: 
#        pos = 'UTG'
#    if t == 4: 
#        pos = 'UTG+1'
#    if t == 5:
#        pos = 'MP'
#    if t == 6:
#        pos = 'CO'
   
   
   
### potsize before hands were dealt ###

#ante
#def find_nth(haystack, needle, n):
#    start = haystack.find(needle)
#    while start >= 0 and n > 1:
#        start = haystack.find(needle, start+len(needle))
#        n -= 1
#    return start

if 'ante' in HAND1:
    try:
        p1 = HAND1.find('ante')
        ante = HAND1[p1:p1+15]
        ante = ante.partition('ante ')[2]
        ante = int(ante.partition('\nn')[0])
        anteTot = ante*pl
        
    except:
        pass
#pot size before dealing any cards
potSize0 = int(anteTot + hh.sb + hh.bb)


#what amount comes into the pot after cards were dealt until its our turn


v = hh.preflop_actions
potSize1 = potSize0
NotOut = pl-1     #how many player does fold before us
for i in range(len(v)):
    #i = 1
    if v[i].partition(':')[0] != hh.hero.name:
        add = v[i].partition(':')[2]
        if 'calls' in add and 'all-in' not in add:
            add1 = int(add.partition('calls ')[2])
            
        if 'calls' in add and 'all-in' in add:  
            add1 = int(add.partition('to ')[2].partition(' and')[0])

        if 'raises' in add and 'all-in' not in add:
            add1 = int(add.partition('to ')[2])
                       
        if 'raises' in add and 'all-in' in add:  
            add1 = int(add.partition('to ')[2].partition(' and')[0])
            high.append(add1)
            
        if 'checks' in add:
            add1 = 0
            
        if 'folds' in add:
            add1 = 0
            NotOut -= 1
        
        potSize1 += add1

    else:
        break


# i is our position regarding to the player on seat 1 
                
#####################      what are our potOdds preflop, first decision       ####################
                
#if there was no raise before us and our position is outside of the blinds
if all('raises' not in v[j] for j in range(len(v[:i]))) and t != 2 and t != 1:
    potOdds0 = float(hh.bb/potSize1)

if all('raises' not in v[j] for j in range(len(v[:i]))) and t == 1:
    potOdds0 = float(hh.sb/potSize1)
    
if all('raises' not in v[j] for j in range(len(v[:i]))) and t == 2:    
    potOdds0 = float(0.000000001/potSize1)
    
    
#if there was a raise before us and we arent in the blinds    
if any('raises' in v[j] for j in range(len(v[:i]))) and t != 2 and t != 1:
    for q in range(len(v[:i])):
    #q = 0
        if v[q].partition(':')[0] != hh.hero.name:
            addr = v[q].partition(':')[2]
            if 'raises' in addr and all('raises' not in v[q2].partition(':')[2] for q2 in range(q+1,len(v[:i]))) and 'all-in' not in addr:
                addr1 = int(addr.partition('to ')[2])
                
            if 'raises' in addr and all('raises' not in v[q2].partition(':')[2] for q2 in range(q+1,len(v[:i]))) and 'all-in' in addr:
                addr1 = max(high)
                
                if addr1-addWe < p.stack:
                    potOdds1 = float((addr1-addWe)/potSize1)

    potOdds0 = float(addr1/potSize1)
    

    



###### deuces, a hand evaluator from github #####

from deuces import Card
from deuces import Evaluator
evaluator = Evaluator()
from deuces import Deck



#what are our raw cards?
raw = HAND1.strip()
split_re = re.compile(r" ?\*\*\* ?\n?|\n")
splitted = split_re.split(raw)
sections = [ind for ind, elem in enumerate(splitted) if not elem]
hole_cards_line = splitted[sections[0] + 2]

hero_re = re.compile(r"^Dealt to (?P<hero_name>.+?) \[(..) (..)\]")
match = hero_re.match(hole_cards_line)

#def get_hero_from_players(hero_name):
#        #hero_name = 'ollikahn23'
#        player_names = [p.name for p in hh.players]
#        #player_names = [p.name for p in players]        
#        hero_index = player_names.index(hero_name)
#        #hero_index = player_names.index(hero_name)        
#        return hh.players[hero_index], hero_index
#
#hero, hero_index = get_hero_from_players(match.group('hero_name')) 

first_raw_card = match.group(2)
second_raw_card = match.group(3)
raw_hand = first_raw_card + second_raw_card

   
hand = [
   Card.new(first_raw_card),
   Card.new(second_raw_card)
]    
    

#calculating our equity preflop, regarding the count of players


p11 = 0                 #how often do we win
p22 = 0                 #how often opponents win
opp = NotOut            #how many opponents are still in the game in that moment, we have to make a decision
playerHero_hand = hand  #our hand


start_time = time.time()
for i in range(20000):   
    #constructin the whole deck
    deck = Deck()
    
    
    #Card.print_pretty_cards(player1_hand)
    
    
    #removing our own hand from the deck
    deck.cards.remove(hand[0])
    deck.cards.remove(hand[1])
    
    
    d = {}
    for j in range(opp):
        #giving a random player random cards
        d['player%s_hand'%j] = deck.draw(2)
        
    #Card.print_pretty_cards(d['player2_hand'])
   
    #Card.print_pretty_cards(d['player3_hand'])
    
    
    board = deck.draw(5)
    #Card.print_pretty_cards(board)
    
    
    #how strong are the hands from our opponents
    e = {}
    for k in range(opp):
        e['p%s_score'%k] = evaluator.evaluate(board, d['player%s_hand'%k])
#        p1_score = evaluator.evaluate(board, player1_hand)
#        p2_score = evaluator.evaluate(board, player2_hand)
#        p3_score = evaluator.evaluate(board, player3_hand)
    
    
    #how strong is our hand
    e['pHero_score'] = evaluator.evaluate(board, playerHero_hand)
    
    
    if min(e, key=e.get) == 'pHero_score':
        p11 += 1
        
    else:
        p22 += 1
   

rate = p11/20000


if rate < potOdds0:
    print('Decision Nr.%d: Fold the Hand preflop'%dec)
    dec += 1
    
else:
    print('Decision Nr.%d: Call/ Raise the Hand preflop'%dec)
    dec += 1    
    
print("--- %s seconds ---" % (time.time() - start_time))








#####what amount comes into the pot after it was our turn for the first time


v = hh.preflop_actions
potSize1 = potSize0
c = 0           #what is our position regarding to UTG
for i in range(len(v)):
    #i = 1
    if v[i].partition(':')[0] != hh.hero.name:
        
        add = v[i].partition(':')[2]
        if 'calls' in add:
            add1 = int(add.partition('calls ')[2])

        if 'raises' in add:
            add1 = int(add.partition('to ')[2])
            
        if 'checks' in add:
            add1 = 0
            
        if 'folds' in add:
            add1 = 0
            NotOut -= 1
        
        potSize1 += add1

    else:
        break
  
  
#what amount do we spend into the pot with our first affirmative decision 
potSize2 = potSize1
for i in range(len(v)):
    c += 1
    if v[i].partition(':')[0] == hh.hero.name:
        add = v[i].partition(':')[2]
        if 'calls' in add:
            addWe += int(add.partition('calls ')[2])

        if 'raises' in add:
            addWe += int(add.partition('to ')[2])
            
        if 'checks' in add:
            addWe += 0
            
        if 'folds' in add:
            addWe += 0
            NotOut -= 1
        
        potSize2 += addWe
        break
    
    

#what amount comes into the pot after from our opponents after our first decision until our second decision
potSize3 = potSize2
for i in range(c, len(v)):
    #i = 3
    if v[i].partition(':')[0] != hh.hero.name:
        add = v[i].partition(':')[2]
        if 'calls' in add and 'all-in' not in add:
            add1 = int(add.partition('calls ')[2])
            
        if 'calls' in add and 'all-in' in add:  
            add1 = int(add.partition('to ')[2].partition(' and')[0])

        if 'raises' in add and 'all-in' not in add:
            add1 = int(add.partition('to ')[2])
                       
        if 'raises' in add and 'all-in' in add:  
            add1 = int(add.partition('to ')[2].partition(' and')[0])
            high.append(add1)
            
        if 'checks' in add:
            add1 = 0
            
        if 'folds' in add:
            add1 = 0
            NotOut -= 1
        
        potSize3 += add1

    else:
        break



# i is our position regarding to the player on seat 1 (change the name of the variable!!!)
                
                
#####################      what are our potOdds preflop, second decision       ####################


                
#if there was no raise before us and our position is outside of the blinds
if all('raises' not in v[j] for j in range(len(v[:i]))) and t != 2 and t != 1:
    potOdds0 = float(hh.bb/potSize1)

if all('raises' not in v[j] for j in range(len(v[:i]))) and t == 1:
    potOdds0 = float(hh.sb/potSize1)
    
if all('raises' not in v[j] for j in range(len(v[:i]))) and t == 2:    
    potOdds0 = float(0.000000001/potSize1)
    
    
#if there was a raise before us and we arent in the blinds    
if any('raises' in v[j] for j in range(len(v[:i]))) and t != 2 and t != 1:
    for q in range(len(v[:i])):
    #q = 3
        if v[q].partition(':')[0] != hh.hero.name:
            addr = v[q].partition(':')[2]
            #is there raise and is it the last one before our decision, q2 = 1
            if 'raises' in addr and all('raises' not in v[q2].partition(':')[2] for q2 in range(q+1,len(v[:i]))) and 'all-in' not in addr:
                addr1 = int(addr.partition('to ')[2])
                
            if 'raises' in addr and all('raises' not in v[q2].partition(':')[2] for q2 in range(q+1,len(v[:i]))) and 'all-in' in addr:
                addr1 = max(high)
                
                if addr1-addWe < p.stack:
                    potOdds1 = float((addr1-addWe)/potSize3)




    



p11 = 0                 #how often do we win
p22 = 0                 #how often opponents win
opp = NotOut            #how many opponents are still in the game in that moment, we have to make a decision
playerHero_hand = hand  #our hand


start_time = time.time()
for i in range(20000):   
    #constructin the whole deck
    deck = Deck()
    
    
    #Card.print_pretty_cards(player1_hand)
    
    
    #removing our own hand from the deck
    deck.cards.remove(hand[0])
    deck.cards.remove(hand[1])
    
    
    d = {}
    for j in range(opp):
        #giving a random player random cards
        d['player%s_hand'%j] = deck.draw(2)
        
    #Card.print_pretty_cards(d['player2_hand'])
   
    #Card.print_pretty_cards(d['player3_hand'])
    
    
    board = deck.draw(5)
    #Card.print_pretty_cards(board)
    
    
    #how strong are the hands from our opponents
    e = {}
    for k in range(opp):
        e['p%s_score'%k] = evaluator.evaluate(board, d['player%s_hand'%k])
#        p1_score = evaluator.evaluate(board, player1_hand)
#        p2_score = evaluator.evaluate(board, player2_hand)
#        p3_score = evaluator.evaluate(board, player3_hand)
    
    
    #how strong is our hand
    e['pHero_score'] = evaluator.evaluate(board, playerHero_hand)
    
    
    if min(e, key=e.get) == 'pHero_score':
        p11 += 1
        
    else:
        p22 += 1
   

rate = p11/20000


if rate < potOdds0:
    print('Decision Nr.%d: Fold the Hand preflop'%dec)
    dec += 1
    
else:
    print('Decision Nr.%d: Call/ Raise the Hand preflop'%dec)
    dec += 1    
    
print("--- %s seconds ---" % (time.time() - start_time))
























#what is our stack
p.stack





#what player were around us?
q = hh.players



#show me the flop
r = hh.flop
r.actions
r.pot
r.players
r.is_rainbow
r.is_monotone


r.has_flushdraw
r.has_straightdraw
#both yes, pretty wet flop

 



#show me the turn
s = hh.turn


#show me the river
t = hh.river



####  show the complete board
u = hh.board

#flop
u[0:3]



#what happened preflop?
v = hh.preflop_actions


#what happenedon the turn/ river

w = hh.flop_actions  ###does work, see variable r
w1 = hh.turn_actions
w2 = hh.river_actions



#how big are the pots on each street
x = hh.flop_pot ###doesnt work
x1 = hh.turn_pot ###doesnt work
x2 = hh.river_pot ###doesnt work


#how many players were there on each street
y = hh.flop_num_players 
###does work with:
y = len(r.players)    
 

    
y1 = hh.turn_num_players  ###doesnt work
y2 = hh.river_num_players  ###doesnt work


#total pot at the end
z = hh.total_pot
z1 = hh.winners
z2 = hh.show_down








from poker.room.pokerstars import PokerStarsHandHistory
# First step, only raw hand history is saved, no parsing will happen yet
hh = PokerStarsHandHistory(HAND1)
hh.parse()

hh.max_players
hh.players
hh.button
hh.hero.combo



###################   space for the essential - THE HANDS #################



HAND1 = """
PokerStars Hand #167865096867: Tournament #1859440577, $3.40+$0.10 USD Hold'em No Limit - Level II (15/30) - 2013/10/04 19:53:27 CET [2013/10/04 13:53:27 ET]
Table '1859440577 1' 2-max Seat #1 is the button
Seat 1: ollikahn23 (225 in chips)
Seat 2: 44tom44 (775 in chips)
ollikahn23: posts small blind 15
44tom44: posts big blind 30
*** HOLE CARDS ***
Dealt to ollikahn23 [2s Ac]
ollikahn23: raises 195 to 225 and is all-in
44tom44: calls 195
*** FLOP *** [8d 7s Jc]
*** TURN *** [8d 7s Jc] [Kc]
*** RIVER *** [8d 7s Jc Kc] [Qs]
*** SHOW DOWN ***
44tom44: shows [Th Qd] (a pair of Queens)
ollikahn23: shows [2s Ac] (high card Ace)
44tom44 collected 450 from pot
*** SUMMARY ***
Total pot 450 | Rake 0
Board [8d 7s Jc Kc Qs]
Seat 1: ollikahn23 (button) (small blind) showed [2s Ac] and lost with high card Ace
Seat 2: 44tom44 (big blind) showed [Th Qd] and won (450) with a pair of Queens
"""


HAND1 = """
PokerStars Hand #182153559719: Tournament #2211561885, $4.10+$0.40 USD Hold'em No Limit - Level VI (100/200) - 2013/10/04 19:53:27 CET [2013/10/04 13:53:27 ET]
Table '2211561885 2' 9-max Seat #3 is the button
Seat 1: Yolo19 (8680 in chips)
Seat 2: neuiwirt28 (16091 in chips)
Seat 3: waddenzicht (6695 in chips)
Seat 4: RUBL72 (4599 in chips)
Seat 5: Jahjge (5716 in chips)
Seat 6: AlekseyK7777 (6670 in chips)
Seat 7: RTS-Rob (6326 in chips)
Seat 8: ollikahn23 (8786 in chips)
Seat 9: ionelinho28 (2643 in chips)
Yolo19: posts the ante 20
neuiwirt28: posts the ante 20
waddenzicht: posts the ante 20
RUBL72: posts the ante 20
Jahjge: posts the ante 20
AlekseyK7777: posts the ante 20
RTS-Rob: posts the ante 20
ollikahn23: posts the ante 20
ionelinho28: posts the ante 20
RUBL72: posts small blind 100
Jahjge: posts big blind 200
*** HOLE CARDS ***
Dealt to ollikahn23 [6h 6s]
AlekseyK7777: raises 200 to 400
RTS-Rob: calls 400
ollikahn23: calls 400
ionelinho28: raises 2223 to 2623 and is all-in
Yolo19: folds
neuiwirt28: folds
waddenzicht: folds
RUBL72: folds
Jahjge: folds
AlekseyK7777: folds
RTS-Rob: folds
ollikahn23: calls 2223
*** FLOP *** [4h Jh 8h]
*** TURN *** [4h Jh 8h] [9c]
*** RIVER *** [4h Jh 8h 9c] [6d]
*** SHOW DOWN ***
ollikahn23: shows [6h 6s] (three of a kind, Sixes)
ionelinho28: shows [Jc Kc] (a pair of Jacks)
ollikahn23 collected 6526 from pot
ionelinho28 finished the tournament in 27th place
*** SUMMARY ***
Total pot 6526 | Rake 0
Board [4h Jh 8h 9c 6d]
Seat 1: Yolo19 folded before Flop (didn't bet)
Seat 2: neuiwirt28 folded before Flop (didn't bet)
Seat 3: waddenzicht (button) folded before Flop (didn't bet)
Seat 4: RUBL72 (small blind) folded before Flop
Seat 5: Jahjge (big blind) folded before Flop
Seat 6: AlekseyK7777 folded before Flop
Seat 7: RTS-Rob folded before Flop
Seat 8: ollikahn23 showed [6h 6s] and won (6526) with three of a kind, Sixes
Seat 9: ionelinho28 showed [Jc Kc] and lost with a pair of Jacks
"""









HAND1 = """
PokerStars Hand #183001414583: Hold'em No Limit ($0.05/$0.10 USD) - 2018/02/24 19:47:59 ET
Table 'Sarin' 9-max Seat #8 is the button
Seat 1: ollikahn23 ($10 in chips) 
Seat 2: your_drama1 ($18.73 in chips) 
Seat 3: Sasha Ghan ($13.88 in chips) 
Seat 4: Velliton87 ($10.16 in chips) 
Seat 5: kasatka07 ($17.53 in chips) 
Seat 6: Denisella ($10.24 in chips) 
Seat 7: Mr_Dick666 ($11.06 in chips) 
Seat 8: JasonAG ($10.32 in chips) 
Seat 9: ZuJIOk ($18.53 in chips) 
ZuJIOk: posts small blind $0.05
ollikahn23: posts big blind $0.10
*** HOLE CARDS ***
Dealt to ollikahn23 [6h Th]
your_drama1: folds 
Sasha Ghan: folds 
Velliton87: folds 
kasatka07: folds 
Denisella: folds 
Mr_Dick666: folds 
JasonAG: raises $0.10 to $0.20
ZuJIOk: folds 
ollikahn23: folds 
Uncalled bet ($0.10) returned to JasonAG
JasonAG collected $0.25 from pot
JasonAG: doesn't show hand 
*** SUMMARY ***
Total pot $0.25 | Rake $0 
Seat 1: ollikahn23 (big blind) folded before Flop
Seat 2: your_drama1 folded before Flop (didn't bet)
Seat 3: Sasha Ghan folded before Flop (didn't bet)
Seat 4: Velliton87 folded before Flop (didn't bet)
Seat 5: kasatka07 folded before Flop (didn't bet)
Seat 6: Denisella folded before Flop (didn't bet)
Seat 7: Mr_Dick666 folded before Flop (didn't bet)
Seat 8: JasonAG (button) collected ($0.25)
Seat 9: ZuJIOk (small blind) folded before Flop"""



HAND1 = """
PokerStars Hand #182153766627: Tournament #2211561885, $4.10+$0.40 USD Hold'em No Limit - Level VII (125/250) - 2018/02/07 14:49:30 CET [2018/02/07 8:49:30 ET]
Table '2211561885 2' 9-max Seat #2 is the button
Seat 1: Yolo19 (7035 in chips)
Seat 2: neuiwirt28 (21457 in chips)
Seat 4: RUBL72 (4104 in chips)
Seat 5: Jahjge (7873 in chips)
Seat 6: AlekseyK7777 (6497 in chips)
Seat 7: RTS-Rob (5481 in chips)
Seat 8: ollikahn23 (13759 in chips)
Yolo19: posts the ante 25
neuiwirt28: posts the ante 25
RUBL72: posts the ante 25
Jahjge: posts the ante 25
AlekseyK7777: posts the ante 25
RTS-Rob: posts the ante 25
ollikahn23: posts the ante 25
RUBL72: posts small blind 125
Jahjge: posts big blind 250
*** HOLE CARDS ***
Dealt to ollikahn23 [7h 7s]
AlekseyK7777: calls 250
RTS-Rob: calls 250
ollikahn23: calls 250
Yolo19: folds
neuiwirt28: folds
RUBL72: calls 125
Jahjge: checks
*** FLOP *** [Kh 8c 7c]
RUBL72: checks
Jahjge: checks
AlekseyK7777: checks
RTS-Rob: checks
ollikahn23: bets 1025
RUBL72: folds
Jahjge: folds
AlekseyK7777: folds
RTS-Rob: calls 1025
*** TURN *** [Kh 8c 7c] [3h]
RTS-Rob: checks
ollikahn23: bets 3000
RTS-Rob: calls 3000
*** RIVER *** [Kh 8c 7c 3h] [8h]
RTS-Rob: bets 1181 and is all-in
ollikahn23: calls 1181
*** SHOW DOWN ***
RTS-Rob: shows [Tc 9c] (a pair of Eights)
ollikahn23: shows [7h 7s] (a full house, Sevens full of Eights)
ollikahn23 collected 11837 from pot
RTS-Rob finished the tournament in 23rd place
*** SUMMARY ***
Total pot 11837 | Rake 0
Board [Kh 8c 7c 3h 8h]
Seat 1: Yolo19 folded before Flop (didn't bet)
Seat 2: neuiwirt28 (button) folded before Flop (didn't bet)
Seat 4: RUBL72 (small blind) folded on the Flop
Seat 5: Jahjge (big blind) folded on the Flop
Seat 6: AlekseyK7777 folded on the Flop
Seat 7: RTS-Rob showed [Tc 9c] and lost with a pair of Eights
Seat 8: ollikahn23 showed [7h 7s] and won (11837) with a full house, Sevens full of Eights"""




HAND1 = """
PokerStars Hand #138364355489: Tournament #1280727192, $3.19+$0.31 USD Hold'em No Limit - Level VIII (150/300) - 2015/07/22 2:17:55 BRT [2015/07/22 1:17:55 ET]
Table '1280727192 2' 9-max Seat #5 is the button
Seat 3: py3k (2388 in chips)
Seat 4: Sky_Shanks (3751 in chips)
Seat 5: rockrock568 (2041 in chips)
Seat 6: SiickTico (8831 in chips)
Seat 7: SanSuhan (1890 in chips)
Seat 8: allbluff78 (4615 in chips)
Seat 9: shakuni8492 (5713 in chips)
py3k: posts the ante 25
Sky_Shanks: posts the ante 25
rockrock568: posts the ante 25
SiickTico: posts the ante 25
SanSuhan: posts the ante 25
allbluff78: posts the ante 25
shakuni8492: posts the ante 25
SiickTico: posts small blind 150
SanSuhan: posts big blind 300
*** HOLE CARDS ***
Dealt to py3k [Js 3s]
allbluff78: folds
shakuni8492: folds
py3k: raises 2063 to 2363 and is all-in
Sky_Shanks: raises 1363 to 3726 and is all-in
rockrock568: folds
SiickTico: folds
SanSuhan: folds
Uncalled bet (1363) returned to Sky_Shanks
*** FLOP *** [Ts Td As]
*** TURN *** [Ts Td As] [Jd]
*** RIVER *** [Ts Td As Jd] [2c]
*** SHOW DOWN ***
py3k: shows [Js 3s] (two pair, Jacks and Tens)
Sky_Shanks: shows [Kc Qc] (a straight, Ten to Ace)
Sky_Shanks collected 5351 from pot
py3k finished the tournament in 14th place
*** SUMMARY ***
Total pot 5351 | Rake 0
Board [Ts Td As Jd 2c]
Seat 3: py3k showed [Js 3s] and lost with two pair, Jacks and Tens
Seat 4: Sky_Shanks showed [Kc Qc] and won (5351) with a straight, Ten to Ace
Seat 5: rockrock568 (button) folded before Flop (didn't bet)
Seat 6: SiickTico (small blind) folded before Flop
Seat 7: SanSuhan (big blind) folded before Flop
Seat 8: allbluff78 folded before Flop (didn't bet)
Seat 9: shakuni8492 folded before Flop (didn't bet)
"""

