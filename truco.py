#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an example of pyCardDeck, it's not meant to be complete poker script,
but rather a showcase of pyCardDeck's usage.
"""

import sys
import pyCardDeck
from typing import List
from pyCardDeck.cards import BaseCard


class TrucoCard(BaseCard):
    """
    Example Poker Card, since Poker is a a deck of Unique cards,
    we can say that if their name equals, they equal too.
    """
    def __init__(self, suit: str, rank: str, name: str):
        # Define self.name through BaseCard Class
        super().__init__("{} de {}".format(name, suit))
        self.suit = suit
        self.rank = rank
    def __eq__(self, other):
        return self.name == other
    def __gt__(self, other):
        suits = ['Ouros', 'Espadas', 'Copas', 'Paus']
        ranks = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        rank, suit = 0,0
        # Compare Ranks
        if ranks.index(self.rank) < ranks.index(other.rank):
            rank = -1
        elif ranks.index(self.rank) > ranks.index(other.rank):
            rank = 1
        else:
            rank = 0
        # Compare Suits
        if suits.index(self.suit) < suits.index(other.suit):
            suit = -1
        elif suits.index(self.suit) > suits.index(other.suit):
            suit = 1
        else:
            suit = 0
        return {'rank':rank, 'suit':suit}



    # def __cmp__(self,other):
    #     if self.value < other.value:
    #         return -1
    #     elif self.value > other.value:
    #         return 1
    #     else:
    #         return 0



def generate_deck(sujo=True) -> List[TrucoCard]:
    """
    Function that generates the deck, instead of writing down all cards, we use iteration
    to generate the cards for use
    :return:    List with all (24/40) cards for truco playing cards
    :rtype:     List[TrucoCard]
    """
    if sujo:
        suits = ['Ouros', 'Espadas', 'Copas', 'Paus']
        ranks = {'4': 'Quatro',
                 '5': 'Cinco',
                 '6': 'Seis',
                 '7': 'Sete',
                 'Q': 'Dama',
                 'J': 'Valete',
                 'K': 'Rei',
                 'A': 'Ás',
                 '2': 'Dois',
                 '3': 'Três'}
    if not sujo:
        suits = ['Ouros', 'Espadas', 'Copas', 'Paus']
        ranks = {'Q': 'Dama',
                 'J': 'Valete',
                 'K': 'Rei',
                 'A': 'Ás',
                 '2': 'Dois',
                 '3': 'Três'}
    cards = []
    for suit in suits:
        for rank, name in ranks.items():
            cards.append(TrucoCard(suit=suit,rank=rank,name=name))
    print('Baralho criado para a mesa de Truco')
    return cards


#
# my_truco = pyCardDeck.Deck(generate_deck(),name="Truco Sujo", reshuffle=False)
# carta1 = my_truco.draw()
# carta2 = my_truco.draw()
# carta3 = my_truco.draw_random()
# carta4 = my_truco.draw_bottom()
# print(carta1)
# print(carta2)
# print(carta3)
# print(carta4)
# carta1 > carta2
# carta1 > carta3
# carta1 > carta4


class Player:

    def __init__(self, name: str):
        self.hand = []
        self.name = name

    def __str__(self):
        return self.name

class TrucoGame:

    def __init__(self, players: List[Player]):
        self.deck = pyCardDeck.Deck(generate_deck(),name="Truco Sujo", reshuffle=False)
        self.players = players
        self.scores = {}
        print("Jogo criado com {} jogadores.".format(len(self.players)))

    def truco(self):
        """

        """
        print("Preparando...")
        print("Jogador {} embaralhando...".format(self.players[0]))
        self.deck.shuffle()
        print("Tudo misturado! Sem maço!")
        print("")
        print("Distribuindo as cartas...")
        #Muda a ordem dos Jogadores, quem dá cartá é pé:
        self.players.sort(key=self.players[0].__eq__)
        self.deal()
        print("\nVamos jogar!")
        for player in self.players:
            print("{}, sua vez...".format(player.name))
            self.play(player)
        else:
            print("Essa é a última mão... vamos determinar o vencedor...")
            self.find_winner()

    def deal(self):
        """
        Deals three cards to each player.
        """
        for _ in range(3):
            for p in self.players:
                newcard = self.deck.draw()
                p.hand.append(newcard)
                # This will not be here in the future!
                print("Jogador {} recebeu a carta {}.".format(p.name, str(newcard)))

    def find_winner(self):
        """
        Finds the highest score, then finds which player(s) have that score,
        and reports them as the winner.
        """
        winners = []
        try:
            win_score = max(self.scores.values())
            for key in self.scores.keys():
                if self.scores[key] == win_score:
                    winners.append(key)
                else:
                    pass
            winstring = " & ".join(winners)
            print("And the winner is...{}!".format(winstring))
        except ValueError:
            print("Whoops! Everybody lost!")

    def hit(self, player):
        """
        Adds a card to the player's hand and states which card was drawn.
        """
        newcard = self.deck.draw()
        player.hand.append(newcard)
        print("   Drew the {}.".format(str(newcard)))

    def play(self, player):
        """
        An individual player's turn.
        If the player's cards are an ace and a ten or court card,
        the player has a blackjack and wins.
        If a player's cards total more than 21, the player loses.
        Otherwise, it takes the sum of their cards and determines whether
        to hit or stand based on their current score.
        """
        while True:
            points = sum_hand(player.hand)
            if points < 17:
                print("   Hit.")
                self.hit(player)
            elif points == 21:
                print("   {} wins!".format(player.name))
                sys.exit(0) # End if someone wins
            elif points > 21:
                print("   Bust!")
                break
            else:  # Stand if between 17 and 20 (inclusive)
                print("   Standing at {} points.".format(str(points)))
                self.scores[player.name] = points
                break

def sum_hand(hand: list):
    """
    Converts ranks of cards into point values for scoring purposes.
    'K', 'Q', and 'J' are converted to 10.
    'A' is converted to 1 (for simplicity), but if the first hand is an ace
    and a 10-valued card, the player wins with a blackjack.
    """
    vals = [card.rank for card in hand]
    intvals = []
    while len(vals) > 0:
        value = vals.pop()
        try:
            intvals.append(int(value))
        except ValueError:
            if value in ['K', 'Q', 'J']:
                intvals.append(10)
            elif value == 'A':
                intvals.append(1)  # Keep it simple for the sake of example
    if intvals == [1, 10] or intvals == [10, 1]:
        print("   Blackjack!")
        return(21)
    else:
        points = sum(intvals)
        print("   Current score: {}".format(str(points)))
        return(points)


if __name__ == "__main__":
    game = TrucoGame([Player("Felipe"), Player("Marcos"), Player("Pedro"),
        Player("Jose")])
    game.truco()