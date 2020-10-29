import requests
import json
from bs4 import BeautifulSoup


def get_data(team, person, date=None):
    try:
        game_url = get_game_url(team, date)
        record = get_record(person, game_url)
    except Exception as e:
        return e
    return record


def get_record(person, url):
    soup = create_soup(url)
    records = soup.select(
        '.bb-liveText__content:contains("{}")'.format(person))
    if not records:
        raise Exception("出場していない選手です")
    return list(map(lambda x: list(x.stripped_strings), records))


def get_game_url(team, date=None):
    # ?date=2020-XX-XX で日付を指定
    # dateを省略した場合、当日の日付にハンドリングされる
    BASE_URL = "https://baseball.yahoo.co.jp/npb/schedule"
    top_url = "{}?date={}".format(BASE_URL, date) if date else BASE_URL

    soup = create_soup(top_url)
    battle_cards = soup.select('.bb-score__item:contains("{}")'.format(team))
    if not battle_cards:
        raise Exception("球団か日付の指定が間違っています")
    battle_card = battle_cards[0]
    return battle_card.find('a')["href"].replace("index", "text")


def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, 'html.parser')
