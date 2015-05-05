# -*- coding: utf-8 -*-
#
# Copyright 2014-2015 Ratina
#

"""Mahjong rule definitions and checkers.

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

Agari: A player wins the game if he `agari`s.
     His hand must match one of the agari patterns for him to ron.
Tsumo: A player agari's with the last tile drawn by himself.
Ron: A player agari's with the other player's discard.

Ron patterns:
Regular: four mentsu's and one jantou.
Seven-pairs: Seven pairs.
"""

from .agaris import *
