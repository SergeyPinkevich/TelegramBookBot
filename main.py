# coding: utf8

import telebot
import config
import LitRu
import re

bot = telebot.TeleBot(config.token)
books = []


@bot.message_handler(commands=['start'])
def handle_command(message):
    bot.send_message(config.chat_id, "Чтобы начать, просто введите название книги или автора, и я начну поиск :)")


@bot.message_handler(regexp='/download_\d+')
def handle_command(message):
    download_link = LitRu.get_book(message.text)
    bot.send_message(config.chat_id, download_link)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(config.chat_id, 'Выполняется поиск...')
    query = str(message.text.replace(' ', '+'))
    books = launch_parsing(query)
    bot.send_message(config.chat_id, print_books(books))


def launch_parsing(query):
    return LitRu.main(query)
    # Flibusta.main(query)


def print_books(books):
    result = ""
    if len(books) != 0:
        result = "Найдено результатов: " + str(len(books)) + '\n\n'
        for book in books:
            temp_link = re.split(r'\?p=', book.link)[1]
            result += ('Автор: ' + book.author + '\n' + 'Название: ' + book.title + '\n' + 'Скачать FB2: /download_'
                       + temp_link + '\n\n')
    else:
        result = "К сожалению, поиск не дал результатов. Попробуйте изменить поисковый запрос"
    return result


if __name__ == '__main__':
    bot.polling(none_stop=True)