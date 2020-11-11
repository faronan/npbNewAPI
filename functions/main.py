import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

from result import Record, Result, Content
from result_repository import ResultReposiroty


def get_data(request):
    try:
        date = get_param_from_request(request, "date")
        team = get_param_from_request(request, "team")
        person = get_param_from_request(request, "person")

        records = get_records_if_not_find_repository(date, team, person)
    except Exception as e:
        return json.dumps({"error": e.args}, ensure_ascii=False)

    return json.dumps({"records": records}, ensure_ascii=False)


def get_records_if_not_find_repository(date, team, person):
    result_repository = ResultReposiroty()
    docs = result_repository.find(date, team)

    dt = datetime.strptime(date, '%Y-%m-%d')
    today = datetime.now(timezone(timedelta(hours=+9), 'JST')).date()
    is_today = (dt.year == today.year & dt.month ==
                today.month & dt.day == today.day)
    # 日付と球団でキャッシュしたデータがある場合はそちらを参照、ただし当日なら毎回スクレイピングして更新する
    if not is_today & bool(docs):
        is_no_game = docs[0].to_dict()[u'content'][u'is_no_game']
        if is_no_game:
            raise Exception("球団か日付の指定が間違っています")

        result_texts_filter_by_person = [doc.to_dict()[u'content'][u'record'][u'texts']
                                         for doc in docs if doc.to_dict()[u'content'][u'record'][u'person'] == person]
        # 対象の選手のデータもある場合
        if result_texts_filter_by_person:
            return list(sorted(result_texts_filter_by_person[0].values()))

    game_url = scraping_game_url(team, date)
    record_texts = scraping_record_texts(person, game_url)

    record = Record(person=person, texts=record_texts)
    content = Content(is_no_game=False, record=record)
    result = Result(date=date, team=team, content=content)
    if is_today & bool(docs):
        result_repository.update(result)
    else:
        result_repository.save(result)

    return record_texts


def get_param_from_request(request, param):
    if request.args and param in request.args:
        return request.args.get(param)
    raise Exception("パラメータが間違っています")


def scraping_record_texts(person, url):
    soup = create_soup(url)
    scraping_data = soup.select(
        '.bb-liveText__content:contains("{}")'.format(person))
    if scraping_data:
        texts = list(map(lambda x: " ".join(
            list(x.stripped_strings)[1:]), scraping_data))

        return texts
    raise Exception("出場していない選手です")


def scraping_game_url(team, date):
    BASE_URL = "https://baseball.yahoo.co.jp/npb/schedule"
    top_url = "{}?date={}".format(BASE_URL, date) if date else BASE_URL

    soup = create_soup(top_url)
    battle_cards = soup.select('.bb-score__item:contains("{}")'.format(team))
    if battle_cards:
        battle_card = battle_cards[0]
        return battle_card.find('a')["href"].replace("index", "text")
    result_repository = ResultReposiroty()
    content = Content(is_no_game=True, record=Record(person="", texts=[""]))
    result = Result(date=date, team=team, content=content)
    result_repository.save(result)

    raise Exception("球団か日付の指定が間違っています")


def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, 'html.parser')
