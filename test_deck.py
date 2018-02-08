# # ToDo Write the tests for the following:
import random
import pyCardDeck
from typing import List
from trucodeck import *
import unittest

class TrucoDeckTests(unittest.TestCase):

    def test_mydeck(self):
        my_truco = pyCardDeck.Deck(generate_deck(),name="Truco Sujo", reshuffle=False)
        self.assertEqual(len(my_truco),40) # True
        carta0 = my_truco.draw_specific("Três de Ouros")
        carta1 = my_truco.draw_specific("Três de Espadas")
        carta2 = my_truco.draw_specific("Três de Copas")
        carta3 = my_truco.draw_specific("Três de Paus")

        carta4 = my_truco.draw_random()
        carta5 = my_truco.draw_bottom()

        self.assertEqual(carta0.name , "Três de Ouros" )# True
        self.assertEqual(carta0.suit , 1 )# True
        self.assertEqual(carta0.suit_name , "Ouros" )# True

        self.assertEqual(carta1.name , "Três de Espadas" )# True
        self.assertEqual(carta1.suit , 2) # True
        self.assertEqual(carta1.suit_name , "Espadas") # True

        self.assertEqual(carta2.name , "Três de Copas") # True
        self.assertEqual(carta2.suit , 3 )# True
        self.assertEqual(carta2.suit_name , "Copas") # True

        self.assertEqual(carta3.name , "Três de Paus") # True
        self.assertEqual(carta3.suit , 4) # True
        self.assertEqual(carta3.suit_name , "Paus") # True

        self.assertEqual(carta1.rank , carta2.rank)
        self.assertEqual(carta0.rank , carta3.rank) # True
        self.assertNotEqual(carta1, carta2) # False
        self.assertEqual(carta1 > carta2,0) # 0
        self.assertEqual(carta0.suit < carta1.suit, True) #True
        self.assertEqual(carta1.suit < carta2.suit, True) #True
        self.assertEqual(carta2.suit < carta3.suit, True) #True
        self.assertEqual(carta3.suit > carta0.suit, True) #True
        self.assertEqual(carta0 > carta4, True) # True

        cartas = [carta1, carta2 , carta3, carta4, carta5, carta0]
        print(cartas)
        random.shuffle(cartas)
        cartas.sort()
        self.assertEqual(len(my_truco),34) # True

        tres = [carta1,carta2,carta3,carta0]
        print(*tres, sep= ", ") # Três de Espadas, Três de Copas, Três de Paus, Três de Ouros
        tres.sort(key= lambda x: x.suit)
        print(*tres, sep= ", ") # Três de Ouros, Três de Espadas, Três de Copas, Três de Paus




# Study of how to pass an information from outer class to inner class.
#
# class Human:
#     def __init__(self):
#         self.name = 'Guido'
#         self.head = self.createHead()
#     def createHead(self):
#         return Human.Head(self)
#     class Head:
#         def __init__(self, human):
#             self.human = human
#         def talk(self):
#             return 'talking...', self.human.name
#
#
# guido = Human()
# guido.name
# guido.head.talk()
# guido.name = "Power Guido"
# guido.head.talk()
