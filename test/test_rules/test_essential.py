# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Ratina
#

"""Test cases for rule.essential module.
"""

import unittest
from rules import essential as _ess


class EssentialTestCase(unittest.TestCase):
    def test_sort_tiles(self):
        tiles = _ess.make_tiles(
            'P1', 'S2', 'P8', 'P8', 'S6', 'D3', 'D2',
            'M2', 'M5', 'M2', 'S5', 'W2', 'P7', 'P6'
        )
        sorted_tiles = _ess.sort_tiles(tiles)
        self.assertEqual(
            sorted_tiles,
            _ess.make_tiles(
                'P1', 'P6', 'P7', 'P8', 'P8', 'S2', 'S5',
                'S6', 'M2', 'M2', 'M5', 'W2', 'D2', 'D3'
            )
        )

    def test_is_jantou(self):
        tiles = _ess.make_tiles('P1', 'P1')
        self.assertTrue(_ess.is_jantou(tiles))

        tiles = _ess.make_tiles('W1', 'W1')
        self.assertTrue(_ess.is_jantou(tiles))

        tiles = _ess.make_tiles('P1', 'M1')
        self.assertFalse(_ess.is_jantou(tiles))

        tiles = _ess.make_tiles('P1', 'P1', 'P1')
        self.assertFalse(_ess.is_jantou(tiles))

        tiles = tuple()
        self.assertFalse(_ess.is_jantou(tiles))

    def test_is_same_kind(self):
        tiles = _ess.make_tiles('P1', 'P2', 'P3', 'P7')
        self.assertTrue(_ess.is_same_kind(tiles))

        tiles = _ess.make_tiles('P1', 'P2', 'M3')
        self.assertFalse(_ess.is_same_kind(tiles))

        tiles = tuple()
        self.assertTrue(_ess.is_same_kind(tiles))

    def test_is_shuntsu(self):
        tiles = _ess.make_tiles('P1', 'P2', 'P3')
        self.assertTrue(_ess.is_shuntsu(tiles))

        tiles = _ess.make_tiles('P2', 'P1', 'P3')
        self.assertFalse(_ess.is_shuntsu(tiles))

        tiles = _ess.make_tiles('P1', 'M2', 'M3')
        self.assertFalse(_ess.is_shuntsu(tiles))

        tiles = _ess.make_tiles('P1', 'P2', 'P3', 'P4')
        self.assertFalse(_ess.is_shuntsu(tiles))

        # Jihai's do not make shuntsu's at all.
        tiles = _ess.make_tiles('W1', 'W2', 'W3')
        self.assertFalse(_ess.is_shuntsu(tiles))

        tiles = tuple()
        self.assertFalse(_ess.is_shuntsu(tiles))

    def test_is_koutsu(self):
        tiles = _ess.make_tiles('P1', 'P1', 'P1')
        self.assertTrue(_ess.is_koutsu(tiles))

        tiles = _ess.make_tiles('P1', 'P1', 'P2')
        self.assertFalse(_ess.is_koutsu(tiles))

        tiles = _ess.make_tiles('P1', 'P1', 'P1', 'P1')
        self.assertFalse(_ess.is_koutsu(tiles))

        tiles = tuple()
        self.assertFalse(_ess.is_koutsu(tiles))

    def test_is_kantsu(self):
        tiles = _ess.make_tiles('P1', 'P1', 'P1', 'P1')
        self.assertTrue(_ess.is_kantsu(tiles))

        tiles = _ess.make_tiles('P1', 'P1', 'P1')
        self.assertFalse(_ess.is_kantsu(tiles))

        tiles = tuple()
        self.assertFalse(_ess.is_kantsu(tiles))

    def test_is_mentsu(self):
        tiles = _ess.make_tiles('P1', 'P2', 'P3')
        self.assertTrue(_ess.is_mentsu(tiles))

        tiles = _ess.make_tiles('P1', 'P1', 'P1')
        self.assertTrue(_ess.is_mentsu(tiles))

        tiles = _ess.make_tiles('P1', 'P1', 'P1', 'P1')
        self.assertTrue(_ess.is_mentsu(tiles))

        tiles = tuple()
        self.assertFalse(_ess.is_mentsu(tiles))
