# -*- coding: utf-8 -*-

import itertools
import re
import time
from datetime import datetime

import bs4
from bs4 import BeautifulSoup

from baan3gung1 import lihkg
from .User import User
from .utils import change_type, get_response


def remove_escape_code(x):
    return re.sub(r'[\n\r]', '', x)


# Functions to handle tags and their contents
def remove_tag(soup, tag_name, keep_content=True, keep_text_only=False):
    soup = soup.__copy__()
    parser_name = soup.builder.NAME
    for x in soup.find_all(tag_name):
        if keep_content:
            if keep_text_only:
                x.replace_with(x.text)
            else:
                text = ''.join(str(c) for c in x.contents)
                x.replace_with(BeautifulSoup(text.encode(), 'html.parser'))
        else:
            x.replace_with('')
    if keep_content and not keep_text_only:
        soup = BeautifulSoup(str(soup).encode(), parser_name)
    return soup


def clean_style(soup):
    soup = soup.__copy__()
    soup = remove_tag(soup, 'div')
    soup = remove_tag(soup, 'p')
    soup = remove_tag(soup, 'span', keep_text_only=True)
    soup = remove_tag(soup, 'strong', keep_text_only=True)
    soup = remove_tag(soup, 'ins', keep_text_only=True)
    return soup


# Function to handle quotations
def find_blockquotes(soup):
    blockquotes = []
    if soup is not None:
        soup = soup.__copy__()
        first_bq = soup.find('blockquote')
        if first_bq is not None:
            blockquotes = [first_bq] + first_bq.find_next_siblings('blockquote')
    return blockquotes


def read_quote(tag):
    if tag.name == 'blockquote':
        tag = tag.__copy__()
        children_blockquotes = find_blockquotes(tag)
        for x in tag.find_all('blockquote'):
            x.replace_with('')
        contents = [
            bs4.element.NavigableString(c.strip()) if isinstance(c, bs4.element.NavigableString) else c
            for c in tag.contents
            if str(c).strip() != ''
        ]
        quote = {
            'content': contents,
            'children_blockquotes': children_blockquotes
        }
    else:
        quote = dict()
    return quote


def organise_quotes(quotes, level=-1):
    contents = list()
    for q in quotes:
        children_blockquotes = q.get('children_blockquotes', [])
        if len(children_blockquotes) > 0:
            blockquotes = [read_quote(q) for q in children_blockquotes]
            contents.extend(organise_quotes(blockquotes, level - 1))
        contents.append({'level': level,
                         'content': q.get('content', None)})
    return contents


def extract_quotes(soup):
    if soup.name == 'blockquote':
        quotes = [read_quote(soup)]
    else:
        blockquotes_1st_layer = find_blockquotes(soup)
        quotes = [read_quote(x) for x in blockquotes_1st_layer]
    quotes = organise_quotes(quotes)
    return quotes


def print_content(x, indentation='', quote_depth=None):
    newline = '\n' + indentation
    if x.name == 'blockquote':
        print('> ', end='')
        max_depth = -min(bq['level'] for bq in extract_quotes(x))
        # quote depth
        if quote_depth is None:
            quote_depth = max_depth
        else:
            quote_depth = min(max_depth, quote_depth)
        # Print quote contents
        for bq in extract_quotes(x):
            bq_lv = bq['level']
            for bq_c in bq['content']:
                v = quote_depth + bq_lv
                if bq_lv >= -quote_depth:
                    print_content(bq_c, indentation=indentation + ' ' * v + '> ')
    elif x.name == 'br':
        print('', end=newline)
    elif x.name == 'img':
        src = x.attrs['src']
        if 'hkgmoji' in x.attrs.get('class', []):
            hkgmoji = re.sub('.*faces/(.*)\.[a-z]+$', '\\1', src)
            print_text = '({:})'.format(hkgmoji)
            print(print_text, end=' ')
        else:
            print_text = '[img]({:})'.format(src)
            print(newline + print_text, end=newline)
    elif x.name == 'a':
        href = x.attrs['href']
        print_text = '[a]({:})'.format(href)
        print(print_text, end=' ')
    elif x.name in ['p', 'span']:
        print_text = x.text.strip()
        print(print_text, end=' ')
    else:
        print_text = str(x).strip()
        print(print_text, end=' ')


def print_separator(text='', width=80):
    if text == '':
        print('-' * width)
    else:
        if len(text) % 2 == 1:
            text += ' '
        v = (width - len(text)) // 2 - 1
        print('-' * v, text, '-' * v)


# Class Post
class Post(object):
    def __init__(self, data=None):
        if isinstance(data, dict):
            self._data = data
        elif data is None:
            self._data = dict()
        else:
            raise TypeError('data must be a \'dict\' object.')
    
    def __repr__(self):
        print_text = '<Thread {:} - Post {:} (User {:} @ {:})>'
        print_text = print_text.format(
            self.thread_id,
            self.id,
            self.user.id,
            self.reply_time
        )
        return print_text
    
    @property
    def id(self):
        return self._data.get('post_id')
    
    @property
    def raw_contents(self):
        return self._data.get('msg')
    
    @property
    def contents(self):
        doc = self.raw_contents
        doc = remove_escape_code(doc)
        soup = BeautifulSoup(doc.encode(), 'lxml')
        soup = clean_style(soup)
        soup = soup.find('body')
        c = [x for x in soup.contents if str(x).strip() != '']
        return c
    
    @property
    def reply_time(self):
        t = self._data.get('reply_time')
        t = change_type(t, int)
        return change_type(t, datetime.fromtimestamp)
    
    @property
    def user(self):
        u = User(self._data.get('user', dict()))
        return u
    
    @property
    def thread_id(self):
        return self._data.get('thread_id')
    
    def show(self, quote_depth=None, post_index=None):
        indent = '  '
        if post_index is not None:
            print('#', post_index, sep='')
        # User name & reply time
        u = '{:} @ {:}:\n'.format(self.user.name, self.reply_time)
        print(u, end='\n' + indent)
        # Contents
        for x in self.contents:
            print_content(x, indentation=indent, quote_depth=quote_depth)
        print('\n\n' + '-' * 80)


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
        response = get_response(resp)
        return ThreadPage(data=response)
    
    def refresh(self):
        if self.thread_id is not None and self.page is not None:
            resp = lihkg.requests.get_thread(thread_id=self.thread_id, page=self.page)
            response = get_response(resp)
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


class Thread(object):
    def __init__(self, thread_id, post_per_page=25):
        self.thread_id = thread_id
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
        response = get_response(resp=resp)
        self.thread_id = response.get('thread_id')
        self.title = response.get('title')
        self.category = response.get('category')
        self.create_time = change_type(response.get('create_time'), datetime.fromtimestamp)
        self.update_info(response)
        self._pages.append(ThreadPage(response))
    
    def get_next_page(self):
        current_page = len(self._pages)
        resp = lihkg.requests.get_thread(thread_id=self.thread_id, page=current_page + 1)
        response = get_response(resp)
        if self.thread_id == response.get('thread_id'):
            self.update_info(response)
            self._pages.append(ThreadPage(response))
        else:
            raise ValueError('Inconsistent \'thread_id\'.')
    
    def get_all_pages(self, time_interval=0.25):
        self.get_first_page()
        for _ in range(self.no_of_reply // 25):
            time.sleep(time_interval)
            self.get_next_page()
    
    def refresh(self, time_interval=0.25):
        self._pages = self._pages[:-1]
        self.get_next_page()
        for _ in range(self.no_of_reply // 25 - len(self._pages) + 1):
            time.sleep(time_interval)
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


__all__ = ['Post', 'ThreadPage', 'Thread']

