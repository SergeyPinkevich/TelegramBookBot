import re
import config
import requests
from Book import Book
from bs4 import BeautifulSoup

URL = config.LitRu_URL


def get_html(url):
    response = requests.get(url)
    return response.text


def find_link(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    for td in table.find_all("td"):
        link = td.find("a")['href']
    return link


def remove_empty_book(books):
    for book in books:
        if book.link == "http://litru.ru/?p=397461":
            books.remove(books[0])


def get_book(link):
    url = "http://litru.ru/?p=" + re.split('download_', link)[1]
    download_link = find_link(get_html(url))
    return download_link


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="book")

    books = []

    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        author_and_title = columns[0].text
        rate = columns[2].text

        if check_book_has_author(author_and_title) is True:
            link = "".join(re.findall(r'http://litru\.ru/\?p=\w+', str(columns[0])))
            book = create_book(author_and_title, link, rate)
            books.append(book)

    remove_empty_book(books)
    books.sort(key=lambda b: b.rate)
    return books


def check_book_has_author(string):
    if string[0] is ' ':
        return False
    else:
        return True


def create_book(name, link, rate):
    book = Book()

    author = re.split(' - ', name)[0]
    book.set_author(author)

    title = re.split(' - ', name)[1]
    book.set_title(title)

    book.set_link(str(link))

    book.set_rate(int(rate))

    return book


def main(query):
    return parse(get_html(URL + query))
