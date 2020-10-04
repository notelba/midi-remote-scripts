# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPD32\config.py
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
DEVICE_CONTROLS = (
 (
  GENERIC_ENC1, 0),
 (
  GENERIC_ENC2, 0),
 (
  GENERIC_ENC3, 0),
 (
  GENERIC_ENC4, 0),
 (
  GENERIC_ENC5, 0),
 (
  GENERIC_ENC6, 0),
 (
  GENERIC_ENC7, 0),
 (
  GENERIC_ENC8, 0))
VOLUME_CONTROLS = (
 (
  GENERIC_SLI1, 0),
 (
  GENERIC_SLI2, 0),
 (
  GENERIC_SLI3, 0),
 (
  GENERIC_SLI4, 0),
 (
  GENERIC_SLI5, 0),
 (
  GENERIC_SLI6, 0),
 (
  GENERIC_SLI7, 0),
 (
  GENERIC_SLI8, 0))
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
   b'BANK1': -1, 
   b'BANK2': -1, 
   b'BANK3': -1, 
   b'BANK4': -1, 
   b'BANK5': -1, 
   b'BANK6': -1, 
   b'BANK7': -1, 
   b'BANK8': -1}
PAD_TRANSLATION = (
 (0, 0, 67, 1),
 (1, 0, 69, 1),
 (2, 0, 71, 1),
 (3, 0, 72, 1),
 (0, 1, 60, 1),
 (1, 1, 62, 1),
 (2, 1, 64, 1),
 (3, 1, 65, 1),
 (0, 2, 67, 0),
 (1, 2, 69, 0),
 (2, 2, 71, 0),
 (3, 2, 72, 0),
 (0, 3, 60, 0),
 (1, 3, 62, 0),
 (2, 3, 64, 0),
 (3, 3, 65, 0))
CONTROLLER_DESCRIPTION = {b'INPUTPORT': b'Akai MPD32', 
   b'OUTPUTPORT': b'Akai MPD32', 
   b'CHANNEL': 0, 
   b'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {b'NUMSENDS': 2, 
   b'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 
   b'MASTERVOLUME': -1}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MPD32/config.pyc
