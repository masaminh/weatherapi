"""市町村コード関係の関数群."""

from collections import namedtuple

Urls = namedtuple('Urls', 'hourly')


def get_cityname(code):
    """市町村名を取得する.

    Arguments:
        code {str} -- 市町村コード

    Returns:
        str -- 市町村名

    """
    if code != '01101':
        return None

    return "札幌市中央区"


def get_tenkijp_urls(code):
    """tenki.jpのurlを取得する.

    Arguments:
        code {str} -- 市町村コード

    Returns:
        Urls -- tenki.jpのURL情報

    """
    if code != '01101':
        return None

    urls = Urls(
        hourly='https://tenki.jp/forecast/1/2/1400/1101/1hour.html')
    return urls


def get_weathernews_urls(code):
    """weathernewsのurlを取得する.

    Arguments:
        code {str} -- 市町村コード

    Returns:
        Urls -- weathernewsのURL情報

    """
    if code != '01101':
        return None

    urls = Urls(
        hourly='https://weathernews.jp/onebox/tenki/hokkaido/01101/')
    return urls
