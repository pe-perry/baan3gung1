# -*- coding: utf-8 -*-

from .. import lihkg
from .Post import Post
from ..lihkg.get_lihkg_response import get_lihkg_response
from ..utils.change_type import change_type
from ..utils.print_func import print_separator


class ThreadPage(object):
    def __init__(self, data=None):
        if isinstance(data, dict):
            self._data = data
        elif data is None:
            self._data = dict()
        else:
            raise TypeError('data must be a \'dict\' object.')
    
    def __repr__(self):
        print_text = '<Thread {:} - Page {:} ({:} Posts)>'
        print_text = print_text.format(
            self.thread_id,
            self.page,
            len(self.posts)
        )
        return print_text
    
    @property
    def thread_id(self):
        return self._data.get('thread_id')
    
    @property
    def title(self):
        return self._data.get('title')
    
    @property
    def page(self):
        pg = self._data.get('page')
        pg = change_type(pg, int)
        return pg
    
    @property
    def posts(self):
        return [Post(x) for x in self._data.get('item_data', dict())]
    
    @staticmethod
    def read_thread_page(thread_id, page=1):
        resp = lihkg.requests.get_thread(thread_id=thread_id, page=page)
        response = get_lihkg_response(resp)
        return ThreadPage(data=response)
    
    def refresh(self):
        if self.thread_id is not None and self.page is not None:
            resp = lihkg.requests.get_thread(thread_id=self.thread_id, page=self.page)
            response = get_lihkg_response(resp)
            self.__init__(data=response)
        else:
            pass
    
    def show(self, quote_depth=None):
        if self.page is None:
            print_separator('Captain, I can\'t see shit!')
        else:
            print_separator('Page {:2}.'.format(self.page))
            start_index = (self.page - 1) * 25
            for i, p in enumerate(self.posts):
                p.show(quote_depth=quote_depth, post_index=start_index + i)

