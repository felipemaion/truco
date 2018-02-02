#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a game: Truco Paulista.
Author: Felipe Maion Garcia
Language: Python 3
Started: 31/jan/2018
"""
#### NEEDED SETUP:
#### pip install pyCardDeck

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
#
    def __init__(self, name: str):
        self.hand = pyCardDeck.Deck(name=name, reshuffle=False)
        self.name = name
#
    def __str__(self):
        return self.name



class TrucoGame:

    def __init__(self, players: List[Player]):
        self.deck = pyCardDeck.Deck(generate_deck(),name="Truco Sujo", reshuffle=False)
        if len(players) not in [2,4,6]:
            raise("Erro: Precisa de 2, 4 ou 6 jogadores")
        self.players = players
        self.teams = {}
        team = 1
        for player in players:
            self.teams[player] = team
            team += 1
            if team > 2:
                team = 1
        print(self.teams)

        self.scores = {}
        self.gameround = {'score': 1, 'first_round': None, 'second_round':None, 'third_round': None, 'last_call':None}
        print("Jogo criado com {} jogadores:".format(len(self.players)))
        print(*self.players, sep=", ")


    def bet(self, current_score = None):
        if not current_score:
            current_score = self.gameround['score']
        if current_score == 1:
            return "Truco!", 3
        if current_score == 3:
            return "Seis!", 6
        if current_score == 6:
            return "Nove!", 9
        if current_score == 9:
            return "Doze!", 12

    def truco(self):
        """

        """
        print("Preparando...")
        print("Jogador {} embaralhando...".format(self.players[0]))
        self.deck.shuffle()
        print("Tudo misturado! Sem maço!")
        print("")
        print("Distribuindo as cartas...")
        # Change order of the players - quem dá cartá é pé:
        self.players.append(self.players.pop(0))
        self.deal()
        print("\nVamos jogar!")
        gameround = True
        while gameround == True:

            for player in self.players:
                print("\n{} - Time {}, sua vez...".format(player.name, self.teams[player]))
                self.play(player)
            else:
                print("\nTodos jogaram!?")
                self.find_winner()
                # Todo: After winner found, re-order players - next player after the winner plays first.

    def deal(self):
        """
        Deals three cards to each player.
        """
        for _ in range(3):
            for p in self.players:
                newcard = self.deck.draw()
                p.hand.add_single(newcard)
                # This will not be here in the future!
                print("Jogador {} recebeu a carta {}.".format(p.name, str(newcard)))
            print("\n")
        self.flop = self.deck.draw()
        print("Vira: {}".format(self.flop))

    def find_winner(self):
        """
        Finds the highest card, then finds which player won, give points to the team.
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


    def play(self, player):
        """
        """
        # Todo implement blind draw (esconder)
        # Show player's hand:
        valid = True
        while valid:
            options = {}
            roundover = False
            for i, card in enumerate(player.hand):
                options[str(i+1)] = card.name
            card = None
            bet = self.bet()
            # Give possibility to raise the bet, if not asked by the team before:
            if self.gameround['last_call'] != self.teams[player]:
                # increase_bet = input("\nPedir {}?".format(bet[0]))
                options['0'] = bet[0]
            else:
                print("Você não pode pedir {}...".format(bet[0]))
            print("Opções:")
            for key, value in options.items():
                print("\t", key, ":", value)
                # Todo: If it is not first round.
                print("\t \t{}{} : Esconde a carta {}".format(key,key, value)) if key != '0' else None

            choice = input(player.name + " escolha " + str([*options.keys()])  + ">> ")
            if choice[0] in options.keys():
                    # Todo: Implement reply from next player.
                if choice == '0':
                    call = self.call_by(player)
                    # self.gameround['score'] = bet[1]

                    valid = True
                else:
                    if len(choice) == 1:
                        print("{} escolheu uma carta...".format(player))
                        card =  player.hand.draw_specific(options[choice[0]])
                        valid = False
                        visible = True
                    elif choice[1] == str(choice[0]):
                        print("{} ESCONDEU uma carta...".format(player))
                        card =  player.hand.draw_specific(options[choice[0]])
                        valid = False
                        visible = False
                    else:
                        valid = True

            else:
                print("Vou jogar qualquer uma...")
                card = player.hand.draw_random()
                visible = True
                valid = False
        print("{}, jogou: {}".format(player, card if visible else None))
        return {'card':card, 'visible':visible, 'roundover':roundover}

    def call_by(self,player):
        index = self.players.index(player) + 1
        if index >= len(self.players):
            index = 0
        called = self.players[index]
        # ToDo: Show only to the player...
        self.gameround['last_call'] = self.teams[player]
        print("{} diz: {}!!! {} MARRECO!!!".format(player, str(self.bet()[0]).upper(), str(called).upper()))

        print("Sua mão,", called, ":", [card.name for card in called.hand])

        print("Opções:")

        if self.gameround['score'] < 9:
            print("\t1: Aceitar - Partida: {} tentos\n\t2: Pedir: {}\n\t0: Fugir - Perde: {} tento(s)".format(self.bet()[1], self.bet(current_score=self.bet()[1])[0], self.gameround['score']))
            options = [1, 2, 0]
        else:
            options = [1, 0]
            print("\t1: Aceitar - Partida: {} tentos\n\t0: Fugir - Perde: {} tentos\n".format(self.bet()[1]),self.gameround['score'] )
        valid = True
        while valid:
            calling = int(input("{} {}? >>".format(called, options)))
            if calling in options:
                if calling == 1:
                    self.gameround['score'] = self.bet()[1]
                    print("Valendo:", self.gameround['score'], "tentos")
                    return # Todo WTF??
                elif calling == 2:
                    self.gameround['score'] = self.bet()[1]
                    print("Valendo:", self.gameround['score'], "tentos")
                    self.call_by(called)
                else:
                    print("Fugiu!!")
                    print("Valeu:", self.gameround['score'], "tentos")
                    return "END GAME"
                valid = False




if __name__ == "__main__":
    game = TrucoGame([Player("Felipe"), Player("Marcos"), Player("Pedro"),
        Player("Jose")])
    game.truco()