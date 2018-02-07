# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 23:24:38 2018

@author: Robin
"""

import poker
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

import random
random.shuffle(deck)
