"""tenki.jpの予報を取得する."""
from datetime import datetime
from datetime import timedelta

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
    hourly_weathers = dict()

    url = citycode.get_tenkijp_urls(code).hourly
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    tables = soup.select('table.forecast-point-1h')

    for table in tables:
        p_str = table.select_one('tr.head p').text

        # '今日 2019年08月16日(金)[仏滅]'形式なので、以下で日付部分を切り出す
        datestr = p_str.split()[1][:11]
        date = datetime.strptime(datestr, '%Y年%m月%d日').date()

        weathers = table.select('tr.weather td')
        for i, weather in enumerate(weathers):
            time = _get_time(date, i)
            weather_text = weather.p.text
            weather_icon = weather.img['src']
            hourly_weathers[time] = {
                'time': time, 'weather': weather_text,
                'weather_icon': weather_icon}

        temperatures = [p.text for p in table.select('tr.temperature span')]
        for i, temperature in enumerate(temperatures):
            time = _get_time(date, i)
            hourly_weathers[time]['temperature'] = float(temperature)

        precipitations = [
            p.text for p in table.select('tr.precipitation span')]
        for i, precipitation in enumerate(precipitations):
            time = _get_time(date, i)
            hourly_weathers[time]['precipitation'] = float(precipitation)

    result = list(hourly_weathers.values())
    result.sort(key=lambda x: x['time'])

    return result


def _get_time(date, index):
    delta = timedelta(seconds=(index+1)*3600)
    time = datetime(date.year, date.month, date.day)
    time += delta
    return time
