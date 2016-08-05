# -*- coding: utf-8 -*-

import telebot
import config
import urllib.request
from bs4 import BeautifulSoup


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="book")
    tbody = table.find("tbody")

    for tr in tbody.find_all('tr'):
        print(tr)


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['search'])
def handle_command(message):
    bot.send_message(config.chat_id, "Please, enter the title or author")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    query = message.text
    query.replace(' ', '+')
    print(query)
    parse(get_html(config.URL + query))


if __name__ == '__main__':
     bot.polling(none_stop=True)