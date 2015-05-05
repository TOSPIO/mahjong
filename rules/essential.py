# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Ratina
#

"""Useful functions.
"""

from .structures import Tile


def make_tile(str_repr):
    kind = str_repr[0]
    number = int(str_repr[1:])
    return Tile(kind, number)


def make_tiles(*str_reprs):
    return tuple(make_tile(tile) for tile in str_reprs)


# All tiles
_tiles = make_tiles(
    'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9',
    'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9',
    'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9',
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
    return tuple(sorted(tiles, key=_sort_key_func))


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

    if tiles[1].number - tiles[0].number == 1 \
       and tiles[2].number - tiles[1].number == 1:
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


def is_successor(tile, tile_succ):
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


def get_successor(tile):
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
