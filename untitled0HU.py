from __future__ import unicode_literals
from __future__ import division
from poker import Suit
import time
import re
import random
from poker import Range



HAND1 = """
PokerStars Hand #187932118690: Tournament #2339076938, $28.20+$1.80 USD Hold'em No Limit - Match Round I, Level I (10/20) - 2018/05/30 22:16:20 CET [2018/05/30 16:16:20 ET]
Table '2339076938 1' 3-max Seat #1 is the button
Seat 1: boomerang747 (480 in chips)
Seat 3: heutegewinnwa (1020 in chips)
boomerang747: posts small blind 10
heutegewinnwa: posts big blind 20
*** HOLE CARDS ***
Dealt to heutegewinnwa [8h 8c]
boomerang747: raises 460 to 480 and is all-in
heutegewinnwa: calls 460
*** FLOP *** [Ah 6d 5h]
*** TURN *** [Ah 6d 5h] [Jd]
*** RIVER *** [Ah 6d 5h Jd] [9h]
*** SHOW DOWN ***
heutegewinnwa: shows [8h 8c] (a pair of Eights)
boomerang747: shows [Qc Kd] (high card Ace)
heutegewinnwa collected 960 from pot
boomerang747 finished the tournament in 2nd place
heutegewinnwa wins the tournament and receives $60.00 - congratulations!
*** SUMMARY ***
Total pot 960 | Rake 0
Board [Ah 6d 5h Jd 9h]
Seat 1: boomerang747 (button) (small blind) showed [Qc Kd] and lost with high card Ace
Seat 3: heutegewinnwa (big blind) showed [8h 8c] and won (960) with a pair of Eights"""





from poker.room.pokerstars import PokerStarsHandHistory
# First step, only raw hand history is saved, no parsing will happen yet
hh = PokerStarsHandHistory(HAND1)
hh.parse()




########   STARTING ANALYSE HEADS-UP BY THE BOOK OF TIPTON  ##########
#Open Exercises:

#make a function out of some if and for-loops
#3bb-range preflop automated from PokerTracker?
#what if we are small blind? is there any boolean for hero to indicate if we are bb or sb?
#-> search a hand where u are in the small blind


#####  Stats of Villain  ######

#preflop:

threeB_PF = 0.5     #automated from PokerTracker?



##############################


if threeB_PF == 0.5:
    Range3bPF = Range("33+ A2o+ A2s+ K5o+ K2s+ Q7o+ Q2s+ J7o+ J4s+ T8o+ T6s+ 98o+ 96s+ 98o+ 96s+ 86s 76s").hands








fullRg = []
suits = ['c', 's', 'h', 'd']

for k in Range3bPF:
    if 'o' in str(k):
#        for l in range(12):
         for l in suits:    
             for l1 in suits:
                 fullRg.append(str(k)[0]+l+str(k)[1]+l1)
            
    if 's' in str(k):
        for m in suits:
            fullRg.append(str(k)[0]+m+str(k)[1]+m)
 
        
    if 'o' not in str(k) and 's' not in str(k):
        for n in range(4):
            for o in range(4):
                if o > n:
                    try: 
                        fullRg.append(str(k)[0]+suits[n]+str(k)[1]+suits[o])
                    
                    except:
                        pass

fullRg = list(set(fullRg))



#### Exercises ####

# 2) EV is the stack at the end of the round (so try out raises preflop and check through the whole hand)
# 3) check out pokerstove for more equity-exercises
# 4) maximum exploitive strategy
# 5) control the inequality below





dec = 1             #Number of our decision
addWe = 0           #what we have add to the pot so far
high = []           #empty list to get the highest amount being bet so far





#hh.max_players
#hh.players
#hh.button
#hh.hero.combo




###who and where we are?
p = hh.hero



###what we have?
#p.combo




###what is our position
#p.seat

#what is our positon regarding to the button (utg, utg+1, etc.), make a function out of it

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


#how many players are on the table at the moment including us
pl = 0
for i in range(hh.max_players):
    if 'Empty Seat' not in a[i].name:
        pl += 1


if 'ante' in HAND1:
    try:
        p1 = HAND1.find('ante')
        ante = HAND1[p1:p1+15]
        ante = ante.partition('ante ')[2]
        ante = int(ante.partition('\nn')[0])
        anteTot = ante*pl
        potSize0 = int(anteTot + hh.sb + hh.bb)
    except:
        pass
    
else:
    potSize0 = int(hh.sb + hh.bb)
    
 

#what amount comes into the pot after cards were dealt until its our turn
v = hh.preflop_actions
potSize1 = potSize0
NotOut = pl-1     #how many player does fold before us
for i in range(len(v)):
    #i = 0
    if v[i].partition(':')[0] != hh.hero.name:
        if v[i].partition(':')[0] != hh.button.name:
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
            add2 = v[i].partition(':')[2]
            if 'calls' in add2 and 'all-in' not in add2:
                add3 = int(add2.partition('calls ')[2])
                
            if 'calls' in add2 and 'all-in' in add2:  
                add3 = int(add2.partition('to ')[2].partition(' and')[0])
    
            if 'raises' in add2 and 'all-in' not in add2:
                add3 = int(add2.partition('to ')[2])
                           
            if 'raises' in add2 and 'all-in' in add2:  
                add3 = int(add2.partition('to ')[2].partition(' and')[0])
                high.append(add3)
                
            if 'checks' in add2:
                add3 = 0
                
            if 'folds' in add2:
                add3 = 0
                NotOut -= 1
            
            potSize1 += add3 - hh.sb
            

    else:
        break




# i is our position regarding to the player on seat 1, see the for loop for the amount size before 
                
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
    
    
    
    
#if there was a raise before us and we are in the blinds     
if any('raises' in v[j] for j in range(len(v[:i]))) and t != 2 and t == 1:
    for q in range(len(v[:i])):
    #q = 0
        if v[q].partition(':')[0] != hh.hero.name:
            addr = v[q].partition(':')[2]
            if 'raises' in addr and all('raises' not in v[q2].partition(':')[2] for q2 in range(q+1,len(v[:i]))) and 'all-in' not in addr:
                addr1 = int(addr.partition('to ')[2])
                
                if v[q].partition(':')[0] == hh.button.name:
                    addr1 = int(addr1 - hh.bb)
                    
                
                
                #was the raise an all-in?
            if 'raises' in addr and all('raises' not in v[q2].partition(':')[2] for q2 in range(q+1,len(v[:i]))) and 'all-in' in addr:
                addr1 = max(high)
                
                if addr1-addWe < p.stack:
                    potOdds1 = float((addr1-addWe)/potSize1)

    potOdds0 = float(addr1/(potSize1+addr1))    







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
#first_raw_card = '2s'
second_raw_card = match.group(3)
#second_raw_card = '7c'
raw_hand = first_raw_card + second_raw_card



fullRg = [x for x in fullRg if first_raw_card not in x and second_raw_card not in x]


   
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
for i in range(50000):   
    #constructin the whole deck
    deck = Deck()
    
    
    #Card.print_pretty_cards(player1_hand)
    
    
    #removing our own hand from the deck
    deck.cards.remove(hand[0])
    deck.cards.remove(hand[1])
    
    
    
    
    d = {}
    
    #giving villain random cards or cards from a range
    for j in range(opp):   
        #random:
        #d['player%s_hand'%j] = deck.draw(2)
        #print(d)
    
    
        #giving villain cards from his range regarding his 3bPF-Range:
        t1 = random.randint(0,len(fullRg)-1)
        #print(fullRg[t1])
        d['player%s_hand'%j] = [Card.new(fullRg[t1][:2]), Card.new(fullRg[t1][2:])]
        #print(d)
        #removing our own hand from the deck
        deck.cards.remove(d['player%s_hand'%j][0])
        deck.cards.remove(d['player%s_hand'%j][1])
    
            
        
    #Card.print_pretty_cards(d['player0_hand'])
   
    #Card.print_pretty_cards(d['player3_hand'])
    
    
    board = deck.draw(5)
    #Card.print_pretty_cards(board)
    
    
    
    
    
    #how strong are the hands from our opponents
    e = {}
    for k in range(opp):
        e['p%s_score'%k] = evaluator.evaluate(board, d['player%s_hand'%k])
        #print(e)
#        p1_score = evaluator.evaluate(board, player1_hand)
#        p2_score = evaluator.evaluate(board, player2_hand)
#        p3_score = evaluator.evaluate(board, player3_hand)
    
    
    #how strong is our hand
    e['pHero_score'] = evaluator.evaluate(board, playerHero_hand)
    
    
    if min(e, key=e.get) == 'pHero_score':
        p11 += 1
        
    else:
        p22 += 1
   

rate = p11/50000




#if our EV at the end of the hand is smaller/bigger than our EV if we fold, then fold/call or raise:
#if we are in the big blind
if t == 1:
    if ((p.stack-float(hh.bb)) - addr1)*(1-rate) + ((p.stack-float(hh.bb)) + int(potSize1))*rate < (p.stack-float(hh.bb)):    
        print('Decision Nr.%d: Fold the Hand preflop'%dec)
        dec += 1
        print(rate)
        
    else:
        print('Decision Nr.%d: Call/ Raise the Hand preflop'%dec)
        dec += 1 
        print(rate)
        
else:
    pass
        
    print("--- %s seconds ---" % (time.time() - start_time))

#errors in 300817, 3003, 9417, 168113, 700321, 67735, 13195(Js5s)




















