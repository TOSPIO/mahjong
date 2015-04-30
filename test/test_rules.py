# -*- coding: utf-8 -*-

"""
Copyright 2014-2015 Ratina

@author: Savor d'Isavano
@date: 2015-04-30

Rules test cases
"""

__author__ = "Savor d'Isavano"

import unittest
import rules as r


class RulesTestCase(unittest.TestCase):
    def test_sort_tiles(self):
        tiles = r.make_tiles(
            'P1', 'S2', 'P8', 'P8', 'S6', 'D3', 'D2',
            'M2', 'M5', 'M2', 'S5', 'W2', 'P7', 'P6'
        )
        sorted_tiles = r.sort_tiles(tiles)
        self.assertEqual(
            sorted_tiles,
            r.make_tiles(
                'P1', 'P6', 'P7', 'P8', 'P8', 'S2', 'S5',
                'S6', 'M2', 'M2', 'M5', 'W2', 'D2', 'D3'
            )
        )

    def test_is_psm(self):
        tile = r.make_tile('P1')
        self.assertTrue(r.is_psm(tile))

        tile = r.make_tile('S4')
        self.assertTrue(r.is_psm(tile))

        tile = r.make_tile('M2')
        self.assertTrue(r.is_psm(tile))

        tile = r.make_tile('W3')
        self.assertFalse(r.is_psm(tile))

    def test_is_jantou(self):
        tiles = r.make_tiles('P1', 'P1')
        self.assertTrue(r.is_jantou(tiles))

        tiles = r.make_tiles('W1', 'W1')
        self.assertTrue(r.is_jantou(tiles))

        tiles = r.make_tiles('P1', 'M1')
        self.assertFalse(r.is_jantou(tiles))

        tiles = r.make_tiles('P1', 'P1', 'P1')
        self.assertFalse(r.is_jantou(tiles))

        tiles = tuple()
        self.assertFalse(r.is_jantou(tiles))

    def test_is_same_kind(self):
        tiles = r.make_tiles('P1', 'P2', 'P3', 'P7')
        self.assertTrue(r.is_same_kind(tiles))

        tiles = r.make_tiles('P1', 'P2', 'M3')
        self.assertFalse(r.is_same_kind(tiles))

        tiles = tuple()
        self.assertTrue(r.is_same_kind(tiles))

    def test_is_shuntsu(self):
        tiles = r.make_tiles('P1', 'P2', 'P3')
        self.assertTrue(r.is_shuntsu(tiles))

        tiles = r.make_tiles('P2', 'P1', 'P3')
        self.assertFalse(r.is_shuntsu(tiles))

        tiles = r.make_tiles('P1', 'M2', 'M3')
        self.assertFalse(r.is_shuntsu(tiles))

        tiles = r.make_tiles('P1', 'P2', 'P3', 'P4')
        self.assertFalse(r.is_shuntsu(tiles))

        # Jihai's do not make shuntsu's at all.
        tiles = r.make_tiles('W1', 'W2', 'W3')
        self.assertFalse(r.is_shuntsu(tiles))

        tiles = tuple()
        self.assertFalse(r.is_shuntsu(tiles))

    def test_is_koutsu(self):
        tiles = r.make_tiles('P1', 'P1', 'P1')
        self.assertTrue(r.is_koutsu(tiles))

        tiles = r.make_tiles('P1', 'P1', 'P2')
        self.assertFalse(r.is_koutsu(tiles))

        tiles = r.make_tiles('P1', 'P1', 'P1', 'P1')
        self.assertFalse(r.is_koutsu(tiles))

        tiles = tuple()
        self.assertFalse(r.is_koutsu(tiles))

    def test_is_kantsu(self):
        tiles = r.make_tiles('P1', 'P1', 'P1', 'P1')
        self.assertTrue(r.is_kantsu(tiles))

        tiles = r.make_tiles('P1', 'P1', 'P1')
        self.assertFalse(r.is_kantsu(tiles))

        tiles = tuple()
        self.assertFalse(r.is_kantsu(tiles))

    def test_is_mentsu(self):
        tiles = r.make_tiles('P1', 'P2', 'P3')
        self.assertTrue(r.is_mentsu(tiles))

        tiles = r.make_tiles('P1', 'P1', 'P1')
        self.assertTrue(r.is_mentsu(tiles))

        tiles = r.make_tiles('P1', 'P1', 'P1', 'P1')
        self.assertTrue(r.is_mentsu(tiles))

        tiles = tuple()
        self.assertFalse(r.is_mentsu(tiles))

    def test_check_ron_regular(self):
        tiles = r.make_tiles(
            'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P3', 'P3', 'P3',
            'P4', 'P4', 'P4', 'D1', 'D1'
        )
        result_list = r._check_ron_regular(tiles)

        result1 = {
            'shuntsu': [
                ('P1', 'P2', 'P3'),
                ('P1', 'P2', 'P3'),
                ('P1', 'P2', 'P3'),
            ],
            'koutsu': [
                ('P4', 'P4', 'P4'),
            ],
            'jantou': [
                ('D1', 'D1')
            ]
        }
        self.assertIn(result1, result_list)

        result1 = {
            'shuntsu': [
                ('P2', 'P3', 'P4'),
                ('P2', 'P3', 'P4'),
                ('P2', 'P3', 'P4'),
            ],
            'koutsu': [
                ('P1', 'P1', 'P1'),
            ],
            'jantou': [
                ('D1', 'D1')
            ]
        }
        self.assertIn(result1, result_list)
