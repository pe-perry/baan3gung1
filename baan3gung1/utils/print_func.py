# -*- coding: utf-8 -*-

from .translate_func import translate_to_full_width, translate_to_half_width


# Translate all text to full width and print
def print_full_width(*args, **kwargs):
    txt = translate_to_full_width(*args)
    if isinstance(txt, str):
        print(txt, **kwargs)
    else:
        print(*txt, **kwargs)


# Translate all text to half width and print
def print_half_width(*args, **kwargs):
    txt = translate_to_half_width(*args)
    if isinstance(txt, str):
        print(txt, **kwargs)
    else:
        print(*txt, **kwargs)


# Print separator line
def print_separator(text='', width=80):
    if text == '':
        print('-' * width)
    else:
        if len(text) % 2 == 1:
            text += ' '
        v = (width - len(text)) // 2 - 1
        print('-' * v, text, '-' * v)

