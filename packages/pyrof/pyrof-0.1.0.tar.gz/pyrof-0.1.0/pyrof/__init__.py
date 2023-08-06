#! /usr/bin/env python

from .menu import Menu, MenuError, MenuResult

def new_rofi(**kwargs):
    """Create an instance of dynmen.rofi.Rofi(**kwargs)

    The keyword arguments set the corresponding attribute
    on the Rofi instance.
    """
    from .rofi import Rofi
    return Rofi(**kwargs)
