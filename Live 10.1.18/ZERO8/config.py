# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ZERO8\config.py
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
   b'BANK1': 80, 
   b'BANK2': 81, 
   b'BANK3': 82, 
   b'BANK4': 83, 
   b'BANK5': 84, 
   b'BANK6': 85, 
   b'BANK7': 86, 
   b'BANK8': 87}
CONTROLLER_DESCRIPTION = {b'INPUTPORT': b'ZERO8 MIDI IN 2', 
   b'OUTPUTPORT': b'ZERO8 MIDI OUT 2', 
   b'CHANNEL': 0}
MIXER_OPTIONS = {b'NUMSENDS': 2, 
   b'SEND1': (
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)), 
   b'SEND2': (
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)), 
   b'PANS': (
           (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7)), 
   b'MASTERVOLUME': -1}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ZERO8/config.pyc
