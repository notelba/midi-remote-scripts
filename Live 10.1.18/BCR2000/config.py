# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BCR2000\config.py
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
VOLUME_CONTROLS = (97, 98, 99, 100, 101, 102, 103, 104)
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
   b'BANK1': GENERIC_PAD1, 
   b'BANK2': GENERIC_PAD2, 
   b'BANK3': GENERIC_PAD3, 
   b'BANK4': GENERIC_PAD4, 
   b'BANK5': GENERIC_PAD5, 
   b'BANK6': GENERIC_PAD6, 
   b'BANK7': GENERIC_PAD7, 
   b'BANK8': GENERIC_PAD8}
CONTROLLER_DESCRIPTION = {b'INPUTPORT': b'BCR2000', b'OUTPUTPORT': b'BCR2000', b'CHANNEL': 0}
MIXER_OPTIONS = {b'NUMSENDS': 2, 
   b'SEND1': GENERIC_SLIDERS, 
   b'SEND2': (89, 90, 91, 92, 93, 94, 95, 96), 
   b'MASTERVOLUME': -1}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/BCR2000/config.pyc
