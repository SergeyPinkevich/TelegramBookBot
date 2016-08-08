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
    books = launch_parsing(query)
    bot.send_message(config.chat_id, print_books(books))


def launch_parsing(query):
    return LitRu.main(query)
    # Flibusta.main(query)


def print_books(books):
    result = "Найдено результатов: " + str(len(books)) + '\n\n'
    for book in books:
        result += ('Автор: ' + book.author + '\n' + 'Название: ' + book.title + '\n' + 'Скачать FB2: ' + book.link + '\n\n')
    return result

if __name__ == '__main__':
    launch_parsing("Гарри+Поттер")
    # bot.polling(none_stop=True)