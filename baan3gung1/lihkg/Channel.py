# -*- coding: utf-8 -*-

from datetime import datetime

from baan3gung1 import lihkg
from .utils import change_type, get_response


# Thread Topic
class Topic(object):
    def __init__(self, data=dict()):
        if isinstance(data, dict):
            self._data = data
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


# Channel
class Channel(object):
    def __init__(self, data=dict(), print_mode=1):
        if isinstance(data, dict):
            self._data = data
        else:
            raise TypeError('data must be a \'dict\' object.')
        self._print_mode = print_mode
    
    def __repr__(self):
        print_text = '<{:} ({:} Threads>)'
        print_text = print_text.format(self.channel, len(self.topics))
        return print_text
    
    @property
    def print_mode(self):
        return self._print_mode
    
    @print_mode.setter
    def print_mode(self, x):
        if x in [0, 1, 2]:
            self._print_mode = x
        else:
            raise ValueError('Only mode 0, 1, 2 are supported.')
    
    @property
    def category(self):
        return self._data.get('category', {'cat_id': None, 'name': '?'})
    
    @property
    def is_pagination(self):
        return self._data.get('is_pagination', False)
    
    @property
    def topics(self):
        items = self._data.get('items', list())
        return [Topic(thd) for thd in items]
    
    @property
    def id(self):
        return self.category.get('cat_id')
    
    @property
    def channel(self):
        return self.category.get('name').replace('\u3000', '')
    
    @staticmethod
    def get_channel(channel_id=1, page=1, count=30, print_mode=1):
        resp = lihkg.requests.get_channel(channel_id=channel_id, page=page, count=count)
        response = get_response(resp)
        return Channel(data=response, print_mode=print_mode)
    
    @staticmethod
    def search(query, page=1, count=30, print_mode=1):
        resp = lihkg.requests.search(query=query, page=page, count=count)
        response = get_response(resp)
        return Channel(data=response, print_mode=print_mode)
    
    def refresh(self):
        if self.id is not None:
            resp = lihkg.requests.get_channel(channel_id=self.id)
            response = get_response(resp)
            self.__init__(data=response, print_mode=self._print_mode)
        else:
            pass
    
    def show(self):
        topics = self.topics
        print_format_id = '{{0:{:}}}'.format(max(len(x.id) for x in topics))
        print_template = print_format_id + ' - {1:} ({2:})\n'
        if self._print_mode > 0:
            print_template += print_format_id.format('') + '   回覆數: {3:} | 正負皮: {4:}:{5:}\n'
        if self._print_mode > 1:
            print_template += print_format_id.format('') + '   建立時間: {6:} | 最後回覆: {7:}\n'
        if len(topics) > 0:
            for topic in topics:
                print_text = print_template.format(
                    topic.id, topic.title, topic.category,
                    topic.no_of_reply, topic.like_count, topic.dislike_count,
                    topic.create_time, topic.last_reply_time,
                )
                print(print_text)
        else:
            print('-- Nothing was found. --')


__all__ = ['Topic', 'Channel']


def main():
    ch = Channel.get_channel(2)
    ch.show()


if __name__ == "__main__":
    main()

