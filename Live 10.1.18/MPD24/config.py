# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPD24\config.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {b'STOP': GENERIC_STOP, 
   b'PLAY': GENERIC_PLAY, 
   b'REC': GENERIC_REC, 
   b'LOOP': GENERIC_LOOP, 
   b'RWD': GENERIC_RWD, 
   b'FFWD': GENERIC_FFWD, 
   b'NORELEASE': 0}
DEVICE_CONTROLS = GENERIC_ENCODERS
VOLUME_CONTROLS = (
 (
  GENERIC_SLI1, -1),
 (
  GENERIC_SLI2, -1),
 (
  GENERIC_SLI3, -1),
 (
  GENERIC_SLI4, -1),
 (
  GENERIC_SLI5, -1),
 (
  GENERIC_SLI6, -1),
 (
  GENERIC_SLI7, -1),
 (
  GENERIC_SLI8, -1))
TRACKARM_CONTROLS = (
 GENERIC_BUT1,
 GENERIC_BUT2,
 GENERIC_BUT3,
 GENERIC_BUT4,
 GENERIC_BUT5,
 GENERIC_BUT6,
 GENERIC_BUT7,
 GENERIC_BUT8)
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
 (0, 0, 48, 0),
 (1, 0, 49, 0),
 (2, 0, 50, 0),
 (3, 0, 51, 0),
 (0, 1, 44, 0),
 (1, 1, 45, 0),
 (2, 1, 46, 0),
 (3, 1, 47, 0),
 (0, 2, 40, 0),
 (1, 2, 41, 0),
 (2, 2, 42, 0),
 (3, 2, 43, 0),
 (0, 3, 36, 0),
 (1, 3, 37, 0),
 (2, 3, 38, 0),
 (3, 3, 39, 0))
CONTROLLER_DESCRIPTION = {b'INPUTPORT': b'Akai MPD24', 
   b'OUTPUTPORT': b'Akai MPD24', 
   b'CHANNEL': 0, 
   b'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {b'NUMSENDS': 2, 
   b'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'MASTERVOLUME': -1}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MPD24/config.pyc
