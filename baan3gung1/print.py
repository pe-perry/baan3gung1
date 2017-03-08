# -*- coding: utf-8 -*-

# Reference
# http://stackoverflow.com/questions/2422177/python-how-can-i-replace-full-width-characters-with-half-width-characters

# Dictionary
FULL_TO_HALF = {
    i + 0xFEE0: i for i in range(0x21, 0x7F)
}
FULL_TO_HALF[0x3000] = 0x20  # Space

HALF_TO_FULL = {
    i: i + 0xFEE0 for i in range(0x21, 0x7F)
}
HALF_TO_FULL[0x20] = 0x3000  # Space


# Translation functions
def translate_text(*args, table):
    if not isinstance(table, dict):
        raise TypeError('table must be a dictionary.')
    # Translation
    if len(args) == 1:
        txt = str(args[0]).translate(table)
    else:
        txt = [str(x).translate(table) for x in args]
    return txt


def translate_to_full_width(*args):
    txt = translate_text(*args, table=HALF_TO_FULL)
    return txt


def translate_to_half_width(*args):
    txt = translate_text(*args, table=FULL_TO_HALF)
    return txt


# Print functions
def print_full_width(*args, **kwargs):
    txt = translate_to_full_width(*args)
    if isinstance(txt, str):
        print(txt, **kwargs)
    else:
        print(*txt, **kwargs)


def print_half_width(*args, **kwargs):
    txt = translate_to_half_width(*args)
    if isinstance(txt, str):
        print(txt, **kwargs)
    else:
        print(*txt, **kwargs)

