"""tenki.jpの予報を取得する."""
from datetime import datetime, timedelta

import requests
from aws_xray_sdk.core import xray_recorder
from bs4 import BeautifulSoup

import citycode


@xray_recorder.capture('tenkijp.get_hourly')
def get_hourly(code):
    """1時間毎天気予報を取得する.

    Arguments:
        code {str} -- 市町村コード

    Returns:
        list -- 1時間毎の天気情報.

    """
    hourly_weathers = []

    url = citycode.get_tenkijp_urls(code).hourly
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    tables = soup.select('table.forecast-point-1h')

    for table in tables:
        p_str = table.select_one('tr.head p').text

        # '今日 2019年08月16日(金)[仏滅]'形式なので、以下で日付部分を切り出す
        datestr = p_str.split()[1][:11]
        date = datetime.strptime(datestr, '%Y年%m月%d日').date()

        weathers = table.select('tr.weather td')
        temperatures = [p.text for p in table.select('tr.temperature span')]
        precipitations = [
            p.text for p in table.select('tr.precipitation span')]

        for i in range(24):
            time = _get_time(date, i)
            weather = weathers[i]
            temperature = temperatures[i]
            precipitation = precipitations[i]
            weather_text = weather.p.text
            weather_icon = weather.img['src']
            hourly_weathers.append({
                'time': time, 'weather': weather_text,
                'weather_icon': weather_icon,
                'temperature': float(temperature),
                'precipitation': float(precipitation)
            })

    return hourly_weathers


def _get_time(date, index):
    delta = timedelta(seconds=(index+1)*3600)
    time = datetime(date.year, date.month, date.day)
    time += delta
    return time
