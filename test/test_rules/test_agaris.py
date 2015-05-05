# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Ratina
#

"""Test cases for essential.agaris module.
"""

import unittest
from rules.essential import *
from rules.agaris import *


class RulesTestCase(unittest.TestCase):
    def test_regular(self):
        tiles = make_tiles(
            'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P3', 'P3', 'P3',
            'P4', 'P4', 'P4', 'D1', 'D1'
        )
        result_list = (
            tiles >> RegularAgariPattern()
        ).check_agari()

        result1 = ('regular', {
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
        })
        self.assertIn(result1, result_list)

        result1 = ('regular', {
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
        })
        self.assertIn(result1, result_list)

    def test_seven_pair(self):
        tiles = make_tiles(
            'P1', 'P1', 'P1', 'M2', 'P1', 'M2', 'D1',
            'D1', 'S2', 'S2', 'S4', 'S4', 'S3', 'S3'
        )

        result_list = (
            tiles >> SevenPairPattern()
        ).check_agari()

        result1 = ('sevenpair', {
            'pairs': [
                ('M2', 'M2'),
                ('P1', 'P1'),
                ('P1', 'P1'),
                ('S2', 'S2'),
                ('S3', 'S3'),
                ('S4', 'S4'),
                ('D1', 'D1')
            ]
        })
        self.assertIn(result1, result_list)

    def test_seven_pair_strict(self):
        tiles = make_tiles(
            'P1', 'P1', 'P1', 'M2', 'P1', 'M2', 'D1',
            'D1', 'S2', 'S2', 'S4', 'S4', 'S3', 'S3'
        )

        result_list = (
            tiles >> SevenPairPattern(is_strict=True)
        ).check_agari()

        self.assertEqual(len(result_list), 0)

    def test_kokushi(self):
        tiles = make_tiles(
            'M1', 'M9', 'P1', 'P9', 'S1', 'S9',
            'W1', 'W2', 'W3', 'W4', 'D1', 'D2', 'D3', 'M1'
        )

        result_list = (
            tiles >> KokushiPattern()
        ).check_agari()

        result1 = ('kokushi', {
            'jantou': 'M1',
            'kokushi': (
                'M1', 'M9', 'P1', 'P9', 'S1', 'S9',
                'W1', 'W2', 'W3', 'W4', 'D1', 'D2', 'D3'
            )
        })
        self.assertIn(result1, result_list)

        tiles = make_tiles(
            'M1', 'M9', 'P1', 'P9', 'S1', 'S9',
            'W1', 'W2', 'W3', 'W4', 'D1', 'D2', 'D3', 'D3'
        )

        result_list = (
            tiles >> KokushiPattern()
        ).check_agari()

        result2 = ('kokushi', {
            'jantou': 'D3',
            'kokushi': (
                'M1', 'M9', 'P1', 'P9', 'S1', 'S9',
                'W1', 'W2', 'W3', 'W4', 'D1', 'D2', 'D3'
            )
        })
        self.assertIn(result2, result_list)

        tiles = make_tiles(
            'M1', 'M9', 'P1', 'P9', 'S1', 'S9',
            'W1', 'W2', 'W3', 'W4', 'D1', 'D2', 'D3', 'P2'
        )

        result_list = (
            tiles >> KokushiPattern()
        ).check_agari()

        self.assertEqual(len(result_list), 0)
