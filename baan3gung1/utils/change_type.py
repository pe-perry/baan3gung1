# -*- coding: utf-8 -*-


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

