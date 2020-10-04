# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPK_mini_mkII\config.py
# Compiled at: 2020-07-20 20:22:59
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {b'STOP': -1, 
   b'PLAY': -1, 
   b'REC': -1, 
   b'LOOP': -1, 
   b'RWD': -1, 
   b'FFWD': -1}
DEVICE_CONTROLS = (
 GENERIC_ENC1,
 GENERIC_ENC2,
 GENERIC_ENC3,
 GENERIC_ENC4,
 GENERIC_ENC5,
 GENERIC_ENC6,
 GENERIC_ENC7,
 GENERIC_ENC8)
VOLUME_CONTROLS = (
 (-1, -1),
 (-1, -1),
 (-1, -1),
 (-1, -1),
 (-1, -1),
 (-1, -1),
 (-1, -1),
 (-1, -1))
TRACKARM_CONTROLS = (-1, -1, -1, -1, -1, -1, -1, -1)
BANK_CONTROLS = {b'TOGGLELOCK': -1, 
   b'BANKDIAL': -1, 
   b'NEXTBANK': -1, 
   b'PREVBANK': -1, 
   b'BANK1': -1, 
   b'BANK2': -1, 
   b'BANK3': -1, 
   b'BANK4': -1, 
   b'BANK5': -1, 
   b'BANK6': -1, 
   b'BANK7': -1, 
   b'BANK8': -1}
PAD_TRANSLATION = (
 (0, 0, 40, 9),
 (1, 0, 38, 9),
 (2, 0, 46, 9),
 (3, 0, 44, 9),
 (0, 1, 37, 9),
 (1, 1, 36, 9),
 (2, 1, 42, 9),
 (3, 1, 82, 9),
 (0, 2, 49, 9),
 (1, 2, 55, 9),
 (2, 2, 51, 9),
 (3, 2, 53, 9),
 (0, 3, 48, 9),
 (1, 3, 47, 9),
 (2, 3, 45, 9),
 (3, 3, 43, 9))
CONTROLLER_DESCRIPTION = {b'INPUTPORT': b'MPK mini', 
   b'OUTPUTPORT': b'MPK mini', 
   b'CHANNEL': -1, 
   b'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {b'NUMSENDS': 2, 
   b'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'MASTERVOLUME': -1}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MPK_mini_mkII/config.pyc
