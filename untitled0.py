# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 23:24:38 2018

@author: Robin
"""


from __future__ import unicode_literals
from __future__ import division
from poker import Suit
import re

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
q = 0
for i in range(hh.max_players):
    if 'Empty Seat' not in a[i].name:
        q += 1



#add further q/ positions
if q == 7:
    if t == 1:
        pos = 'SB'    
    if t == 2: 
        pos = 'BB'
    if t == 3: 
        pos = 'UTG'
    if t == 4: 
        pos = 'UTG+1'
    if t == 5:
        pos = 'MP'
    if t == 6:
        pos = 'CO'
   
   
   
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
        anteTot = ante*q
        
    except:
        pass
#pot size before dealing any cards
potSize0 = int(anteTot + hh.sb + hh.bb)


#what amount comes into the pot after cards were dealt until its our turn


v = hh.preflop_actions
potSize1 = potSize0
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
        
        potSize1 += add1

    else:
        break


# í is our position regarding to the raiser
                
#####################      what are our potOdds preflop       ####################
                
#if there was no raise before us and our position is outside of the blinds
if all('raises' not in v[j] for j in range(len(v[:i]))) and t != 2 and t != 1:
    potOdds0 = float(hh.bb/potSize1)

if all('raises' not in v[j] for j in range(len(v[:i]))) and t == 1:
    potOdds0 = float(hh.sb/potSize1)
    
if all('raises' not in v[j] for j in range(len(v[:i]))) and t == 2:    
    potOdds0 = float(0.000000001/potSize1)
    
    
#if there was a raise before and we arent in the blinds    
if any('raises' in v[j] for j in range(len(v[:i]))) and t != 2 and t != 1:
    for q in range(len(v[:i])):
    #q = 0
        if v[q].partition(':')[0] != hh.hero.name:
            addr = v[q].partition(':')[2]
            if 'raises' in addr:
                addr1 = int(addr.partition('to ')[2])
            if 'reraises' in addr:
                addr1 = int(addr.partition('to ')[2])

    potOdds0 = float(addr1/potSize1)
    
    
    


    
    
    
    
    
    
    
    
    



###### deuces, a hand evaluator from github #####

from deuces import Card
from deuces import Evaluator
evaluator = Evaluator()




card = Card.new('Qh')


board = [Card.new('Ah'), Card.new('Kh'), Card.new('Jh'), Card.new('2s'), Card.new('3h')]

hand = [Card.new('Qs'), Card.new('Ts')]





###which strength the hand has
print evaluator.evaluate(board, hand)


from deuces import Deck
deck = Deck()
board = deck.draw(5)
player1_hand = deck.draw(2)
player2_hand = deck.draw(2)

p1_score = evaluator.evaluate(board, player1_hand)

p2_score = evaluator.evaluate(board, player2_hand)


p1_class = evaluator.get_rank_class(p1_score)

p2_class = evaluator.get_rank_class(p2_score)


evaluator.class_to_string(p1_class)

evaluator.class_to_string(p2_class)


hands = [player1_hand, player2_hand]
evaluator.hand_summary(board, hands)






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
    
    


print evaluator.evaluate(hand)


#calculating our equity preflop, regarding the count of players

import random
from deuces import Deck

deck = Deck()

player1_hand = hand
a = deck.cards.remove(hand[0], hand[1])

player2_hand = deck.draw(2)
board = deck.draw(5)




















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
PokerStars Hand #183001414583:  Hold'em No Limit ($0.05/$0.10 USD) - 2018/02/24 19:47:59 ET
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
PokerStars Hand #105024000105: Tournament #797469411, $3.19+$0.31 USD Hold'em No Limit - Level I (10/20) - 2013/10/04 19:53:27 CET [2013/10/04 13:53:27 ET]
Table '797469411 15' 9-max Seat #1 is the button
Seat 1: flettl2 (1500 in chips)
Seat 2: santy312 (3000 in chips)
Seat 3: flavio766 (3000 in chips)
Seat 4: strongi82 (3000 in chips)
Seat 5: W2lkm2n (3000 in chips)
Seat 6: MISTRPerfect (3000 in chips)
Seat 7: blak_douglas (3000 in chips)
Seat 8: sinus91 (1500 in chips)
Seat 9: STBIJUJA (1500 in chips)
santy312: posts small blind 10
flavio766: posts big blind 20
*** HOLE CARDS ***
Dealt to W2lkm2n [Ac Jh]
strongi82: folds
W2lkm2n: raises 40 to 60
MISTRPerfect: calls 60
blak_douglas: folds
sinus91: folds
STBIJUJA: folds
flettl2: folds
santy312: folds
flavio766: folds
*** FLOP *** [2s 6d 6h]
W2lkm2n: bets 80
MISTRPerfect: folds
Uncalled bet (80) returned to W2lkm2n
W2lkm2n collected 150 from pot
W2lkm2n: doesn't show hand
*** SUMMARY ***
Total pot 150 | Rake 0
Board [2s 6d 6h]
Seat 1: flettl2 (button) folded before Flop (didn't bet)
Seat 2: santy312 (small blind) folded before Flop
Seat 3: flavio766 (big blind) folded before Flop
Seat 4: strongi82 folded before Flop (didn't bet)
Seat 5: W2lkm2n collected (150)
Seat 6: MISTRPerfect folded on the Flop
Seat 7: blak_douglas folded before Flop (didn't bet)
Seat 8: sinus91 folded before Flop (didn't bet)
Seat 9: STBIJUJA folded before Flop (didn't bet)"""


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
Seat 9: ionelinho28 showed [Jc Kc] and lost with a pair of Jacks"""

HAND1 = """
PokerStars Hand #183649371977: Tournament #2244789271, $4.10+$0.40 USD Hold'em No Limit - Level IX (200/400) - 2018/03/10 11:29:54 ET
Table '2244789271 8' 9-max Seat #5 is the button
Seat 2: L'éternité (18498 in chips) 
Seat 3: ollikahn23 (7440 in chips) 
Seat 4: Jacobob_Jr (4513 in chips) 
Seat 5: kidkid84 (7853 in chips) 
Seat 6: MoAKs70 (4738 in chips) 
Seat 8: Matt242 (18838 in chips) 
Seat 9: Alt4y (12010 in chips) 
L'éternité: posts the ante 50
ollikahn23: posts the ante 50
Jacobob_Jr: posts the ante 50
kidkid84: posts the ante 50
MoAKs70: posts the ante 50
Matt242: posts the ante 50
Alt4y: posts the ante 50
MoAKs70: posts small blind 200
Matt242: posts big blind 400
*** HOLE CARDS ***
Dealt to ollikahn23 [Qs Qc]
Alt4y: folds 
L'éternité: raises 500 to 900
ollikahn23: calls 900
Jacobob_Jr: folds 
kidkid84: folds 
MoAKs70: folds 
Matt242: folds 
*** FLOP *** [Ad Js Ks]
L'éternité: bets 908
ollikahn23: calls 908
*** TURN *** [Ad Js Ks] [5s]
L'éternité: bets 1507
ollikahn23: raises 2093 to 3600
L'éternité: calls 2093
*** RIVER *** [Ad Js Ks 5s] [3c]
L'éternité: bets 2000
ollikahn23: calls 1982 and is all-in
Uncalled bet (18) returned to L'éternité
*** SHOW DOWN ***
L'éternité: shows [As 9s] (a flush, Ace high)
ollikahn23: shows [Qs Qc] (a pair of Queens)
L'éternité collected 15730 from pot
ollikahn23 finished the tournament in 14th place and received $5.93.
*** SUMMARY ***
Total pot 15730 | Rake 0 
Board [Ad Js Ks 5s 3c]
Seat 2: L'éternité showed [As 9s] and won (15730) with a flush, Ace high
Seat 3: ollikahn23 showed [Qs Qc] and lost with a pair of Queens
Seat 4: Jacobob_Jr folded before Flop (didn't bet)
Seat 5: kidkid84 (button) folded before Flop (didn't bet)
Seat 6: MoAKs70 (small blind) folded before Flop
Seat 8: Matt242 (big blind) folded before Flop
Seat 9: Alt4y folded before Flop (didn't bet)"""

