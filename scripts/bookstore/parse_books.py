
import os
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.books_sh import Shops

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows; Windows NT 6.1;; en-US Trident/6.0)"}


def get_url():
    for count in range(1, 51):

        url = f"https://books.toscrape.com/catalogue/page-{count}.html"

        response = requests.get(url, timeout=(10, 50))
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all(
            "li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for i in data:
            card_url = "https://books.toscrape.com/catalogue/" + \
                i.find("a").get("href").lstrip("../")
            yield card_url


def get_info():
    for item_card in get_url():

        response = requests.get(item_card, headers=headers)
        response.encoding = 'utf-8'
        sleep(0.3)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("div", class_="col-sm-6 product_main")
        data_table = soup.find("table", class_="table table-striped")

        name = data.find("h1").text
        price = data.find("p", class_="price_color").text.replace("£", "")
        availability_in = data.find(
            "p", class_="instock availability").text.strip()

        rating_t = data.find("p", class_="star-rating")
        rating = rating_t.get("class")[1]

        data_genre = soup.find("ul", class_="breadcrumb")
        genre = data_genre.find_all("li")[2].text.strip()

        data_rows = []
        rows = data_table.find_all('tr')
        rows_cut = rows[:-2]
        for row in rows_cut:
            th = row.find('th')
            td = row.find('td')
            if th and td:
                data_rows.append(
                    (th.text.strip(), td.text.strip().replace('£', '')))

        table_data = dict(data_rows)

        yield {
            'title': name,
            'rating': rating,
            'genre': genre,
            **table_data
        }


print("true")
