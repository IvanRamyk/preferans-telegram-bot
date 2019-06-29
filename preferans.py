import random


def card_suit(card):
    return card % 4 * 1000 + card // 4


class Preferans:
    __hand0 = []
    __hand1 = []
    __hand2 = []
    __talon = []
    __in_bidding = []
    __tricks_number = 0
    __trump_suit = 0
    __dib = 23
    __first_player = -1
    __move = 0
    __current_player = 0

    def set_round():
        Preferans.__hand0 = []
        Preferans.__hand1 = []
        Preferans.__hand2 = []
        Preferans.__talon = []
        Preferans.__in_bidding = [True, True, True]
        Preferans.__first_player = (Preferans.__first_player + 1) % 3
        Preferans.__move = Preferans.__current_player = Preferans.__first_player
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

    def update_bidding(type_answer):
        if type_answer == 1:  # game
            Preferans.__dib += 1
        begin = Preferans.__current_player
        Preferans.__current_player = (Preferans.__current_player + 1) % 3
        while Preferans.__current_player != begin and not(Preferans.__in_bidding[Preferans.__current_player]):
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
        if Preferans.__current_player == begin:
            return False
        else:
            return True

    def hand0():
        return Preferans.__hand0

    def hand1():
        return Preferans.__hand1

    def hand2():
        return Preferans.__hand2

    def current_player():
        return Preferans.__current_player

    def dib():
        return Preferans.__dib + 1
