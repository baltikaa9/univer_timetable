import os
from datetime import datetime

import telebot
from telebot import types
from dotenv import load_dotenv

from timetables import timetable_img, timetable_text

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id,
                     '<b>Команды:</b>\n'
                     '/rasp_today - Расписание на сегодня\n'
                     '/rasp - Расписание на любой день',
                     parse_mode='html')


@bot.message_handler(commands=['rasp_today'])
def rasp_today(message: types.Message):
    """Timetable today"""
    if datetime.now().weekday() == 6:
        bot.send_message(message.chat.id, timetable_img[datetime.now().weekday()])
    else:
        bot.send_message(message.chat.id, '<b>Расписание на сегодня.</b>', parse_mode='html')
        with open(timetable_img[datetime.now().weekday()], 'rb') as file:
            bot.send_photo(message.chat.id, file.read())


@bot.message_handler(commands=['rasp'])
def rasp(message: types.Message):
    """Timetable for any day"""
    markup = types.InlineKeyboardMarkup()
    btn_mon = types.InlineKeyboardButton(text='Пн', callback_data='0')
    btn_tue = types.InlineKeyboardButton(text='Вт', callback_data='1')
    btn_wed = types.InlineKeyboardButton(text='Ср', callback_data='2')
    btn_thu = types.InlineKeyboardButton(text='Чт', callback_data='3')
    btn_fri = types.InlineKeyboardButton(text='Пт', callback_data='4')
    btn_sat = types.InlineKeyboardButton(text='Сб', callback_data='5')
    markup.add(btn_mon, btn_tue, btn_wed, btn_thu, btn_fri, btn_sat)
    bot.send_message(message.chat.id, 'Выберите день недели.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.send_message(call.message.chat.id, timetable_text[int(call.data)], parse_mode='html')
    with open(timetable_img[int(call.data)], 'rb') as file:
        bot.send_photo(call.message.chat.id, file.read())
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['text'], chat_types=['private'])
def text(message: types.Message):
    match message.text.lower():
        case 'пн' | 'понедельник':
            bot.send_message(message.chat.id, timetable_text[0], parse_mode='html')
            with open(timetable_img[0], 'rb') as file:
                bot.send_photo(message.chat.id, file.read())
        case 'вт' | 'вторник':
            bot.send_message(message.chat.id, timetable_text[1], parse_mode='html')
            with open(timetable_img[1], 'rb') as file:
                bot.send_photo(message.chat.id, file.read())
        case 'ср' | 'среда':
            bot.send_message(message.chat.id, timetable_text[2], parse_mode='html')
            with open(timetable_img[2], 'rb') as file:
                bot.send_photo(message.chat.id, file.read())
        case 'чт' | 'четверг':
            bot.send_message(message.chat.id, timetable_text[3], parse_mode='html')
            with open(timetable_img[3], 'rb') as file:
                bot.send_photo(message.chat.id, file.read())
        case 'пт' | 'пятница':
            bot.send_message(message.chat.id, timetable_text[4], parse_mode='html')
            with open(timetable_img[4], 'rb') as file:
                bot.send_photo(message.chat.id, file.read())
        case 'сб' | 'суббота':
            bot.send_message(message.chat.id, timetable_text[5], parse_mode='html')
            with open(timetable_img[5], 'rb') as file:
                bot.send_photo(message.chat.id, file.read())


if __name__ == '__main__':
    bot.infinity_polling()
