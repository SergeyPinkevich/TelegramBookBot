# coding: utf8

import requests
import os
import zipfile
import telebot
import config
import LitRu
import re

bot = telebot.TeleBot(config.token)
books = []


@bot.message_handler(commands=['start'])
def handle_command(message):
    bot.send_message(config.chat_id, "Привет, " + message.from_user.first_name +
                     "! Чтобы начать, просто введите название книги или автора, и я начну поиск :)")


@bot.message_handler(regexp='/download_\d+')
def handle_command(message):
    bot.send_message(config.chat_id, 'Скачиваю книгу с внешнего ресурса...')
    download_link = LitRu.get_book(message.text)
    file_name = message.text.split('_')[1]
    download_book(download_link, file_name)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(config.chat_id, 'Выполняю поиск...')
    query = str(message.text.replace(' ', '+'))
    books = launch_parsing(query)
    bot.send_message(config.chat_id, print_books(books))


def download_book(link, file_name):
    archive = file_name + ".zip"
    file_fb2 = file_name + ".fb2"
    file_txt = file_name + ".txt"

    r = requests.get(link)
    with open(archive, "wb") as code:
        code.write(r.content)
    with zipfile.ZipFile(archive, "r") as zip_ref:
        zip_ref.extractall()
        r.close()

    document = open_file(file_fb2)
    if document is None:
        document = open_file(file_txt)

    bot.send_document(config.chat_id, document)
    document.close()

    os.remove(os.getcwd() + "/" + archive)
    remove_file(file_fb2)
    remove_file(file_txt)


def open_file(file_name):
    try:
        document = open(os.getcwd() + "/" + file_name, 'rb')
        return document
    except FileNotFoundError:
        print("There is no such file: " + file_name)


def remove_file(file_name):
    try:
        os.remove(os.getcwd() + "/" + file_name)
    except FileNotFoundError:
        print("There is no such file: " + file_name)


def launch_parsing(query):
    return LitRu.main(query)


def print_books(books):
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
