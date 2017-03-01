# -*- coding: utf-8 -*-

import requests

TIMEOUT = (10, 60)

API_URL = 'https://lihkg.com/api_v1_1/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.87 Safari/537.36',
    'from': 'baan3gung1.lihkg'
}

CHANNELS = [
    {'name': '吹水台', 'id': 1},
    {'name': '熱門', 'id': 2},
    {'name': '最新', 'id': 3},
    {'name': '手機台', 'id': 4},
    {'name': '時事台', 'id': 5},
    {'name': '體育台', 'id': 6},
    {'name': '娛樂台', 'id': 7},
    {'name': '動漫台', 'id': 8},
    {'name': 'Apps台', 'id': 9},
    {'name': '遊戲台', 'id': 10},
    {'name': '影視台', 'id': 11},
    {'name': '講故台', 'id': 12},
    {'name': '潮流台', 'id': 13},
    {'name': '上班台', 'id': 14},
    {'name': '財經台', 'id': 15},
    {'name': '飲食台', 'id': 16},
    {'name': '旅遊台', 'id': 17},
    {'name': '學術台', 'id': 18},
    {'name': '校園台', 'id': 19},
    {'name': '汽車台', 'id': 20},
    {'name': '音樂台', 'id': 21},
    {'name': '硬件台', 'id': 22},
    {'name': '攝影台', 'id': 23},
    {'name': '玩具台', 'id': 24},
    {'name': '寵物台', 'id': 25},
    {'name': '軟件台', 'id': 26},
    {'name': '活動台', 'id': 27},
    {'name': '站務台', 'id': 28},
    {'name': '成人台', 'id': 29},
    {'name': '感情台', 'id': 30},
    {'name': '創意台', 'id': 31},
    {'name': '黑洞', 'id': 32},
    {'name': '政事台', 'id': 33},
    {'name': '直播台', 'id': 34},
    {'name': '電訊台', 'id': 35}
]


def get_hot(type_='now'):
    """
    Get Hottest Threads
    """
    if type_ not in ['now', 'daily', 'weekly']:
        raise ValueError('\'type\' must be \'now\', \'daily\', \'weekly\'.')
    response = requests.get(
        url=API_URL + 'thread/hot',
        params={'type': str(type_)},
        headers=HEADERS,
        timeout=TIMEOUT
    )
    return response


def get_latest(page=1, count=30):
    """
    Get Latest Threads
    """
    response = requests.get(
        url=API_URL + 'thread/latest',
        params={'page': str(page), 'count': str(count)},
        headers=HEADERS,
        timeout=TIMEOUT
    )
    return response


def get_news(page=1, count=30):
    """
    Get New Threads
    """
    response = requests.get(
        url=API_URL + 'thread/news',
        params={'page': str(page), 'count': str(count)},
        headers=HEADERS,
        timeout=TIMEOUT
    )
    return response


def get_category(cat_id=1, page=1, count=30):
    response = requests.get(
        url=API_URL + 'thread/category',
        params={'cat_id': str(cat_id), 'page': str(page), 'count': str(count)},
        headers=HEADERS,
        timeout=TIMEOUT
    )
    return response


def get_channel(channel_id=1, page=1, count=30, type_='now'):
    if str(channel_id) == '2':
        return get_hot(type_=type_)
    elif str(channel_id) == '3':
        return get_news(page=page, count=count)
    else:
        return get_category(cat_id=channel_id, page=page, count=count)


def get_thread(thread_id=0, page=1):
    response = requests.get(
        url=API_URL + 'thread/' + str(thread_id) + '/page/' + str(page),
        headers=HEADERS
    )
    return response


def search(query, page=1, count=30):
    response = requests.get(
        url=API_URL + 'thread/search',
        params={'q': query, 'page': page, 'count': count},
        headers=HEADERS
    )
    return response

