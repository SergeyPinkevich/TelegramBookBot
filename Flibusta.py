import config
import requests
from bs4 import BeautifulSoup

URL = config.Flibusta_URL


def get_html(url):
    response = requests.get(url)
    return response.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    block = soup.find('div', {"id": "main"})

    for link in block.find_all("li")[1:]:
        print(link)


def main(query):
    parse(get_html(URL + query))