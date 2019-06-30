import random
import config


def card_suit(card):
    return card % 4 * 1000 + card // 4


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
    __game_type = 0  # 1 - game 2 - miser 3 - all-pass
    __declarer = 0
    __is_misere = False
    __cnt_pass = 0
    __cnt_defined = 0
    __trick = []
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
        if type_answer == 'raise':  # game
            Preferans.__dib += 1
            Preferans.__is_misere = False
            Preferans.__declarer = Preferans.__current_player
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if type_answer == 'misere':  # misere
            Preferans.__dib = 35
            Preferans.__is_misere = True
            Preferans.__declarer = Preferans.__current_player
            if Preferans.__not_defined[Preferans.__current_player]:
                Preferans.__not_defined[Preferans.__current_player] = False
                Preferans.__cnt_defined += 1
        if type_answer == 'fold':  # pass
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
                Preferans.__trump_suit = -1
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
            if card1_id < card1_id:
                del Preferans.__hand1[card1_id - 1]
            else:
                del Preferans.__hand1[card2_id]
        if Preferans.declarer() == 2:
            del Preferans.__hand2[card1_id]
            if card1_id < card1_id:
                del Preferans.__hand2[card1_id - 1]
            else:
                del Preferans.__hand2[card2_id]
        config.state = 'game'

    @staticmethod
    def set_trump(game):
        Preferans.__tricks_number = game // 4
        Preferans.__trump_suit = game % 4
        Preferans.__current_player = Preferans.__move

    @staticmethod
    def get_card(card):
        suit = card % 4
        Preferans.__card_in_trick += 1
        Preferans.__trick.append(card)
        if Preferans.__card_in_trick == 1:
            Preferans.__current_suit = suit
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
            return True
        if Preferans.__card_in_trick == 2 or (Preferans.__game_type == 3 and Preferans.__tricks_total <= 2):
            Preferans.__current_player = (Preferans.__current_player + 1) % 3
            return True
        if (Preferans.__card_in_trick == 3 and (Preferans.__game_type != 3 or Preferans.__tricks_total > 2)) \
                or Preferans.__card_in_trick == 4:
            def key(card1):
                return (card1 % 4 == Preferans.__trump_suit) * (100 + card1 // 4) + \
                       (card1 // 4) * (card1 % 4 == Preferans.__current_suit)

            def comp(card1, card2):
                return key(card1) > key(card2)
            if Preferans.__tricks_total == 4:
                del Preferans.__trick[0]
            Preferans.__current_player = 0
            if comp(Preferans.__trick[1], Preferans.__trick[Preferans.__current_player]):
                Preferans.__current_player = 1
            if comp(Preferans.__trick[2], Preferans.__trick[Preferans.__current_player]):
                Preferans.__current_player = 2
            Preferans.__player_tricks[Preferans.__current_player] += 1
            Preferans.__trick.clear()
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
        return Preferans.__trick

    @staticmethod
    def player_tricks():
        return Preferans.__player_tricks


'''Preferans.set_round()
Preferans.set_trump(6 * 4)
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())
print(Preferans.get_card(8 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(7 * 4 + 2))
print(Preferans.trick())
print(Preferans.get_card(6 * 4 + 1))
print(Preferans.trick())
print(Preferans.player_tricks())'''
