# -*- coding: utf-8 -*-

from datetime import datetime

from ..utils import change_type


class User(object):
    def __init__(self, data=None):
        if isinstance(data, dict):
            self._data = data
        elif data is None:
            self._data = dict()
        else:
            raise TypeError('data must be a \'dict\' object.')
    
    def __repr__(self):
        print_text = '<User {:} - {:}>'
        print_text = print_text.format(self.id, self.name)
        return print_text
    
    @property
    def id(self):
        return self._data.get('user_id')
    
    @property
    def name(self):
        return self._data.get('nickname')
    
    @property
    def gender(self):
        return self._data.get('gender')
    
    @property
    def level(self):
        return self._data.get('level')
    
    @property
    def create_time(self):
        t = self._data.get('create_time')
        t = change_type(t, int)
        t = change_type(t, datetime.fromtimestamp)
        return t
    
    @property
    def status(self):
        return self._data.get('status')

