"""weathernewsの予報を取得する."""
import datetime
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import citycode


def get_hourly(code):
    """1時間毎天気予報を取得する.

    Arguments:
        code {str} -- 市町村コード

    Returns:
        list -- 1時間毎の天気情報.

    """
    today = datetime.date.today()
    hourly_weathers = []

    url = citycode.get_weathernews_urls(code).hourly
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')

    days = soup.select('div.weather-day')
    for day in days:
        date_str = day.select_one('div.weather-day__day p').text
        m = re.fullmatch(
            r'(?P<month>\d{1,2})月(?P<day>\d{1,2})日（.）', date_str)
        date_month = int(m.group('month'))
        date_day = int(m.group('day'))
        date = datetime.datetime(today.year, date_month, date_day)

        if date.date() < today:
            date = datetime.datetime(today.year + 1, date_month, date_day)

        items = day.select('div.weather-day__item')
        hourly_weahter = (
            _get_hourly_weather(url, date, item) for item in items)
        hourly_weathers.extend(hourly_weahter)

    return hourly_weathers


def _get_hourly_weather(baseurl, date, item):
    result = dict()

    time_str = item.select_one('p.weather-day__time').text
    hour = datetime.timedelta(seconds=int(time_str[:2]) * 3600)
    result['time'] = date + hour

    image = item.select_one('p.weather-day__icon img')
    weather_icon = image.get('data-original')
    if weather_icon is None:
        weather_icon = image['src']
    result['weather_icon'] = urljoin(baseurl, weather_icon)

    temperature = item.select_one('p.weather-day__t').text
    result['temperature'] = int(temperature.replace('℃', ''))

    precipitation = item.select_one('p.weather-day__r').text
    result['precipitation'] = float(precipitation.replace('mm/h', ''))

    return result
