# coding: utf8

import telebot
import config
import LitRu
import Flibusta

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['search'])
def handle_command(message):
    bot.send_message(config.chat_id, "Пожалуйста, введите название книги или имя автора")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    query = str(message.text.replace(' ', '+'))
    # bot.send_message(config.chat_id, launch_parsing(query))


def launch_parsing(query):
    LitRu.main(query)
    # Flibusta.main(query)


if __name__ == '__main__':
    launch_parsing("Гарри+Поттер")
    # bot.polling(none_stop=True)