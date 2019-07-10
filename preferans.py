import random
import config


def card_suit(card):
    return card % 4 * 1000 + card // 4


class Trick:
    def __init__(self):
        self.card = 0
        self.player = 0


class Preferans:
    __pool = [0, 0, 0]
    __whist = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
    __mountain = [0, 0, 0]
    __hand = [[], [], []]
    __talon = []
    __not_defined = []
    __pass = []
    __tricks_number = 0
    __trump_suit = 0
    __dib = 23
    __first_player = -1
    __move = 0
    __current_player = 0
    __game_type = ''  # game, misere, all-pass
    __declarer = 0
    __is_misere = False
    __cnt_pass = 0
    __cnt_defined = 0
    __trick = []
    __defenders = []
    __player_tricks = [0, 0, 0]
    __cards_in_trick = 0
    __current_suit = 0
    __tricks_total = 0
    __last_trick = []
    __discarded = 0

    @staticmethod
    def next_player(player):
        return (player + 1) % 3

    @staticmethod
    def inc_discard():
        Preferans.__discarded = (Preferans.__discarded+1) % 3

    @staticmethod
    def discarded():
        return Preferans.__discarded

    @staticmethod
    def set_round():
        config.state = 'bidding'
        Preferans.__hand[0] = []
        Preferans.__hand[1] = []
        Preferans.__hand[2] = []
        Preferans.__talon = []
        Preferans.__player_tricks = [0, 0, 0]
        Preferans.__tricks_total = 0
        Preferans.__pass = [False, False, False]
        Preferans.__not_defined = [True, True, True]
        Preferans.__first_player = Preferans.next_player(Preferans.__first_player)
        Preferans.__current_player = Preferans.__first_player
        Preferans.__move = Preferans.__first_player
        Preferans.__cnt_defined = 0
        Preferans.__cnt_pass = 0
        Preferans.__tricks_number = 0
        Preferans.__dib = 23
        Preferans.__defenders.clear()
        card_list = []
        for i in range(28, 60):
            card_list.append(i)
        random.shuffle(card_list)
        for i in range(10):
            Preferans.__hand[0].append(card_list[i])
        for i in range(10):
            Preferans.__hand[1].append(card_list[10 + i])
        for i in range(10):
            Preferans.__hand[2].append(card_list[20 + i])
        Preferans.__hand[0].sort(key=card_suit)
        Preferans.__hand[1].sort(key=card_suit)
        Preferans.__hand[2].sort(key=card_suit)
        for i in range(2):
            Preferans.__talon.append(card_list[30 + i])

    @staticmethod
    def update_bidding(type_answer):
        if Preferans.__not_defined[Preferans.__current_player]:
            Preferans.__not_defined[Preferans.__current_player] = False
            Preferans.__cnt_defined += 1
        if type_answer == 'raise':
            Preferans.__dib += 1
            Preferans.__is_misere = False
            Preferans.__declarer = Preferans.__current_player
        if type_answer == 'misere':
            Preferans.__dib = 35
            Preferans.__is_misere = True
            Preferans.__declarer = Preferans.__current_player
        if type_answer == 'fold':
            Preferans.__pass[Preferans.__current_player] = True
            Preferans.__cnt_pass += 1
        if Preferans.__cnt_pass == 3:
            Preferans.__game_type = 'all-pass'
            config.state = 'game'
            return False
        if Preferans.__cnt_defined == 3 and Preferans.__cnt_pass == 2:
            if Preferans.__is_misere:
                Preferans.__game_type = 'misere'
                Preferans.__trump_suit = -1
            else:
                Preferans.__game_type = 'game'
            config.state = 'talon'
            return False
        Preferans.__current_player = Preferans.next_player(Preferans.__current_player)
        while not Preferans.__not_defined[Preferans.__current_player] and \
                Preferans.__pass[Preferans.__current_player]:
            Preferans.__current_player = Preferans.next_player(Preferans.__current_player)
        return True

    @staticmethod
    def add_talon():
        Preferans.__hand[Preferans.declarer()].append(Preferans.__talon[0])
        Preferans.__hand[Preferans.declarer()].append(Preferans.__talon[1])
        Preferans.__hand[Preferans.declarer()].sort(key=card_suit)
        return Preferans.__hand[Preferans.declarer()]

    @staticmethod
    def discard(card1_id):
        del Preferans.__hand[Preferans.declarer()][card1_id]

    @staticmethod
    def set_game(game):
        Preferans.__tricks_number = game // 4
        Preferans.__trump_suit = game % 4
        Preferans.__current_player = Preferans.next_player(Preferans.__declarer)
        Preferans.__cnt_defined = 0
        config.state = 'whist'

    @staticmethod
    def get_card(card_id):
        card = Preferans.__hand[Preferans.__current_player][card_id]
        del Preferans.__hand[Preferans.__current_player][card_id]
        suit = card % 4
        Preferans.__cards_in_trick += 1
        trick = Trick()
        trick.card = card
        trick.player = Preferans.current_player()
        Preferans.__trick.append(trick)
        if Preferans.__cards_in_trick == 1:
            Preferans.__current_suit = suit
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
            return True
        if Preferans.__cards_in_trick == 2 or (Preferans.__cards_in_trick == 3 and Preferans.__game_type == 'all-pass'
                                               and Preferans.__tricks_total <= 2):
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
            return True
        if Preferans.__cards_in_trick >= 3:
            def key(trick1):
                value = 0
                if trick1.card % 4 == Preferans.__trump_suit:
                    value += 1000 + trick1.card // 4
                if trick1.card % 4 == Preferans.__current_suit:
                    value += trick1.card // 4
                return value

            def comp(card1, card2):
                return key(card1) > key(card2)
            if Preferans.__game_type == 'all-pass' and Preferans.__tricks_total <= 2:
                Preferans.__current_player = 1
                if comp(Preferans.__trick[2], Preferans.__trick[Preferans.__current_player]):
                    Preferans.__current_player = 2
                if comp(Preferans.__trick[3], Preferans.__trick[Preferans.__current_player]):
                    Preferans.__current_player = 3
            else:
                Preferans.__current_player = 0
                if comp(Preferans.__trick[1], Preferans.__trick[Preferans.__current_player]):
                    Preferans.__current_player = 1
                if comp(Preferans.__trick[2], Preferans.__trick[Preferans.__current_player]):
                    Preferans.__current_player = 2
            Preferans.__current_player = Preferans.__trick[Preferans.current_player()].player
            Preferans.__player_tricks[Preferans.__current_player] += 1
            Preferans.__last_trick.clear()
            for i in Preferans.__trick:
                temp_card = Trick()
                temp_card.player = i.player
                temp_card.card = i.card
                Preferans.__last_trick.append(temp_card)
            Preferans.__trick.clear()
            Preferans.__cards_in_trick = 0
            Preferans.__tricks_total += 1
            if Preferans.__tricks_total == 10:
                return False
            else:
                return True

    '''@staticmethod
    def score():
        print('Ok')
        if Preferans.__game_type == 'game':
            if Preferans.__player_tricks[Preferans.__declarer] >= Preferans.__dib // 4:
                Preferans.__pool[Preferans.__declarer] += (Preferans.__dib // 4 - 5) * 2
                for i in range(3):
                    if i != Preferans.__declarer:
                        Preferans.__whist[i][Preferans.__declarer] += Preferans.__player_tricks[i]'''

    @staticmethod
    def get_whist(is_whist):
        Preferans.__cnt_defined += 1
        if is_whist:
            Preferans.__defenders.append(Preferans.current_player())
        if Preferans.__cnt_defined == 2:
            config.state = 'game'
            Preferans.__current_player = Preferans.__move
            return False
        else:
            return True

    @staticmethod
    def add_pass_card():
        Preferans.__trick.append(Preferans.__talon[0])
        del Preferans.__talon[0]

    @staticmethod
    def hand_declarer():
        return Preferans.__hand[Preferans.declarer()]

    @staticmethod
    def current_hand():
        return Preferans.__hand[Preferans.current_player()]

    @staticmethod
    def hand0():
        return Preferans.__hand[0]

    @staticmethod
    def hand1():
        return Preferans.__hand[1]

    @staticmethod
    def hand2():
        return Preferans.__hand[2]

    @staticmethod
    def current_player():
        return Preferans.__current_player

    @staticmethod
    def dib():
        return Preferans.__dib + 1

    @staticmethod
    def state():
        return config.state

    @staticmethod
    def game_type():
        return Preferans.__game_type

    @staticmethod
    def declarer():
        return Preferans.__declarer

    @staticmethod
    def move():
        return Preferans.__move

    @staticmethod
    def talon():
        return Preferans.__talon

    @staticmethod
    def trick():
        return Preferans.__trick

    @staticmethod
    def player_tricks():
        return Preferans.__player_tricks

    @staticmethod
    def last_trick():
        return Preferans.__last_trick

    @staticmethod
    def cards_in_trick():
        return Preferans.__cards_in_trick
