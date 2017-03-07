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
    {'id':  1, 'full_width_name': '吹水台', 'name': '吹水台'},
    {'id':  2, 'full_width_name': '熱門', 'name': '熱門', },
    {'id':  3, 'full_width_name': '最新', 'name': '最新', },
    {'id':  4, 'full_width_name': '手機台', 'name': '手機台', },
    {'id':  5, 'full_width_name': '時事台', 'name': '時事台', },
    {'id':  6, 'full_width_name': '體育台', 'name': '體育台', },
    {'id':  7, 'full_width_name': '娛樂台', 'name': '娛樂台', },
    {'id':  8, 'full_width_name': '動漫台', 'name': '動漫台', },
    {'id':  9, 'full_width_name': 'Ａｐｐｓ台', 'name': 'Apps台', },
    {'id': 10, 'full_width_name': '遊戲台', 'name': '遊戲台', },
    {'id': 11, 'full_width_name': '影視台', 'name': '影視台', },
    {'id': 12, 'full_width_name': '講故台', 'name': '講故台', },
    {'id': 13, 'full_width_name': '潮流台', 'name': '潮流台', },
    {'id': 14, 'full_width_name': '上班台', 'name': '上班台', },
    {'id': 15, 'full_width_name': '財經台', 'name': '財經台', },
    {'id': 16, 'full_width_name': '飲食台', 'name': '飲食台', },
    {'id': 17, 'full_width_name': '旅遊台', 'name': '旅遊台', },
    {'id': 18, 'full_width_name': '學術台', 'name': '學術台', },
    {'id': 19, 'full_width_name': '校園台', 'name': '校園台', },
    {'id': 20, 'full_width_name': '汽車台', 'name': '汽車台', },
    {'id': 21, 'full_width_name': '音樂台', 'name': '音樂台', },
    {'id': 22, 'full_width_name': '硬件台', 'name': '硬件台', },
    {'id': 23, 'full_width_name': '攝影台', 'name': '攝影台', },
    {'id': 24, 'full_width_name': '玩具台', 'name': '玩具台', },
    {'id': 25, 'full_width_name': '寵物台', 'name': '寵物台', },
    {'id': 26, 'full_width_name': '軟件台', 'name': '軟件台', },
    {'id': 27, 'full_width_name': '活動台', 'name': '活動台', },
    {'id': 28, 'full_width_name': '站務台', 'name': '站務台', },
    {'id': 29, 'full_width_name': '成人台', 'name': '成人台', },
    {'id': 30, 'full_width_name': '感情台', 'name': '感情台', },
    {'id': 31, 'full_width_name': '創意台', 'name': '創意台', },
    {'id': 32, 'full_width_name': '黑洞', 'name': '黑洞', },
    {'id': 33, 'full_width_name': '政事台', 'name': '政事台', },
    {'id': 34, 'full_width_name': '直播台', 'name': '直播台', },
    {'id': 35, 'full_width_name': '電訊台', 'name': '電訊台', }
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

