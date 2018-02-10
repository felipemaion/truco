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
from trucodeck import *




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
        # Not supposed to be here... but where?:
        if len(players) not in [2,4,6]:
            raise("Erro: Precisa de 2, 4 ou 6 jogadores")
        self.players = players
        self.teams, self.team1, self.team2 = {}, [], []
        self._teams()
        self.scores = {1: 0, 2: 0} #team: score
        self.ranks_names = ranks_names()
        self.show_table()

    def createGameRound(self, dealer):
        return TrucoGame.GameRound(self, dealer)

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
            print("\t{} \ttirou a carta: {}".format(player, card))
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
        all_dealers = []
        while game:

            print("Jogador {} embaralhando...".format(self.players[0]))
            self.deck.shuffle_back()
            if len(self.deck) != self.deck_size:
                raise("Faltando carta! {}!! Pega ladrão!".format(len(self.deck)))
            print("Tudo misturado! Sem maço!")
            print("Ok... corta... {}".format(self.players[-1])) # Bleh!
            print("Distribuindo as cartas...")
            all_dealers.append(initial_dealer.name)
            game_round = self.createGameRound(initial_dealer)
            game_round.deal()
            game_round.start()
            print("======================")
            initial_dealer = self.change_player_order()  # move deck to next player
            print("Placar: \n")
            print("\tTime 1\t x\t Time 2")
            print(" \t{}\t x\t {}".format(self.scores[1],self.scores[2]))
            print("======================")

            print(all_dealers) # Debuging help
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
        return self.players[0]



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
            self.players = game.players.copy()
            self.teams = game.teams
            self.cards_round = {}
            self.winners = [] # Who won each turn of the round 3/3

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
            if current_score == 12:
                return "", 0

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
                #     print("Jogador {} \trecebeu uma carta \t--SEGREDO:({}).".format(player.name, str(newcard)))
                # print("\n")
            self.flop = self.deck.draw()
            self.shackles(self.flop)
            # print("Vira: {}".format(self.flop))
            # print("Manilha: ", self.manilha, " - ", ranks_names(self.manilha))

        def give_deck_to(self, initial=None):
            if initial:  # This is only for GameRound
                while self.players[-1] != initial:
                    self.players.append(self.players.pop(0))

        def next_to_play(self, player):
            if player:  # This is only for GameRound
                while self.players[0] != player:
                    self.players.append(self.players.pop(0))

        def find_winner(self):  # This also should be part of a new Class GameRound
            """
            Finds the highest card, then finds which player won, gives points to the team.
            """
            # Todo
            winner = None
            manilhas = {}
            cards = []
            print("Manilha: ", self.manilha)
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
                high_suit = 0 #max(manilhas.values()) # Todo: Bug in max() -> order of manilhas matters in the pile.
                high_card = None
                winner = None
                for player, manilha in manilhas.items():
                    if manilha.suit > high_suit:
                        high_suit = manilha.suit
                        high_card = manilha
                        winner = player
                # winner = player_by_card[high_card.name]
                print("\n\n\tVencedor da rodada: {} com {}".format(winner,high_card))
                return winner
            else:
                tied = []
                if not cards:
                    return None
                high_rank = max(cards).rank
                for card in cards:
                    if card.rank == high_rank:
                        tied.append(card)
                if len(tied) > 1:
                    print("\n\n\tEmpate!")
                    return None
                else:
                    winner = player_by_card[tied[0].name]
                    print("\n\t{} jogou a maior carta {}".format(winner, tied[0]))
                    return winner


        def shackles(self, card):
            ranks = []
            shackles = []
            for current_card in self.all_cards:
                for rank in current_card.rank:
                    ranks.append(rank) if rank not in ranks else None
                    shackles.append(rank) if rank not in shackles else None
            shackles.append(shackles.pop(0))
            dictionary = dict(zip(ranks, shackles))
            self.manilha = dictionary[card.rank]
            return dictionary[card.rank]

        def start(self):
            # print("Vamos jogar!")
            game_round = True
            self.table = []
            self.count_round = 1
            while game_round == True:
                # Turn of the player:
                for player in self.players:

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
                    winner = self.find_winner()
                    game_round = self.check_round_alive(winner)
                    self.count_round += 1
                    # print("\n")
            self.dischard_cards()

        def check_round_alive(self, winner):
            # The round (rodada) keeps alive? No team winner?
            if winner:
                self.winners.append(self.teams[winner])
                self.next_to_play(winner)
            else:
                self.winners.append(winner)
            #print(self.winners) # debug helping..
            if self.count_round == 1:
                return True # Keep playing guys.

            if self.count_round == 2:
                if self.winners[0] == self.winners[1] and self.winners[0]:
                    winner = self.winners[1]
                    self.game.scores[winner] += self.round_score
                    print("Vencedor da rodada: Time {}: +{} tentos".format(winner,self.round_score))
                    return False
                if self.winners[1] and not self.winners[0]: # Tied first but not second.
                    winner = self.winners[1]
                    self.game.scores[winner] += self.round_score
                    print("Vencedor da rodada: Time {}: +{} tentos".format(winner,self.round_score))
                    return False
                if self.winners[0] and not self.winners[1]: # Won first but tied second.
                    winner = self.winners[0]
                    self.game.scores[winner] += self.round_score
                    print("A primeira é caminhão de boi! Venceu time {}: +{} tentos".format(winner,self.round_score))
                    return False
                return True # both are Tied. Play last one!

            if self.count_round == 3:
                if not self.winners[0] and not self.winners[1] and not self.winners[2]:
                    print("EMPATE 3/3!!!!")
                    return False
                if self.winners[2]:
                    winner = self.winners[2]
                    self.game.scores[winner] += self.round_score
                    print("Rodada disputada e vencida pelo time {}: +{} tentos".format(winner,
                                                                                       self.round_score))
                    return False

        def dischard_cards(self):
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
            self.winners = []
            self.count_round = 1

        def play(self, player):
            """
            """
            valid = True
            while valid:
                options = {}
                round_over = False
                for i, card in enumerate(player.hand):
                    options[str(i + 1)] = card
                card = None
                bet = self.bet()
                # Give possibility to raise the bet, if not asked by the team before:
                if self.last_bet_call != self.teams[player] and self.round_score != 12:
                    # increase_bet = input("\nPedir {}?".format(bet[0]))
                    options['0'] = bet[0]
                else:
                    print("Você não pode pedir {}...".format(bet[0]))

                print("\n\tVira: {}\n\tManilhas: {}: {}".format(self.flop, self.manilha, ranks_names(self.manilha)))
                print("{} - Time {}, sua vez...".format(player.name, self.teams[player]))
                print("Opções:")
                for key, value in options.items():
                    print("\t{}: {} ".format(key,value))
                    # Todo: If it is not first round.
                    print("\t \t{}{}: Esconde a carta {}".format(key, key, value)) if key != '0' else None

                # I BET THERE IS A BETTER WAY TO SOLVE THIS ISSUE: (Error when pressing just Enter)
                valid_choice = False
                while not valid_choice:
                    choice = input(player.name + " escolha " + str([*options.keys()]) + ">> ")
                    if choice in ['0','1','2','3','4','11','22','33']: valid_choice = True # '4' is random card.
                # Todo: Bug if empty input!!


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

                else: # Option '4'
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
            # Todo : Put different phrases when challanging... :)
            # challange_by(player, worth, who)
            print("{} grita: {}!!! {}, MARRECO!!!".format(player, str(self.bet()[0]).upper(), str(called).upper()))

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
                try:
                    calling = int(input("{} {}? >>".format(called, options)))
                except:
                    continue
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







if __name__ == "__main__":
    valid = True
    while valid:
        try:
            option = int(input("Jogo para 2, 4 ou 6 Jogadores? [2, 4, 6]>> "))
        except:
            continue
        if option in [2,4,6]:
            if option == 6:
                game = TrucoGame([Player("Felipe"), Player("Marcos"), Player("Pedro"), Player("Jose"),
                                  Player("Bruno"), Player("Ivo")])
                valid = False
            if option == 4:
                game = TrucoGame([Player("Felipe"), Player("Marcos"), Player("Pedro"), Player("Jose")])
                valid = False
            if option == 2:
                game = TrucoGame([Player("Felipe"), Player("Pedro")])
                valid = False
            game.truco()








