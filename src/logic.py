"""WeatherAPIのロジック."""
import copy

import tenkijp
import weathernews


def get_hourly(code):
    """1時間毎天気予報を取得する.

    Arguments:
        code {str} -- 市町村コード

    Returns:
        list -- 1時間毎の天気情報.

    """
    tenkijp_weathers = {x['time']: x for x in tenkijp.get_hourly(code)}
    weathernews_weathers = {x['time']: x for x in weathernews.get_hourly(code)}
    tenkijp_keyset = set(tenkijp_weathers.keys())
    weathernews_keyset = set(weathernews_weathers.keys())

    available_times = tenkijp_keyset.intersection(weathernews_keyset)
    available_times_list = sorted(list(available_times))

    result = [
        {
            'time':  time.isoformat(timespec='minutes'),
            'tenkijp': _get_weather_dict(tenkijp_weathers[time]),
            'weathernews': _get_weather_dict(weathernews_weathers[time])
        }
        for time in available_times_list
    ]

    return result


def _get_weather_dict(weather):
    weather_dict = copy.copy(weather)
    del weather_dict['time']
    return weather_dict
