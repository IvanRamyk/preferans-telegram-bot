import random
import config


def card_suit(card):
    return card % 4 * 1000 + card // 4


class Preferans:
    __state = ''
    __hand0 = []
    __hand1 = []
    __hand2 = []
    __talon = []
    __not_defined = []
    __pass = []
    __tricks_number = 0
    __trump_suit = 0
    __dib = 23
    __first_player = -1
    __move = 0
    __current_player = 0
    __game_type = 0  # 1 - game 2 - miser 3 - all-pass
    __declarer = 0
    __is_misere = False
    __cnt_pass = 0
    __cnt_defined = 0

    @staticmethod
    def set_round():
        Preferans.state = 'bidding'
        config.state = 'bidding'
        Preferans.__hand0 = []
        Preferans.__hand1 = []
        Preferans.__hand2 = []
        Preferans.__talon = []
        Preferans.__pass = [False, False, False]
        Preferans.__not_defined = [True, True, True]
        Preferans.__first_player = (Preferans.__first_player + 1) % 3
        Preferans.__current_player = Preferans.__first_player
        Preferans.__move = Preferans.__first_player
        Preferans.__cnt_defined = 0
        Preferans.__cnt_pass = 0
        card_list = []
        for i in range(28, 60):
            card_list.append(i)
        random.shuffle(card_list)
        for i in range(10):
            Preferans.__hand0.append(card_list[i])
        for i in range(10):
            Preferans.__hand1.append(card_list[10 + i])
        for i in range(10):
            Preferans.__hand2.append(card_list[20 + i])
        Preferans.__hand0.sort(key=card_suit)
        Preferans.__hand1.sort(key=card_suit)
        Preferans.__hand2.sort(key=card_suit)
        for i in range(2):
            Preferans.__talon.append(card_list[30 + i])

    @staticmethod
    def update_bidding(type_answer):
        if type_answer == 1:  # game
            Preferans.__dib += 1
            Preferans.__is_misere = False
            Preferans.__declarer = Preferans.__current_player
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if type_answer == 2:  # misere
            Preferans.__dib = 35
            Preferans.__is_misere = True
            Preferans.__declarer = Preferans.__current_player
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if type_answer == 3:  # pass
            Preferans.__pass[Preferans.__current_player] = True
            Preferans.__cnt_pass += 1
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if Preferans.__cnt_pass == 3:
            Preferans.__game_type = 3
            config.state = 'all-pass'
            return False
        if Preferans.__cnt_defined == 3 and Preferans.__cnt_pass == 2:
            if Preferans.__is_misere:
                Preferans.__game_type = 2
            else:
                Preferans.__game_type = 1
            config.state = 'talon'
            return False
        Preferans.__current_player = (Preferans.__current_player + 1) % 3
        while not Preferans.__not_defined[Preferans.__current_player] and \
                Preferans.__pass[Preferans.__current_player]:
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
        return True

    @staticmethod
    def hand0():
        return Preferans.__hand0

    @staticmethod
    def hand1():
        return Preferans.__hand1

    @staticmethod
    def hand2():
        return Preferans.__hand2

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
