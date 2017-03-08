# -*- coding: utf-8 -*-

import requests

from .. import settings

API_URL = 'https://lihkg.com/api_v1_1/'


def get_hot(type_='now'):
    """
    Get Hottest Threads
    """
    if type_ not in ['now', 'daily', 'weekly']:
        raise ValueError('\'type\' must be \'now\', \'daily\', \'weekly\'.')
    response = requests.get(
        url=API_URL + 'thread/hot',
        params={'type': str(type_)},
        headers=settings.HEADERS,
        timeout=settings.TIMEOUT
    )
    return response


def get_latest(page=1, count=30):
    """
    Get Latest Threads
    """
    response = requests.get(
        url=API_URL + 'thread/latest',
        params={'page': str(page), 'count': str(count)},
        headers=settings.HEADERS,
        timeout=settings.TIMEOUT
    )
    return response


def get_news(page=1, count=30):
    """
    Get New Threads
    """
    response = requests.get(
        url=API_URL + 'thread/news',
        params={'page': str(page), 'count': str(count)},
        headers=settings.HEADERS,
        timeout=settings.TIMEOUT
    )
    return response


def get_category(cat_id=1, page=1, count=30):
    response = requests.get(
        url=API_URL + 'thread/category',
        params={'cat_id': str(cat_id), 'page': str(page), 'count': str(count)},
        headers=settings.HEADERS,
        timeout=settings.TIMEOUT
    )
    return response


def get_channel(channel_id=1, page=1, count=30, type_='now'):
    if str(channel_id) == '2':
        response = get_hot(type_=type_)
    elif str(channel_id) == '3':
        response = get_news(page=page, count=count)
    else:
        response = get_category(cat_id=channel_id, page=page, count=count)
    return response


def get_thread(thread_id=1, page=1):
    response = requests.get(
        url=API_URL + 'thread/' + str(thread_id) + '/page/' + str(page),
        headers=settings.HEADERS,
        timeout=settings.TIMEOUT
    )
    return response


def search(query, page=1, count=30):
    response = requests.get(
        url=API_URL + 'thread/search',
        params={'q': str(query), 'page': page, 'count': count},
        headers=settings.HEADERS,
        timeout=settings.TIMEOUT
    )
    return response

