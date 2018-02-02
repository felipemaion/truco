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

    def __init__(self, players: List[Player], sujo=True):
        self.all_cards = generate_deck(sujo)
        self.deck = pyCardDeck.Deck(self.all_cards.copy(),name="Truco Sujo", reshuffle=False)
        self.sujo = sujo
        self.deck_size = len(self.deck)
        self.manilha = None
        if len(players) not in [2,4,6]:
            raise("Erro: Precisa de 2, 4 ou 6 jogadores")
        self.players = players
        self.teams, self.team1, self.team2 = {}, [], []
        team = 1
        for player in players:
            self.teams[player] = team
            if team == 1:
                self.team1.append(player.name)
            else:
                self.team2.append(player.name)
            team += 1
            if team > 2:
                team = 1
        self.scores = {1: 0, 2: 0} #team: score
        self.game_round = {'score': 1, 'first_round': None, 'second_round':None, 'third_round': None, 'last_call':None}
        self.cards_round = {}
        self.table = []
        self.ranks_names = {'4': 'Quatro', '5': 'Cinco', '6': 'Seis', '7': 'Sete', 'Q': 'Dama', 'J': 'Valete',
                            'K': 'Rei', 'A': 'Ás', '2': 'Dois', '3': 'Três'}
        print("Jogo criado com {} jogadores:".format(len(self.players)))
        print(*self.players, sep=", ")


    def bet(self, current_score = None):
        if not current_score:
            current_score = self.game_round['score']
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

        game = True
        while game:
            print("Preparando...")
            print("Jogador {} embaralhando...".format(self.players[0]))
            self.deck.shuffle_back()
            if len(self.deck) != self.deck_size:
                raise("Faltando carta! {}".format(len(self.deck)))
            print("Tudo misturado! Sem maço!")
            print("")
            print("Distribuindo as cartas...")
            # Change order of the players - quem dá cartá é pé:
            self.players.append(self.players.pop(0))
            self.deal()
            print("\nVamos jogar!")
            game_round = True
            self.table = []
            while game_round == True:

                for player in self.players:
                    print("\n{} - Time {}, sua vez...".format(player.name, self.teams[player]))
                    played = self.play(player)
                    # print(played)
                    self.table.append(played['card']) if played['card'] != None else None
                    self.cards_round[player] = played
                    # print(self.cards_round)
                    if played['round_over'] == True:
                        print("Fim dessa partida!")
                        game_round = False
                        break
                else: # No more players...
                    print("\nTodos jogaram!?")
                    self.find_winner()
                    # Todo: After winner found, re-order players - next player after the winner plays first.
            for player in self.players:
                while not player.hand.empty:
                    card = player.hand.draw()
                    # print(card)
                    self.deck.discard(card)
            # Remove any empty entry in self.table:
            self.table = [x for x in self.table if x is not None]
            for card in self.table:
                self.deck.discard(card)
            # print(self.flop)
            self.deck.discard(self.flop)
            # Reset Table and etc
            self.flop = None
            self.table = []
            self.game_round = {'score': 1, 'first_round': None, 'second_round': None, 'third_round': None,
                              'last_call': None}

            print("Cartas no maço: {}, cartas na mesa: {}".format(len(self.deck), self.deck.discarded))
            print("Placar: \n\tTime1: {} x {} :Time2".format(self.scores[1],self.scores[2]))
            if self.scores[1] >= 12:
                game = False
                print("Fim de Jogo!!")
                print("Vitória do time 1: ", [*self.team1])
                print("Adeus!")
            if self.scores[2] >= 12:
                game = False
                print("Fim de Jogo!!")
                print("Vitória do time 2: ", [*self.team2])
                print("Adeus!")
    def deal(self):
        """
        Deals three cards to each player.
        """
        for _ in range(3):
            for p in self.players:
                newcard = self.deck.draw()
                p.hand.add_single(newcard)
                # This will not be here in the future!
                # print("Jogador {} recebeu a carta {}.".format(p.name, str(newcard)))
            print("\n")
        self.flop = self.deck.draw()
        self.shackles(self.flop)
        print("Vira: {}".format(self.flop))
        print("Manilha: ", self.manilha, " - ", self.ranks_names[self.manilha])

    def find_winner(self):
        """
        Finds the highest card, then finds which player won, gives points to the team.
        """
        # Todo
        print("Manda: ", self.manilha)
        for player, play in self.cards_round.items():
            print("Jogador: {} jogou {}".format(player, play['card'].rank)) if play['visible'] == True else None

        print("Whoops! Everybody lost!")


    def play(self, player):
        """
        """
        # Todo implement blind draw (esconder)
        # Show player's hand:
        valid = True
        while valid:
            options = {}
            round_over = False
            for i, card in enumerate(player.hand):
                options[str(i+1)] = card.name
            card = None
            bet = self.bet()
            # Give possibility to raise the bet, if not asked by the team before:
            if self.game_round['last_call'] != self.teams[player]:
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
                if choice == '0': # Raise Bet!
                    call = self.call_by(player) # Ask other player
                    if not call: # Challange not accepted. End round!
                        winner = self.game_round['last_call'] # Last one to challange wins.
                        self.scores[winner] += self.game_round['score']
                        points = self.scores[winner]
                        print("Vencedor da rodada time: {} total: {} ".format(winner,points))
                        return {'card': None, 'visible': False, 'round_over': True}


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
        return {'card':card, 'visible':visible, 'round_over':round_over}

    def call_by(self,player):
        index = self.players.index(player) + 1
        if index >= len(self.players):
            index = 0
        called = self.players[index]
        # ToDo: Show only to the player...
        self.game_round['last_call'] = self.teams[player]
        print("{} diz: {}!!! {} MARRECO!!!".format(player, str(self.bet()[0]).upper(), str(called).upper()))

        print("Sua mão,", called, ":", [card.name for card in called.hand])

        print("Opções:")

        if self.game_round['score'] < 9:
            print("\t1: Aceitar - Partida: {} tentos\n\t2: Pedir: {}\n\t0: Fugir - Perde: {} tento(s)".format(self.bet()[1], self.bet(current_score=self.bet()[1])[0], self.game_round['score']))
            options = [1, 2, 0]
        else:
            options = [1, 0]
            print("\t1: Aceitar - Partida: {} tentos\n\t0: Fugir - Perde: {} tentos\n".format(self.bet()[1],self.game_round['score'] ))
        valid = True
        while valid:
            calling = int(input("{} {}? >>".format(called, options)))
            if calling in options:
                if calling == 1:
                    self.game_round['score'] = self.bet()[1]
                    print("Valendo:", self.game_round['score'], "tentos")
                    return True# Todo WTF??
                elif calling == 2:
                    self.game_round['score'] = self.bet()[1]
                    print("Valendo:", self.game_round['score'], "tentos")
                    return self.call_by(called)
                else:
                    print("Fugiu!!")
                    print("Valeu:", self.game_round['score'], "tentos")
                    return False
                valid = False

    def shackles(self, card):
        ranks = []
        shackles = []
        # print(self.all_cards)
        for current_card in self.all_cards:
            for rank in current_card.rank:
                # print(rank)
                ranks.append(rank) if rank not in ranks else None
                shackles.append(rank) if rank not in shackles else None
        shackles.append(shackles.pop(0))
        dictionary = dict(zip(ranks, shackles))
        # print(ranks)
        # print(shackles)
        self.manilha = dictionary[card.rank]
        return dictionary[card.rank]


if __name__ == "__main__":
    game = TrucoGame([Player("Felipe"), Player("Marcos"), Player("Pedro"),
        Player("Jose")])
    game.truco()