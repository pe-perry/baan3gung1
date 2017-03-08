# -*- coding: utf-8 -*-

import requests


def get_lihkg_response(resp):
    """
    get_lihkg_response(resp)
    
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

