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

# import sys
import random
import pyCardDeck
from typing import List
from pyCardDeck.cards import BaseCard


class TrucoCard(BaseCard):
    def __init__(self, suit: str, rank: str, name: str):
        # Define self.name through BaseCard Class
        super().__init__("{} de {}".format(name, suit[1]))
        self.suit = suit[0]
        self.suit_name = suit[1]
        self.rank = rank
    def __eq__(self, other):
        return self.name == other
    def __ge__(self, other):
        ranks = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        # Compare Ranks
        if ranks.index(self.rank) < ranks.index(other.rank):
            return False
        elif ranks.index(self.rank) >= ranks.index(other.rank):
            return True
        else:
            return 0
    def __gt__(self, other):
        ranks = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        # Compare Ranks
        if ranks.index(self.rank) < ranks.index(other.rank):
            return False
        elif ranks.index(self.rank) > ranks.index(other.rank):
            return True
        else:
            return 0

def ranks_names():
    return {'4': 'Quatro', '5': 'Cinco', '6': 'Seis', '7': 'Sete', 'Q': 'Dama', 'J': 'Valete',
     'K': 'Rei', 'A': 'Ás', '2': 'Dois', '3': 'Três'}

def generate_deck(sujo=True) -> List[TrucoCard]:
    """
    Function that generates the deck, instead of writing down all cards, we use iteration
    to generate the cards for use
    :return:    List with all (24/40) cards for truco playing cards
    :rtype:     List[TrucoCard]
    """
    if sujo:
        # ♠♣♥♦
        suits = {1: 'Ouros', 2: 'Espadas', 3: 'Copas', 4: 'Paus'}
        # suits = {1: 'Ouros ♦', 2: 'Espadas ♠', 3: 'Copas ♥', 4: 'Paus ♣'}
        ranks = ranks_names()
    if not sujo:
        suits = {1: 'Ouros', 2: 'Espadas', 3: 'Copas', 4: 'Paus'}
        ranks = {'Q': 'Dama',
                 'J': 'Valete',
                 'K': 'Rei',
                 'A': 'Ás',
                 '2': 'Dois',
                 '3': 'Três'}
    cards = []
    for suit in suits.items():
        for rank, name in ranks.items():
            cards.append(TrucoCard(suit=suit,rank=rank,name=name))
    return cards


# # ToDo Write the tests for the following:
# def test_mydeck:
    # my_truco = pyCardDeck.Deck(generate_deck(),name="Truco Sujo", reshuffle=False)
    # len(my_truco) == 40 # True
    # carta0 = my_truco.draw_specific("Três de Ouros")
    # carta1 = my_truco.draw_specific("Três de Espadas")
    # carta2 = my_truco.draw_specific("Três de Copas")
    # carta3 = my_truco.draw_specific("Três de Paus")
    #
    # carta4 = my_truco.draw_random()
    # carta5 = my_truco.draw_bottom()
    #
    # carta0.name == "Três de Ouros" # True
    # carta0.suit == 1 # True
    # carta0.suit_name == "Ouros" # True
    #
    # carta1.name == "Três de Espadas" # True
    # carta1.suit == 2 # True
    # carta1.suit_name == "Espadas" # True
    #
    # carta2.name == "Três de Copas" # True
    # carta2.suit == 3 # True
    # carta2.suit_name == "Copas" # True
    #
    # carta3.name == "Três de Paus" # True
    # carta3.suit == 4 # True
    # carta3.suit_name == "Paus" # True
    #
    # carta1.rank == carta2.rank and carta0.rank == carta3.rank # True
    # carta1 == carta2 # False
    # carta1 > carta2 # 0
    # carta0.suit < carta1.suit #True
    # carta1.suit < carta2.suit #True
    # carta2.suit < carta3.suit #True
    # carta3.suit > carta0.suit #True
    # carta0 > carta4 # True
    #
    # cartas = [carta1, carta2 , carta3, carta4, carta5, carta0]
    # random.shuffle(cartas)
    # cartas.sort()
    # len(my_truco) == 34 # True
    #
    # tres = [carta1,carta2,carta3,carta0]
    # print(*tres, sep= ", ") # Três de Espadas, Três de Copas, Três de Paus, Três de Ouros
    # tres.sort(key= lambda x: x.suit)
    # print(*tres, sep= ", ") # Três de Ouros, Três de Espadas, Três de Copas, Três de Paus


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
        self.deck = pyCardDeck.Deck(generate_deck(sujo),name="Truco Sujo", reshuffle=False)
        self.sujo = sujo
        self.deck_size = len(self.deck)
        #self.manilha = None # ToDO create a new class RoundGame and move it to there
        if len(players) not in [2,4,6]:
            raise("Erro: Precisa de 2, 4 ou 6 jogadores")
        self.players = players
        self.teams, self.team1, self.team2 = {}, [], []
        self._teams()
        self.scores = {1: 0, 2: 0} #team: score
        # game_roud, cards_round, table... also should be part of the class RoundGame
        # self.game_round = {'score': 1, 'first_round': None, 'second_round':None, 'third_round': None, 'last_bet_call':None}
        # self.cards_round = {}
        # self.table = []
        # I am sure that ranks_names should not be here... but where?
        self.ranks_names = ranks_names()
        self.show_table()

    def createGameRound(self, dealer):
        return TrucoGame.GameRound(self, dealer)

    class GameRound: #also known as Rodada ou Partida.
        def __init__(self, game, dealer: Player):
            self.game = game
            self.dealer = dealer
            self.flop = None
            self.manilha = None
            self.round_score = 1
            self.last_bet_call = None
            self.deck = game.deck
            self.all_cards = generate_deck(game.sujo)
            self.players = game.players
            self.teams = game.teams
            self.cards_round = {}


        def bet(self, current_score=None):
            if not current_score:
                current_score = self.round_score
            if current_score == 1:
                return "Truco!", 3
            if current_score == 3:
                return "Seis!", 6
            if current_score == 6:
                return "Nove!", 9
            if current_score == 9:
                return "Doze!", 12

        def deal(self):
            """
            The dealer gets the deck and deals 3 cards to each player.
            Starting to the player at his right hand.
            The dealer is the last to receive the card.
            """
            self.give_deck_to(self.dealer)
            # Three cards to each player:
            for _ in range(3):
                for player in self.players:
                    newcard = self.deck.draw()
                    player.hand.add_single(newcard)
                    # This will not be here in the future!
                    #print("Jogador {} \trecebeu uma carta \t--SEGREDO:({}).".format(player.name, str(newcard)))
                #print("\n")
            self.flop = self.deck.draw()
            self.shackles(self.flop)
            print("Vira: {}".format(self.flop))
            print("Manilha: ", self.manilha, " - ", ranks_names()[self.manilha])

        def give_deck_to(self, initial=None):
            if initial:  # This is only for GameRound
                while self.players[-1] != initial:
                    self.players.append(self.players.pop(0))

        def find_winner(self):  # This also should be part of a new Class GameRound
            """
            Finds the highest card, then finds which player won, gives points to the team.
            """
            # Todo
            winner = None
            manilhas = {}
            cards = []
            print("Manda: ", self.manilha)
            player_by_card = {}
            for player, play in self.cards_round.items():
                if play['visible'] == True:
                    cards.append(play['card'])
                    player_by_card[play['card'].name] = player
                    print("Jogador: {} jogou {}".format(player, play['card']))  # if play['visible'] == True else None
                    # Looking for shackles in the current table
                    if play['card'].rank == self.manilha:
                        print("Opá!! Temos uma manilha! {} jogada por {}".format(play['card'].suit_name, player))
                        manilhas[player] = play['card']

            if manilhas != {}:
                high_card = max(manilhas.values())
                winner = player_by_card[high_card.name]
                print("Vencedor da rodada: {} com {}".format(winner, high_card))
                # Todo deal with score, winner of the round, etc.
                # Todo change order of players according to the winner.
                return winner
            else:
                deal = []
                high_rank = max(cards).rank
                for card in cards:
                    if card.rank == high_rank:
                        deal.append(card)
                        # Todo: Quem mela torna? Não.. a mão...
            print(cards)
            print("Whoops! Everybody lost!")

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

        def start(self):
            # print("\nVamos jogar!")
            game_round = True
            self.table = []
            while game_round == True:

                for player in self.players:
                    print("\n{} - Time {}, sua vez...".format(player.name, self.teams[player]))
                    played = self.play(player) # Todo: Who should play is the PLAYER!!!
                    # Player, Put the cart on the table:
                    self.table.append(played['card']) if played['card'] != None else None
                    # This card belongs to the player.
                    self.cards_round[player] = played
                    # Does anybody run away of this match? Example: when increasing the bet?
                    if played['round_over'] == True:
                        print("Fim dessa partida!")
                        game_round = False
                        break
                else:  # No more players...
                    print("\nTodos jogaram!?")
                    self.find_winner()
                    # Todo: After winner found, re-order players - next player after the winner plays first.
            # All Players give all cards back to the deck:
            for player in self.players:
                while not player.hand.empty:
                    card = player.hand.draw()
                    self.deck.discard(card)
            # Remove any empty entry in self.table:
            self.table = [x for x in self.table if x is not None]
            # Get cards on the table:
            for card in self.table:
                self.deck.discard(card)
            # Get the Flop and put in the deck:
            self.deck.discard(self.flop)
            # Reset Table and etc
            self.flop = None
            self.table = []

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
                    options[str(i + 1)] = card.name
                card = None
                bet = self.bet()
                # Give possibility to raise the bet, if not asked by the team before:
                if self.last_bet_call != self.teams[player]:
                    # increase_bet = input("\nPedir {}?".format(bet[0]))
                    options['0'] = bet[0]
                else:
                    print("Você não pode pedir {}...".format(bet[0]))
                print("Opções:")
                for key, value in options.items():
                    print("\t", key, ":", value)
                    # Todo: If it is not first round.
                    print("\t \t{}{} : Esconde a carta {}".format(key, key, value)) if key != '0' else None

                choice = input(player.name + " escolha " + str([*options.keys()]) + ">> ")
                if choice[0] in options.keys():
                    if choice == '0':  # Raise Bet!
                        call = self.call_by(player)  # Ask other player
                        if not call:  # Challange not accepted. End round!
                            winner = self.last_bet_call  # Last one to challange wins.
                            self.game.scores[winner] += self.round_score
                            points = self.game.scores[winner]
                            print("Vencedor da rodada time: {} total: {} ".format(winner, points))
                            return {'card': None, 'visible': False, 'round_over': True}

                        valid = True
                    else:
                        if len(choice) == 1:
                            print("{} escolheu uma carta...".format(player))
                            card = player.hand.draw_specific(options[choice[0]])
                            valid = False
                            visible = True
                        elif choice[1] == str(choice[0]):
                            print("{} ESCONDEU uma carta...".format(player))
                            card = player.hand.draw_specific(options[choice[0]])
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
            return {'card': card, 'visible': visible, 'round_over': round_over}

        def call_by(self, player):
            index = self.players.index(player) + 1
            if index >= len(self.players):
                index = 0
            called = self.players[index]
            # ToDo: Show only to the player...
            self.last_bet_call = self.teams[player]
            print("{} diz: {}!!! {} MARRECO!!!".format(player, str(self.bet()[0]).upper(), str(called).upper()))

            print("Sua mão,", called, ":", [card.name for card in called.hand])

            print("Opções:")

            if self.round_score < 9:
                print("\t1: Aceitar - Partida: {} tentos\n\t2: Pedir: {}\n\t0: Fugir - Perde: {} tento(s)".format(
                    self.bet()[1], self.bet(current_score=self.bet()[1])[0], self.round_score))
                options = [1, 2, 0]
            else:
                options = [1, 0]
                print("\t1: Aceitar - Partida: {} tentos\n\t0: Fugir - Perde: {} tentos\n".format(self.bet()[1],
                                                                                                  self.round_score))
            valid = True
            while valid:
                calling = int(input("{} {}? >>".format(called, options)))
                if calling in options:
                    if calling == 1:
                        self.round_score = self.bet()[1]
                        print("Valendo:", self.round_score, "tentos")
                        return True  # Todo WTF??
                    elif calling == 2:
                        self.round_score = self.bet()[1]
                        print("Valendo:", self.round_score, "tentos")
                        return self.call_by(called)
                    else:
                        print("Fugiu!!")
                        print("Valeu:", self.round_score, "tentos")
                        return False
                    # valid = False

    def show_table(self):
        print("Jogo criado com {} jogadores. \n\t Mesa disposta:".format(len(self.players)))
        print("\t", *self.players[:int(len(self.players)/2)][::-1], sep="\t")
        print("\n")
        print("\t", *self.players[int(len(self.players)/2):], sep="\t")

    def _teams(self):
        team = 1
        for player in self.players:
            self.teams[player] = team
            if team == 1:
                self.team1.append(player.name)
            else:
                self.team2.append(player.name)
            team += 1
            if team > 2:
                team = 1

    def pick_dealer(self):
        self.deck.shuffle()
        dealer = None
        max_card = self.deck.draw_specific("Quatro de Ouros") # Lowest card for comparison
        cards = []
        cards.append(max_card)
        print("\nQuem sortear a maior carta e naipe começa embaralhando...")
        for player in self.players:
            card = self.deck.draw_random()
            print("\t{} tirou a carta: {}".format(player, card))
            if card >= max_card:
                if card.rank == max_card.rank:
                    if card.suit > max_card.suit:
                        dealer = player
                        max_card = card
                else:
                    dealer = player
                    max_card = card
            cards.append(card)
        # Give cards back to the deck:
        self.dischard_cards(cards)
        self.deck.shuffle_back()
        print("\nQuem começa é o {}".format(dealer))
        return dealer

    def dischard_cards(self,cards):
        for card in cards:
            self.deck.discard(card)

    def truco(self):
        """
        """

        game = True
        print("\nPreparando...")
        initial_dealer = self.pick_dealer()
        self.change_player_order(initial_dealer)
        while game:

            print("Jogador {} embaralhando...".format(self.players[0]))
            self.deck.shuffle_back()
            if len(self.deck) != self.deck_size:
                raise("Faltando carta! {}!! Pega ladrão!".format(len(self.deck)))
            print("Tudo misturado! Sem maço!")
            print("Ok... corta... {}".format(self.players[-1])) # Bleh!
            print("Distribuindo as cartas...")
            # Change order of the players - quem dá carta é pé:
            # self.change_player_order() # This should not be here... this is GameRound rule.
            # Todo createGameRound
            game_round = self.createGameRound(initial_dealer)
            game_round.deal()
            game_round.start()
            # self.deal() # Also not belongs here.
            self.change_player_order()  # move deck to next player
            # Remove this crap from here:
            #self.game_round = {'score': 1, 'first_round': None, 'second_round': None, 'third_round': None,
            #                  'last_bet_call': None}
            # Check quantity of cards:
            # print("Cartas no maço: {}, cartas na mesa: {}".format(len(self.deck), self.deck.discarded))
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






    def change_player_order(self, initial=None):
        self.players.append(self.players.pop(0))
        if initial: # This is only for GameRound
            while self.players[0] != initial:
                self.players.append(self.players.pop(0))









if __name__ == "__main__":
    game = TrucoGame([Player("Felipe"), Player("Marcos"), Player("Pedro"),
        Player("Jose")])
    game.truco()
    # game = TrucoGame([Player("Felipe"), Player("Marcos"), Player("Pedro"),
    #     Player("Jose"), Player('Bruno'), Player('Aline')])







# Study of how to pass an information from outer class to inner class.

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

