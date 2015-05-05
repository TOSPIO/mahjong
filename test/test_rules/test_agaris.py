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
    def test_check_agari_regular(self):
        tiles = make_tiles(
            'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P3', 'P3', 'P3',
            'P4', 'P4', 'P4', 'D1', 'D1'
        )
        result_list = (
            tiles >> RegularAgariPattern()
        ).check_agari()

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
