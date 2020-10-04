# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\TriggerFinger\config.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {b'STOP': GENERIC_STOP, 
   b'PLAY': GENERIC_PLAY, 
   b'REC': GENERIC_REC, 
   b'LOOP': GENERIC_LOOP, 
   b'RWD': GENERIC_RWD, 
   b'FFWD': GENERIC_FFWD}
DEVICE_CONTROLS = (
 GENERIC_ENC1,
 GENERIC_ENC2,
 GENERIC_ENC3,
 GENERIC_ENC4,
 GENERIC_ENC5,
 GENERIC_ENC6,
 GENERIC_ENC7,
 GENERIC_ENC8)
VOLUME_CONTROLS = GENERIC_SLIDERS
TRACKARM_CONTROLS = (
 GENERIC_BUT1,
 GENERIC_BUT2,
 GENERIC_BUT3,
 GENERIC_BUT4,
 GENERIC_BUT5,
 GENERIC_BUT6,
 GENERIC_BUT7,
 GENERIC_BUT8)
BANK_CONTROLS = {b'TOGGLELOCK': GENERIC_BUT9, 
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
 (0, 0, 49, 9),
 (1, 0, 57, 9),
 (2, 0, 51, 9),
 (3, 0, 53, 9),
 (0, 1, 56, 9),
 (1, 1, 39, 9),
 (2, 1, 42, 9),
 (3, 1, 46, 9),
 (0, 2, 50, 9),
 (1, 2, 48, 9),
 (2, 2, 45, 9),
 (3, 2, 41, 9),
 (0, 3, 36, 9),
 (1, 3, 38, 9),
 (2, 3, 40, 9),
 (3, 3, 37, 9))
CONTROLLER_DESCRIPTIONS = {b'INPUTPORT': b'Trigger', 
   b'OUTPUTPORT': b'Trigger', 
   b'CHANNEL': 9, 
   b'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {b'NUMSENDS': 2, 
   b'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'MASTERVOLUME': 7}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/TriggerFinger/config.pyc
