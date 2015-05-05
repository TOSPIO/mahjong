# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Ratina
#

"""Object class definitions.
"""


class Tile:
    _kind_order = ('P', 'S', 'M', 'W', 'D')

    def __init__(self, kind, number):
        self._str_repr = "{}{}".format(kind, number)
        self._kind = kind
        self._number = number

    @property
    def kind(self):
        return self._kind

    @property
    def number(self):
        return self._number

    def __repr__(self):
        return self._str_repr

    def __lt__(self, other):
        kindl = self._kind_order.index(self.kind)
        kindr = self._kind_order.index(other.kind)
        if kindl < kindr:
            return True
        elif kindl == kindr:
            return self.number < other.number
        return False

    def __eq__(self, other):
        return str(self) == str(other)
