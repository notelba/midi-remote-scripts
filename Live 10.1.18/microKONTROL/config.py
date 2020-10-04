# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\microKONTROL\config.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {b'STOP': GENERIC_STOP, 
   b'PLAY': GENERIC_PLAY, 
   b'REC': GENERIC_REC, 
   b'LOOP': GENERIC_LOOP, 
   b'RWD': GENERIC_RWD, 
   b'FFWD': GENERIC_FFWD}
DEVICE_CONTROLS = (
 (
  GENERIC_ENC1, 0),
 (
  GENERIC_ENC2, 1),
 (
  GENERIC_ENC3, 2),
 (
  GENERIC_ENC4, 3),
 (
  GENERIC_ENC5, 4),
 (
  GENERIC_ENC6, 5),
 (
  GENERIC_ENC7, 6),
 (
  GENERIC_ENC8, 7))
VOLUME_CONTROLS = (
 (
  GENERIC_SLI1, 0),
 (
  GENERIC_SLI2, 1),
 (
  GENERIC_SLI3, 2),
 (
  GENERIC_SLI4, 3),
 (
  GENERIC_SLI5, 4),
 (
  GENERIC_SLI6, 5),
 (
  GENERIC_SLI7, 6),
 (
  GENERIC_SLI8, 7))
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
   b'NEXTBANK': GENERIC_PAD5, 
   b'PREVBANK': GENERIC_PAD1, 
   b'BANK1': (47, 1), 
   b'BANK2': (46, 8), 
   b'BANK3': (45, 8), 
   b'BANK4': (44, 8), 
   b'BANK5': (85, 8), 
   b'BANK6': (86, 8), 
   b'BANK7': (87, 8), 
   b'BANK8': (88, 8)}
PAD_TRANSLATION = (
 (0, 0, 61, 9),
 (1, 0, 69, 9),
 (2, 0, 65, 9),
 (3, 0, 63, 9),
 (0, 1, 60, 9),
 (1, 1, 59, 9),
 (2, 1, 57, 9),
 (3, 1, 55, 9),
 (0, 2, 49, 9),
 (1, 2, 51, 9),
 (2, 2, 68, 9),
 (3, 2, 56, 9),
 (0, 3, 48, 9),
 (1, 3, 52, 9),
 (2, 3, 54, 9),
 (3, 3, 58, 9))
CONTROLLER_DESCRIPTIONS = {b'INPUTPORT': b'microKONTROL (PORT B)', 
   b'OUTPUTPORT': b'microKONTROL (CTRL)', 
   b'CHANNEL': 8, 
   b'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {b'NUMSENDS': 2, 
   b'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'MASTERVOLUME': -1}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/microKONTROL/config.pyc
