import telebot
#from telebot import types
import config
from preferans import Preferans

bot = telebot.TeleBot(config.Token)
id_list = []
name_list = []
count_id = 0
age = 0


@bot.message_handler(commands=['start'])
def start_messaging(message):
    global count_id
    bot.send_message(message.from_user.id, 'Ты в игре!')
   # get_age(message)
    id_list.append(message.from_user.id)
    name_list.append(message.from_user.first_name)
    count_id += 1
    if count_id == config.cnt_players:
        new_round()


def new_round():
    Preferans.set_round()
    bot.send_message(id_list[0], 'Твои карты:\n' + hand_to_string(Preferans.hand0()))
    bot.send_message(id_list[1], 'Твои карты:\n' + hand_to_string(Preferans.hand1()))
    bot.send_message(id_list[2], 'Твои карты:\n' + hand_to_string(Preferans.hand2()))
    ask_bidding()


@bot.message_handler(func=lambda message: config.state == 'bidding')
def bidding(message):
    if message.from_user.id != id_list[Preferans.current_player()]:
        bot.send_message(message.from_user.id, 'Имей терпение, блэт!')
    elif message.text != '+' and message.text != '-' and message.text != 'мизер':
        bot.send_message(message.from_user.id, 'Неккоректные входные данные')
    else:
        type_answer = 0
        if message.text == '+':
            type_answer = 1
        if message.text == '-':
            type_answer = 3
        if message.text == 'мизер':
            type_answer = 2
        bid_message = 'Игрок ' + message.from_user.first_name + ' сказал '
        if type_answer == 1:
            bid_message += hash_to_sting(Preferans.dib())
        if type_answer == 2:
            bid_message += 'мизер'
        if type_answer == 3:
            bid_message += 'пас'
        for i in range(3):
            if i != Preferans.current_player():
                bot.send_message(id_list[i], bid_message)
        if Preferans.update_bidding(type_answer):
            ask_bidding()
        else:
            result = ''
            if Preferans.game_type() == 1:
                result = 'Играет ' + name_list[Preferans.declarer()] + '. Ждем пока игрок закажет игру.'
            if Preferans.game_type() == 2:
                result = name_list[Preferans.declarer()] + ' играет мизер. Ждем пока игрок понесет карты.'
            if Preferans.game_type() == 3:
                result = 'Распас. Ход с игрока ' + name_list[Preferans.move()]
            for i in id_list:
                bot.send_message(i, result)
            if Preferans.game_type() == 1 or Preferans.game_type() == 2:
                talon = 'Прикуп:\n' + hand_to_string(Preferans.talon())
                for i in id_list:
                    bot.send_message(i, talon)
                bot.send_message(id_list[Preferans.declarer()], 'Ваша рука:' +
                                 hand_to_string(Preferans.add_talon()) + '\nЧто хочешь понести?')


@bot.message_handler(func=lambda message: config.state == 'talon')
def discarding(message):
    cards = message.text.split()
    Preferans.discard(int(cards[0]), int(cards[1]))
    bot.send_message(id_list[Preferans.declarer()], 'Рука превращается в...\n' + hand_to_string(Preferans.hand_declarer()))

def offer_game():
    print(3)


@bot.message_handler(func=lambda message: config.state != 'bidding')
def hz(message):
    print(message.from_user.first_name)


def hash_to_sting(_hash):
    answer = ''
    if _hash // 4 <= 10:
        answer += str(_hash // 4)
    elif _hash // 4 == 11:
        answer += 'J'
    elif _hash // 4 == 12:
        answer += 'Q'
    elif _hash // 4 == 13:
        answer += 'K'
    elif _hash // 4 == 14:
        answer += 'A'
    if _hash % 4 == 0:
        answer += '♠'
    elif _hash % 4 == 1:
        answer += '♣'
    elif _hash % 4 == 2:
        answer += '♦'
    elif _hash % 4 == 3:
        answer += '♥'
    return answer


def hand_to_string(hand):
    answer = ''
    last_suit = -1
    for i in hand:
        if last_suit != - 1 and last_suit != i % 4:
            answer += '\n'
        answer += hash_to_sting(i)
        answer += ' '
        last_suit = i % 4
    return answer


def ask_bidding():
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_raz = telebot.types.InlineKeyboardButton(text=hash_to_sting(Preferans.dib()), callback_data='raise')
    key_pas = telebot.types.InlineKeyboardButton(text='Пас', callback_data='fold')
    key_misere = telebot.types.InlineKeyboardButton(text='Мизер', callback_data='misere')
    keyboard.add(key_raz)
    keyboard.add(key_pas)
    keyboard.add(key_misere)
    question = "Ваша ставка?"
    bot.send_message(id_list[Preferans.current_player()], text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_bidding(call):
    if call.data == 'raise':
        if Preferans.update_bidding(1):
            ask_bidding()
    elif call.data == 'misere':
        if Preferans.update_bidding(2):
            ask_bidding()
    elif call.data == 'fold':
        if Preferans.update_bidding(3):
            ask_bidding()


'''
def ask_bidding():
    bot.send_message(id_list[Preferans.current_player()], 'Ваше слово!!\nМинимальная ставка - '
                     + hash_to_sting(Preferans.dib()) + 'Отправь "+" если хочешь играть, '
                                                        '"-" если хочешь пасануть или "мизер"\n')
'''

bot.polling()
