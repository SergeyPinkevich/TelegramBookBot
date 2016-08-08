import re
import config
import requests
from Book import Book
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
        author_and_title = columns[0].text
        rate = columns[2].text

        books = []
        if check_book_has_author(author_and_title) is True:
            book = create_book(author_and_title, rate)
            books.append(book)

        books.sort(key=lambda b: b.rate)
        for b in books:
            print(b.author + '/' + b.title + '/' + str(b.rate))
        # print_book(books)
    return result


def check_book_has_author(string):
    if string[0] is ' ':
        return False
    else:
        return True


def create_book(name, rate):
    book = Book()

    author = re.split(' - ', name)[0]
    book.set_author(author)

    title = re.split(' - ', name)[1]
    book.set_title(title)

    book.set_rate(int(rate))

    return book


def print_book(books):
    for book in books:
        print(book.author + '/' + book.title + '/' + str(book.rate))


def main(query):
    parse(get_html(URL + query))