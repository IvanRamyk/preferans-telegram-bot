import telebot
import config
from preferans import Preferans

bot = telebot.TeleBot(config.Token)
id_list = []
name_list = []
count_id = 0
age = 0
discard = []


@bot.message_handler(commands=['start'])
def start_messaging(message):
    global count_id
    if count_id < 3:
        bot.send_message(message.from_user.id, 'Поздравляем! Вы в игре!')
        id_list.append(message.from_user.id)
        name_list.append(message.from_user.first_name)
        count_id += 1
        if count_id == 3:
            new_round()
    else:
        bot.send_message(message.from_user.id, 'К сожалению, мест нет(')


@bot.callback_query_handler(func=lambda call: config.state == 'bidding')
def bidding(call):
    if call.from_user.id != id_list[Preferans.current_player()]:
        return
    if Preferans.update_bidding(call.data):
        ask_bidding()
    else:
        result = ''
        if Preferans.game_type() == 'game':
            result = 'Играет ' + name_list[Preferans.declarer()] + '. Ждем пока игрок закажет игру.'
        if Preferans.game_type() == 'misere':
            result = name_list[Preferans.declarer()] + ' играет мизер. Ждем пока игрок понесет карты.'
        if Preferans.game_type() == 'all-pass':
            result = 'Распас. Ход с игрока ' + name_list[Preferans.move()]
        for i in id_list:
            if i != id_list[Preferans.declarer()]:
                bot.send_message(i, result)
        if Preferans.game_type() == 'game' or Preferans.game_type() == 'misere':
            talon = 'Прикуп:\n' + hand_to_string(Preferans.talon())
            for i in id_list:
                bot.send_message(i, talon)
            Preferans.add_talon()
            keyboard = hand_to_keyboard(Preferans.hand_declarer())
            bot.send_message(id_list[Preferans.declarer()], text='Что хотите понести?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: config.state == 'talon')
def discarding(call):
    if call.from_user.id != id_list[Preferans.current_player()]:
        return
    discard.append(call.data)
    if len(discard) == 2:
        Preferans.discard(int(discard[0]), int(discard[1]))
        discard.clear()
        if Preferans.game_type() == 'game':
            bot.send_message(id_list[Preferans.declarer()], text='Закажите игру', reply_markup=game_keyboard())
        else:
            start()


@bot.callback_query_handler(func=lambda call: config.state == 'set_game')
def set_game(call):
    if call.from_user.id != id_list[Preferans.current_player()]:
        return
    Preferans.set_game(int(call.data))
    start()


@bot.callback_query_handler(func=lambda call: config.state == 'game')
def get_card(call):
    if call.from_user.id != id_list[Preferans.current_player()]:
        return
    if Preferans.get_card(int(call.data)):
        if Preferans.cards_in_trick() == 0:
            for i in id_list:
                bot.send_message(i, last_trick())
        start()
    else:
        for i in id_list:
            bot.send_message(i, last_trick())
        # Preferans.score()
        new_round()


def new_round():
    Preferans.set_round()
    bot.send_message(id_list[0], 'Ваши карты:\n' + hand_to_string(Preferans.hand0()))
    bot.send_message(id_list[1], 'Ваши карты:\n' + hand_to_string(Preferans.hand1()))
    bot.send_message(id_list[2], 'Ваши карты:\n' + hand_to_string(Preferans.hand2()))
    ask_bidding()


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


def game_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keys = []
    for i in range(Preferans.dib() - 1, 44):
        if i % 4 == 0:
            key = telebot.types.InlineKeyboardButton(text=hash_to_sting(i), callback_data=str(i))
            keyboard.row(*keys)
            keys.clear()
            keys.append(key)
        else:
            key = telebot.types.InlineKeyboardButton(text=hash_to_sting(i), callback_data=str(i))
            keys.append(key)
    keyboard.row(*keys)
    return keyboard


def suit(card):
    return card % 4


def hand_to_keyboard(hand):
    keys = []
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(len(hand)):
        if i == 0 or suit(hand[i]) == suit(hand[i-1]):
            key = telebot.types.InlineKeyboardButton(text=hash_to_sting(hand[i]), callback_data=str(i))
            keys.append(key)
        else:
            key = telebot.types.InlineKeyboardButton(text=hash_to_sting(hand[i]), callback_data=str(i))
            keyboard.row(*keys)
            keys.clear()
            keys.append(key)
    keyboard.row(*keys)
    return keyboard


def current_trick():
    if len(Preferans.trick()) == 0:
        return players_tricks()
    answer = 'Текущая взятка\n'
    for i in Preferans.trick():
        answer += name_list[i.player] + ' - ' + hash_to_sting(i.card) + '\n'
    return players_tricks() + answer


def players_tricks():
    answer = 'Взятки:\n'
    for i in range(3):
        answer += name_list[i] + ': ' + str(Preferans.player_tricks()[i]) + '\n'
    return answer


def start():
    message = current_trick() + 'Ваш ход'
    bot.send_message(id_list[Preferans.current_player()], text=message,
                     reply_markup=hand_to_keyboard(Preferans.current_hand()))


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


def last_trick():
    answer = ''
    answer += 'Забрал игрок ' + name_list[Preferans.current_player()] + '\n'
    for j in Preferans.last_trick():
        for i in range(3):
            if i == j.player:
                answer += name_list[i] + ': ' + hash_to_sting(j.card) + '\n'
    return answer


bot.polling()
