# -*- coding: utf-8 -*-

import itertools
import time
from datetime import datetime

from .. import lihkg
from .. import settings
from .ThreadPage import ThreadPage
from ..lihkg.get_lihkg_response import get_lihkg_response
from ..utils.change_type import change_type
from ..utils.print_func import print_separator


class Thread(object):
    def __init__(self, thread_id, post_per_page=25):
        self.thread_id = str(thread_id)
        self._post_per_page = post_per_page
        self.title = None
        self.category = None
        self.create_time = None
        self.no_of_reply = None
        self.like_count = None
        self.dislike_count = None
        self.total_page = None
        self.status = None
        self._pages = []
    
    def __repr__(self):
        print_text = '<Thread {:} ({:} Replies)>'.format(
            self.thread_id,
            self.no_of_reply
        )
        return print_text
    
    @property
    def id(self):
        return self.thread_id
    
    @property
    def pages(self):
        return self._pages
    
    @property
    def posts(self):
        return list(itertools.chain.from_iterable(page.posts for page in self.pages))
    
    def update_info(self, response):
        no_of_reply = response.get('no_of_reply')
        like_count = response.get('like_count')
        dislike_count = response.get('dislike_count')
        total_page = response.get('total_page')
        status = response.get('status')
        self.no_of_reply = change_type(no_of_reply, int)
        self.like_count = change_type(like_count, int)
        self.dislike_count = change_type(dislike_count, int)
        self.total_page = change_type(total_page, int)
        self.status = status
    
    def get_first_page(self):
        resp = lihkg.requests.get_thread(thread_id=self.thread_id, page=1)
        response = get_lihkg_response(resp=resp)
        self.thread_id = response.get('thread_id')
        self.title = response.get('title')
        self.category = response.get('category')
        self.create_time = change_type(response.get('create_time'), datetime.fromtimestamp)
        self.update_info(response)
        self._pages.append(ThreadPage(response))
    
    def get_next_page(self):
        current_page = len(self._pages)
        resp = lihkg.requests.get_thread(thread_id=self.thread_id, page=current_page + 1)
        response = get_lihkg_response(resp)
        if self.thread_id == response.get('thread_id'):
            self.update_info(response)
            self._pages.append(ThreadPage(response))
        else:
            raise ValueError('Inconsistent \'thread_id\'.')
    
    def get_all_pages(self, time_interval=0.25):
        self.get_first_page()
        t = max(0, settings.MIN_SLEEP_TIME, time_interval)
        for _ in range(self.no_of_reply // 25):
            time.sleep(t)
            self.get_next_page()
    
    def refresh(self, time_interval=0.25):
        self._pages = self._pages[:-1]
        self.get_next_page()
        t = max(0, settings.MIN_SLEEP_TIME, time_interval)
        for _ in range(self.no_of_reply // 25 - len(self._pages) + 1):
            time.sleep(t)
            self.get_next_page()
    
    @staticmethod
    def get_thread(thread_id, time_interval=0.25):
        th = Thread(thread_id=thread_id)
        th.get_all_pages(time_interval=time_interval)
        return th
    
    def show(self, quote_depth=None):
        print_separator()
        print(self.title)
        for page in self.pages:
            page.show(quote_depth=quote_depth)
        print_separator('End of post.')
    
    def show_page(self, page_no=1, quote_depth=None):
        no_of_page = self.no_of_reply // 25 + 1
        if page_no > no_of_page:
            print_separator('No such page.')
        else:
            self.pages[page_no - 1].show(quote_depth=quote_depth)
            if page_no == no_of_page:
                print_separator('End.')
    
    def show_reply(self, reply_no=1, quote_depth=None):
        no_of_reply = self.no_of_reply
        if reply_no > no_of_reply:
            print_separator('No such post.')
        else:
            self.posts[reply_no].show(quote_depth=quote_depth, post_index=reply_no)
            if reply_no == no_of_reply:
                print_separator('End.')

