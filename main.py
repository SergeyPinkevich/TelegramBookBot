# coding: utf8

import telebot
import config
import LitRu

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['search'])
def handle_command(message):
    bot.send_message(config.chat_id, "Пожалуйста, введите название книги или имя автора")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    query = str(message.text.replace(' ', '+'))
    launch_parsing(query)


def launch_parsing(query):
    LitRu.main(query)


if __name__ == '__main__':
     bot.polling(none_stop=True)