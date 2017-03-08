# -*- coding: utf-8 -*-

from datetime import datetime

from ..utils.change_type import change_type


# Thread Topic
class Topic(object):
    def __init__(self, data=None):
        if isinstance(data, dict):
            self._data = data
        elif data is None:
            self._data = dict()
        else:
            raise TypeError('data must be a \'dict\' object.')
    
    def __repr__(self):
        print_text = '<Topic {:} - {:}>'
        print_text = print_text.format(self.id, self.title)
        return print_text
    
    @property
    def id(self):
        return self._data.get('thread_id')
    
    @property
    def title(self):
        return self._data.get('title')
    
    @property
    def category(self):
        return self._data.get('category').get('name')
    
    @property
    def create_time(self):
        t = self._data.get('create_time')
        t = change_type(t, func=datetime.fromtimestamp)
        return t
    
    @property
    def last_reply_time(self):
        t = self._data.get('last_reply_time')
        t = change_type(t, func=datetime.fromtimestamp)
        return t
    
    @property
    def like_count(self):
        n = self._data.get('like_count')
        n = change_type(n, func=int)
        return n
    
    @property
    def dislike_count(self):
        n = self._data.get('dislike_count')
        n = change_type(n, func=int)
        return n
    
    @property
    def no_of_reply(self):
        n = self._data.get('no_of_reply')
        n = change_type(n, func=int)
        return n
    
    @property
    def total_page(self):
        n = self._data.get('total_page')
        n = change_type(n, func=int)
        return n

