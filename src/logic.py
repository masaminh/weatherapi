"""WeatherAPIのロジック."""
import copy
from concurrent.futures import ThreadPoolExecutor

from aws_xray_sdk.core import xray_recorder

import citycode
import tenkijp
import weathernews


@xray_recorder.capture('logic.get_hourly')
def get_hourly(code):
    """1時間毎天気予報を取得する.

    Arguments:
        code {str} -- 市町村コード

    Returns:
        list -- 1時間毎の天気情報.

    """
    with ThreadPoolExecutor() as executor:
        tenkijp_future = executor.submit(_tenkijp_hourly_task, code)
        weathernews_future = executor.submit(_weathernews_hourly_task, code)

        tenkijp_weathers = {x['time']: x for x in tenkijp_future.result()}
        weathernews_weathers = {
            x['time']: x for x in weathernews_future.result()}

    tenkijp_keyset = set(tenkijp_weathers.keys())
    weathernews_keyset = set(weathernews_weathers.keys())

    available_times = tenkijp_keyset.intersection(weathernews_keyset)
    available_times_list = sorted(list(available_times))

    result = {
        'cityname': citycode.get_cityname(code),
        'weathers': [
            {
                'time':  time.isoformat(timespec='minutes'),
                'tenkijp': _get_weather_dict(tenkijp_weathers[time]),
                'weathernews': _get_weather_dict(weathernews_weathers[time])
            }
            for time in available_times_list
        ]
    }

    return result


def _get_weather_dict(weather):
    weather_dict = copy.copy(weather)
    del weather_dict['time']
    return weather_dict


def _tenkijp_hourly_task(x):
    return tenkijp.get_hourly(x)


def _weathernews_hourly_task(x):
    return weathernews.get_hourly(x)
