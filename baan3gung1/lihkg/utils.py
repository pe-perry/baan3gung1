# -*- coding: utf-8 -*-

import requests


def change_type(x, func):
    """
    change_type(x, func)
    
    Change object type
    
    Parameters:
    -----------
    x: object
        Object to be converted.
    
    func: function
        Function for conversion.
    
    Return:
    -------
    func(x) or None if there are value or type error.
    """
    try:
        return func(x)
    except ValueError:
        return None
    except TypeError:
        return None


def get_response(resp):
    """
    get_response(resp)
    
    Obtain the data of the response object.
    
    Return:
    -------
    A dictionary.
    """
    response = dict()
    if isinstance(resp, requests.models.Response):
        if resp.status_code == 200:
            response = resp.json()
            if response.get('success', 0) == 1:
                response = response.get('response', dict())
        return response
    else:
        raise TypeError('resp must be a \'requests.models.Response\' object.')

