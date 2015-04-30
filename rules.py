# -*- coding: utf-8 -*-

"""
Copyright 2014-2015 Ratina

@author: Savor d'Isavano
@date: 2015-04-30

Mahjong rule definitions and checkers.
We employ the names defined in Japanese mahjong rules.

To denote the 43 unique tiles, we use the following representations:
P: Pinzu(筒子) (P1~P9)
S: Souzu(索子) (S1~S9)
M: Manzu(萬子) (M1~M9)
W: Kazehai(風牌) (W1~W4)
D: Sangenhai(三元牌) (D1~D3)


Rules:

Term definitions:
Jantou: a pair of identical tiles. e.g. ('P1', 'P1').
Shuntsu: a meld of three suited tiles in sequence.
         e.g. ('M1', 'M2', 'M3')
Koutsu: a meld of three identical tiles.
        e.g. ('M1', 'M1', 'M1')
Kantsu: a meld of four identical tiles (fuuro only).
        e.g. ('M1', 'M1', 'M1', 'M1')
Mentsu: a shuntsu, koutsu or kantsu.
Fuuro: A mentsu place aside of hand tiles.

Ron: A player wins the game if he `ron`s.
     His hand must match one of the ron patterns for him to ron.

Ron patterns:
Regular: four mentsu's and one jantou.
Seven-pairs: Seven pairs.
"""

__author__ = "Savor d'Isavano"

from copy import copy, deepcopy

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


def make_tile(str_repr):
    kind = str_repr[0]
    number = int(str_repr[1:])
    return Tile(kind, number)
    

def make_tiles(*str_reprs):
    return tuple(make_tile(tile) for tile in str_reprs)


# All tiles
_tiles = make_tiles(
    'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9',
    'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9',
    'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9',
    'W1', 'W2', 'W3', 'W4',
    'D1', 'D2', 'D3',
)


def is_psm(tile):
    '''Checks if a tile is a pinzu, souzu or manzu.

    Returns:
    True/False
    '''
    return tile.kind in ('P', 'S', 'M')

def is_jihai(tile):
    '''Check is a tile is a kazehai or sangenhai.

    Returns:
    True/False
    '''
    return tile.kind in ('W', 'D')

def _sort_key_func(tile):
    return _tiles.index(tile)

    
def sort_tiles(tiles):
    return tuple(sorted(tiles))


def is_jantou(tiles):
    if len(tiles) == 2 and tiles[0] == tiles[1]:
        return True
    return False


def is_same_kind(tiles):
    if len(tiles) == 0:
        return True

    return all(tile.kind == tiles[0].kind for tile in tiles)


def is_shuntsu(tiles):
    if len(tiles) != 3:
        return False

    if not is_same_kind(tiles):
        return False

    if not is_psm(tiles[0]):
        return False

    if tiles[1].number - tiles[0].number == 1 and tiles[2].number - tiles[1].number == 1:
        return True
    
    return False

    

def is_koutsu(tiles):
    if len(tiles) != 3:
        return False

    return all(tile == tiles[0] for tile in tiles)


def is_kantsu(tiles):
    if len(tiles) != 4:
        return False

    return all(tile == tiles[0] for tile in tiles)


def is_mentsu(tiles):
    return is_shuntsu(tiles) or is_koutsu(tiles) or is_kantsu(tiles)


def _is_successor(tile, tile_succ):
    if tile.kind != tile_succ.kind:
        return False

    if is_psm(tile):
        if 1 <= tile.number <= 8 and tile_succ.number - tile.number == 1:
            return True

    if tile.kind == 'W':
        if 1 <= tile.number <= 3 and tile_succ.number - tile.number == 1:
            return True

    if tile.kind == 'D':
        if 1 <= tile.number <= 2 and tile_succ.number - tile.number == 1:
            return True


def _get_successor(tile):
    if is_psm(tile):
        if 1 <= tile.number <= 8:
            return Tile(tile.kind, tile.number+1)
    # Does not apply to jihai's.
    # if tile.kind == 'W':
    #     if 1 <= tile.number <= 3:
    #         return Tile('W', tile.number+1)
    # if tile.kind == 'D':
    #     if 1 <= tile.number <= 2:
    #         return Tile('D', tile.number+1)
        
    return None


def _extract_successor(base, tiles):
    # TODO: Optimize. Check the tiles one by one.
    successor = _get_successor(base)
    try:
        successor_idx = tiles[:7].index(successor)
    except ValueError:
        # Not found
        return None
    return tiles[successor_idx], tiles[:successor_idx] + tiles[successor_idx+1:]


def _extract_identical(base, tiles):
    if not tiles:
        return None
    if tiles[0] == base:
        return tiles[0], tiles[1:]

def _check_ron_regular(tiles):
    '''Check for regular ron

    Arguments:
    tiles: tiles as a list of string defined in _tiles

    '''
    tiles_dict = {
        'jantou': [],
        'shuntsu': [],
        'koutsu': [],
    }
    ron_patterns = []
    _check_ron_regular_1(tiles_dict, sort_tiles(tiles), ron_patterns)
    return ron_patterns
    

def _check_ron_regular_1(tiles_dict, rest_tiles, ron_patterns):
    '''Check for regular ron. Can be used with a small set of tiles.
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
        # All other tiles are valid mentsu's. A jantou determines a ron hand.
        if len(tiles_dict['jantou']) == 1:
            ron_patterns.append(tiles_dict)
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
            _check_ron_regular_1(tiles_dict, _rest_tiles, ron_patterns)
            tiles_dict['koutsu'].pop()
        else:
            # Got a jantou
            if len(tiles_dict['jantou']) > 0:
                # More than one jantou. Proceed with other checks
                pass
            else:
                tiles_dict['jantou'].append(tuple(meld))
                _check_ron_regular_1(tiles_dict, _rest_tiles, ron_patterns)
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
            _check_ron_regular_1(tiles_dict, _rest_tiles, ron_patterns)
            tiles_dict['shuntsu'].pop()
