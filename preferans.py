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
    __game_type = ''  # game, misere, all-pass
    __declarer = 0
    __is_misere = False
    __cnt_pass = 0
    __cnt_defined = 0
    __tricks = []
    __player_tricks = [0, 0, 0]
    __card_in_trick = 0
    __current_suit = 0
    __tricks_total = 0

    @staticmethod
    def set_round():
        Preferans.state = 'bidding'
        config.state = 'bidding'
        Preferans.__hand0 = []
        Preferans.__hand1 = []
        Preferans.__hand2 = []
        Preferans.__talon = []
        Preferans.__player_tricks = [0, 0, 0]
        Preferans.__tricks_total = 0
        Preferans.__pass = [False, False, False]
        Preferans.__not_defined = [True, True, True]
        Preferans.__first_player = (Preferans.__first_player + 1) % 3
        Preferans.__current_player = Preferans.__first_player
        Preferans.__move = Preferans.__first_player
        Preferans.__cnt_defined = 0
        Preferans.__cnt_pass = 0
        Preferans.__tricks_number = 0
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
        if type_answer == 'raise':
            Preferans.__dib += 1
            Preferans.__is_misere = False
            Preferans.__declarer = Preferans.__current_player
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if type_answer == 'misere':
            Preferans.__dib = 35
            Preferans.__is_misere = True
            Preferans.__declarer = Preferans.__current_player
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if type_answer == 'fold':
            Preferans.__pass[Preferans.__current_player] = True
            Preferans.__cnt_pass += 1
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if Preferans.__cnt_pass == 3:
            Preferans.__game_type = 'all-pass'
            config.state = 'all-pass'
            return False
        if Preferans.__cnt_defined == 3 and Preferans.__cnt_pass == 2:
            if Preferans.__is_misere:
                Preferans.__game_type = 'misere'
                Preferans.__trump_suit = -1
            else:
                Preferans.__game_type = 'game'
            config.state = 'talon'
            return False
        Preferans.__current_player = (Preferans.__current_player + 1) % 3
        while not Preferans.__not_defined[Preferans.__current_player] and \
                Preferans.__pass[Preferans.__current_player]:
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
        return True

    @staticmethod
    def add_talon():
        if Preferans.declarer() == 0:
            Preferans.__hand0.append(Preferans.__talon[0])
            Preferans.__hand0.append(Preferans.__talon[1])
            Preferans.__hand0.sort(key=card_suit)
            return Preferans.__hand0
        if Preferans.declarer() == 1:
            Preferans.__hand1.append(Preferans.__talon[0])
            Preferans.__hand1.append(Preferans.__talon[1])
            Preferans.__hand1.sort(key=card_suit)
            return Preferans.__hand1
        if Preferans.declarer() == 2:
            Preferans.__hand2.append(Preferans.__talon[0])
            Preferans.__hand2.append(Preferans.__talon[1])
            Preferans.__hand2.sort(key=card_suit)
            return Preferans.__hand2

    @staticmethod
    def discard(card1_id, card2_id):
        if Preferans.declarer() == 0:
            del Preferans.__hand0[card1_id]
            if card1_id < card2_id:
                del Preferans.__hand0[card2_id - 1]
            else:
                del Preferans.__hand0[card2_id]
        if Preferans.declarer() == 1:
            del Preferans.__hand1[card1_id]
            if card1_id < card2_id:
                del Preferans.__hand1[card1_id - 1]
            else:
                del Preferans.__hand1[card2_id]
        if Preferans.declarer() == 2:
            del Preferans.__hand2[card1_id]
            if card1_id < card2_id:
                del Preferans.__hand2[card1_id - 1]
            else:
                del Preferans.__hand2[card2_id]
        if Preferans.__game_type == 'game':
            config.state = 'set_game'
        else:
            config.state = 'game'

    @staticmethod
    def set_game(game):
        Preferans.__tricks_number = game // 4
        Preferans.__trump_suit = game % 4
        Preferans.__current_player = Preferans.__move
        config.state = 'game'

    @staticmethod
    def get_card(card_id):
        card = 0
        if Preferans.__current_player == 0:
            card = Preferans.__hand0[card_id]
            del Preferans.__hand0[card_id]
        if Preferans.__current_player == 1:
            card = Preferans.__hand1[card_id]
            del Preferans.__hand1[card_id]
        if Preferans.__current_player == 2:
            card = Preferans.__hand2[card_id]
            del Preferans.__hand2[card_id]
        suit = card % 4
        Preferans.__card_in_trick += 1
        trick = Trick()
        trick.card = card
        trick.player = Preferans.current_player()
        Preferans.__tricks.append(trick)
        if Preferans.__card_in_trick == 1:
            Preferans.__current_suit = suit
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
            return True
        if Preferans.__card_in_trick == 2 or (Preferans.__game_type == 3 and Preferans.__tricks_total <= 2):
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
            return True
        if (Preferans.__card_in_trick == 3 and (Preferans.__game_type != 3 or Preferans.__tricks_total > 2)) \
                or Preferans.__card_in_trick == 4:
            def key(trick1):
                value = 0
                if trick1.card % 4 == Preferans.__trump_suit:
                    value += 1000 + trick1.card // 4
                if trick1.card % 4 == Preferans.__current_suit:
                    value += trick1.card // 4
                print(Preferans.__trump_suit)
                return value

            def comp(card1, card2):
                return key(card1) > key(card2)
            Preferans.__current_player = 0
            if comp(Preferans.__tricks[1], Preferans.__tricks[Preferans.__current_player]):
                Preferans.__current_player = 1
            if comp(Preferans.__tricks[2], Preferans.__tricks[Preferans.__current_player]):
                Preferans.__current_player = 2
            Preferans.__current_player = Preferans.__tricks[Preferans.current_player()].player
            Preferans.__player_tricks[Preferans.__current_player] += 1
            Preferans.__tricks.clear()
            Preferans.__card_in_trick = 0
            Preferans.__tricks_total += 1
            if Preferans.__tricks_total == 10:
                return False
            else:
                return True

    @staticmethod
    def hand_declarer():
        if Preferans.declarer() == 0:
            return Preferans.__hand0
        if Preferans.declarer() == 1:
            return Preferans.__hand1
        if Preferans.declarer() == 2:
            return Preferans.__hand2

    @staticmethod
    def current_hand():
        if Preferans.current_player() == 0:
            return Preferans.__hand0
        if Preferans.current_player() == 1:
            return Preferans.__hand1
        if Preferans.current_player() == 2:
            return Preferans.__hand2

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

    @staticmethod
    def trick():
        return Preferans.__tricks

    @staticmethod
    def player_tricks():
        return Preferans.__player_tricks
