# -*- coding: utf-8 -*-

import re
from datetime import datetime

import bs4
from bs4 import BeautifulSoup

from .User import User
from ..utils.change_type import change_type


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

