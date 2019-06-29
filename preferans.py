import random


def card_suit(card):
    return card % 4 * 1000 + card // 4


class Preferans:
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

    def set_round(self):
        Preferans.__hand0 = []
        Preferans.__hand1 = []
        Preferans.__hand2 = []
        Preferans.__talon = []
        Preferans.__pass = [False, False, False]
        Preferans.__not_defined = [True, True, True]
        Preferans.__first_player = (Preferans.__first_player + 1) % 3
        Preferans.__move = Preferans.__current_player = Preferans.__first_player
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

    def update_bidding(self, type_answer):
        if type_answer == 1:  # game
            Preferans.__dib += 1
            Preferans.__is_misere = False
            Preferans.__declarer = Preferans.__current_player
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if type_answer == 2:  # misere
            Preferans.__dib = 31
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
            return False
        if Preferans.__cnt_defined == 3 and Preferans.__cnt_pass == 2:
            if Preferans.__is_misere:
                Preferans.__game_type = 2
            else:
                Preferans.__game_type = 1
            return False
        Preferans.__current_player = (Preferans.__current_player + 1) % 3
        while not Preferans.__not_defined[Preferans.__current_player] and \
                Preferans.__pass[Preferans.__current_player]:
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
        return True

    def hand0(self):
        return Preferans.__hand0

    def hand1(self):
        return Preferans.__hand1

    def hand2(self):
        return Preferans.__hand2

    def current_player(self):
        return Preferans.__current_player

    def dib(self):
        return Preferans.__dib + 1
