import data
from data import *
import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

states = {}

token = 'не скажу'
bot = telebot.TeleBot(token)

about_text = '''
https://github.com/FreddyFazberUrUr/TG-botik.git
'''

help_text = """
Привет! Я - бот~квест. Вот что я умею:
/start или /go - начало приключения
/resume - продолжение приключения
/help - помощь
/about - информация о боте
"""


@bot.message_handler(commands=['about'])
def bot_about(msg):
    bot.send_message(msg.from_user.id, about_text)


@bot.message_handler(commands=['resume'])
def resume(msg):
    if msg.from_user.id in states:
        ask_question(msg)

    else:
        bot.send_message(msg.from_user.id,
                         'Вы еще не начали проходить викторину. Чтобы начать введите команду /start')


@bot.message_handler(commands=['help'])
def help_user(user_id):
    bot.send_message(user_id, help_text)


@bot.message_handler(commands=['start', 'go'])
def start_polling(msg):
    bot.send_message(msg.from_user.id, 'Привет! Введи /help если тебе нужна помощь в управлении ботом. Удачи!')
    states[msg.from_user.id] = {}
    states[msg.from_user.id]['location'] = 'start'
    ask_question(msg)


def ask_question(msg):
    user_id = msg.from_user.id

    with open('game_data.json', 'r', encoding='utf-8') as f_g:
        file_g = json.load(f_g)
        current_state = states[user_id]['location']

        if current_state in file_g:
            if file_g[states[user_id]['location']]['options'] == {}:
                data.save_data(states)
                bot.send_message(user_id, file_g[current_state]['description'])

            else:
                keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
                key1 = KeyboardButton("1")
                key2 = KeyboardButton("2")
                key3 = KeyboardButton("3")
                keyboard.add(key1, key2, key3)
                bot.send_message(user_id, file_g[current_state]['description'], reply_markup=keyboard)

            bot.register_next_step_handler(msg, handle_answer)

        else:
            bot.send_message(user_id, 'У нас технические шоколадки, но мы скоро починим')


def handle_answer(msg):
    user_id = msg.from_user.id

    with open('game_data.json', 'r', encoding='utf-8') as f_g:
        file_g = json.load(f_g)

        if msg.text == '/help':
            help_user(user_id)

        elif msg.text == '/about':
            bot_about(msg)

        elif msg.text == '/start':
            start_polling(msg)

        elif msg.text == '/resume':
            resume(msg)

        elif file_g[states[user_id]['location']]['options'] == {}:
            bot.send_message(user_id, 'Чтобы начать игру заново нажми сюда --> /start\n'
                                      'Если нужна помощь с управлением нажми сюда --> /help')
            bot.register_next_step_handler(msg, handle_answer)
            return

        elif msg.text in file_g[states[user_id]['location']]['options']:
            states[user_id]['location'] = file_g[states[user_id]['location']]['options'][msg.text]
            ask_question(msg)

        else:
            bot.send_message(user_id, 'Чота я не понял. Давай по новой {0.first_name}'.format(msg.from_user,
                                                                                              bot.get_me()))
            ask_question(msg)


if __name__ == '__main__':
    bot.infinity_polling()
