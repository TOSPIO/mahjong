# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Ratina
#

"""All agari patterns.

All agari patterns in use by any rules.
Note these are patterns only, disrespecting rule-specific
playground info, player info and other factors.
"""

from abc import ABCMeta, abstractmethod
from copy import deepcopy
from .essential import *


def _extract_successor(base, tiles):
    # TODO: Optimize. Check the tiles one by one.
    successor = get_successor(base)
    try:
        successor_idx = tiles[:7].index(successor)
    except ValueError:
        # Not found
        return None
    return tiles[successor_idx], \
        tiles[:successor_idx] + tiles[successor_idx+1:]


def _extract_identical(base, tiles):
    if not tiles:
        return None
    if tiles[0] == base:
        return tiles[0], tiles[1:]


class AgariPattern(metaclass=ABCMeta):
    @abstractmethod
    def _check_agari(self):
        # This function should return a list of dict
        # containing all categorized melds.
        # And possibly multiple categorizations.
        # Return an empty on failure.
        pass

    def check_agari(self):
        return self._check_agari() + \
            (
                hasattr(self, '_successor') and
                self._successor.check_agari() or
                []
            )

    def __rshift__(self, other):
        self._successor = other
        other._tiles = self._tiles
        return other

    def __rrshift__(self, other):
        # The left operand must be a list of tiles.
        self._tiles = other
        return self


class RegularAgariPattern(AgariPattern):
    @classmethod
    def _check_agari_regular(cls, tiles):
        '''Check for regular agari.

        Arguments:
        tiles: tiles as a list of string defined in _tiles
        '''
        tiles_dict = {
            'jantou': [],
            'shuntsu': [],
            'koutsu': [],
        }
        agari_patterns = []
        cls._check_agari_regular_1(
            tiles_dict, sort_tiles(tiles), agari_patterns
        )
        return agari_patterns

    @classmethod
    def _check_agari_regular_1(cls, tiles_dict, rest_tiles, agari_patterns):
        '''Check for regular agari. Can be used with a small set of tiles.
        (i.e. With fuuros excluded.)

        Arguments:
        tiles_dict: a dict of list of jantous, shuntsus and koutsus, e.g.
                    {
                        'jantou': [('W2', 'W2')],
                        'shuntsu': [('P1', 'P2', 'P3'), ('M6', 'M7', 'M8)],
                        'koutsu': [('S4', 'S4', 'S4')]
                    }
        rest_tiles: a list of tiles that exclude those contained
                    in ``tiles_dict``.
        '''
        tiles_dict = deepcopy(tiles_dict)

        if not rest_tiles:
            # All other tiles are valid mentsu's.
            # A jantou determines an agari hand.
            if len(tiles_dict['jantou']) == 1:
                agari_patterns.append(tiles_dict)
                return True
            return False

        meld = []
        a = rest_tiles[0]
        rest_tiles = rest_tiles[1:]
        meld.append(a)
        b = _extract_identical(a, rest_tiles)
        if b is not None:
            # Got a pair
            b, _rest_tiles = b
            meld.append(b)
            c = _extract_identical(b, _rest_tiles)
            if c is not None:
                # Got a koutsu
                c, _rest_tiles = c
                meld.append(c)
                tiles_dict['koutsu'].append(tuple(meld))
                cls._check_agari_regular_1(
                    tiles_dict, _rest_tiles, agari_patterns
                )
                tiles_dict['koutsu'].pop()
            else:
                # Got a jantou
                if len(tiles_dict['jantou']) > 0:
                    # More than one jantou. Proceed with other checks
                    pass
                else:
                    tiles_dict['jantou'].append(tuple(meld))
                    cls._check_agari_regular_1(
                        tiles_dict, _rest_tiles, agari_patterns
                    )
                    tiles_dict['jantou'].pop()

        del meld[1:]
        b = c = None
        # Shuntsu check
        b = _extract_successor(a, rest_tiles)
        if b is not None:
            # Got a semi-shuntsu
            b, _rest_tiles = b
            meld.append(b)
            c = _extract_successor(b, _rest_tiles)
            if c is not None:
                c, _rest_tiles = c
            meld.append(c)
            tiles_dict['shuntsu'].append(tuple(meld))
            cls._check_agari_regular_1(tiles_dict, _rest_tiles, agari_patterns)
            tiles_dict['shuntsu'].pop()

    def _check_agari(self):
        return self._check_agari_regular(self._tiles)
