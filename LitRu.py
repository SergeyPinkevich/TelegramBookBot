import re
import config
import requests
import Book
from bs4 import BeautifulSoup

URL = config.LitRu_URL


def get_html(url):
    response = requests.get(url)
    return response.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="book")
    result = ""

    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        result = columns[0].text + ' ' + columns[2].text
        if check_is_book(result):
            create_book(result)
    return result


def check_is_book(string):
    first_word = re.findall(r'^\w+', string)
    if first_word == '-':
        return False
    else:
        return True


def create_book(string):
    author = re.split(' - ', string)[0]
    print(author)


def main(query):
    parse(get_html(URL + query))