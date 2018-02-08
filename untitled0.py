# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 23:24:38 2018

@author: Robin
"""


from __future__ import unicode_literals
from poker import Suit


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







