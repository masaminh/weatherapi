"""weathernewsの予報を取得する."""
import datetime
import re
from urllib.parse import urljoin

import requests
from aws_xray_sdk.core import xray_recorder
from bs4 import BeautifulSoup

import citycode


@xray_recorder.capture('weathernews.get_hourly')
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
    soup = BeautifulSoup(response.content, 'lxml')

    days = soup.find_all('div', class_='weather-day')
    for day in days:
        date_str = day.find('div', class_='weather-day__day').find('p').text
        m = re.fullmatch(
            r'(?P<month>\d{1,2})月(?P<day>\d{1,2})日（.）', date_str)
        date_month = int(m.group('month'))
        date_day = int(m.group('day'))
        date = datetime.datetime(today.year, date_month, date_day)

        if date.date() < today:
            date = datetime.datetime(today.year + 1, date_month, date_day)

        items = day.find_all('div', class_='weather-day__item')
        hourly_weahter = (
            _get_hourly_weather(url, date, item) for item in items)
        hourly_weathers.extend(hourly_weahter)

    return hourly_weathers


def _get_hourly_weather(baseurl, date, item):
    result = dict()

    time_str = item.find('p', class_='weather-day__time').text
    hour = datetime.timedelta(seconds=int(time_str[:2]) * 3600)
    result['time'] = date + hour

    image = item.find('p', class_='weather-day__icon').find('img')
    weather_icon = image.get('data-original')
    if weather_icon is None:
        weather_icon = image['src']
    result['weather_icon'] = urljoin(baseurl, weather_icon)

    temperature = item.find('p', class_='weather-day__t').text
    result['temperature'] = int(temperature.replace('℃', ''))

    precipitation = item.find('p', class_='weather-day__r').text
    result['precipitation'] = float(precipitation.replace('mm/h', ''))

    return result
