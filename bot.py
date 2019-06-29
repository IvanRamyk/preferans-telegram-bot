import telebot
import const
from preferans import Preferans

bot = telebot.TeleBot(const.Token)
id_list = []
count_id = 0


@bot.message_handler(commands=['start'])
def start_messaging(message):
    global count_id
    bot.send_message(message.from_user.id, 'Ты в игре!')
    id_list.append(message.from_user.id)
    count_id += 1
    if count_id == const.cnt_players:
        new_round(message)


def new_round(message):
    Preferans.set_round()
    bot.send_message(id_list[0], 'Твои карты:\n' + hand_to_string(Preferans.hand0()))
    bot.send_message(id_list[1], 'Твои карты:\n' + hand_to_string(Preferans.hand1()))
    bot.send_message(id_list[2], 'Твои карты:\n' + hand_to_string(Preferans.hand2()))
    bidding(message)


def bidding(message):
    bot.send_message(id_list[Preferans.current_player()], 'Ваше слово!!\nМинимальная ставка - '
                     + hash_to_sting(Preferans.dib()) + 'Отправь "+" если хочешь играть, '
                                                        '"-" если хочешь пасануть и "мизер" если хочешь сказать мизер\n')
    bot.register_next_step_handler(message, bidding)


def get_answer(message):
    if message.from_user.id != id_list[Preferans.current_player()] \
            or (message.text != '+' and message.text != '-' and message.text != 'мизер'):
        bot.register_next_step_handler(message, bidding)
    else:
        bot.send_message(message.from_user.id, 'coooool')


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


bot.polling()
