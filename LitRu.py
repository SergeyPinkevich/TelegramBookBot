# coding: utf8

import config
import urllib.request
from bs4 import BeautifulSoup

URL = config.LitRu_URL


def get_html(url):
    url = str(url)
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")


def main(query):
    parse(get_html(URL + query))


if __name__ == '__main__':
    main()