# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\sysex.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
SYSEX_MSG_HEADER = (240, 71, 0)
SYSEX_END_BYTE = 247
MPC_X_PRODUCT_ID = 58
MPC_LIVE_PRODUCT_ID = 59
FORCE_PRODUCT_ID = 64
SUPPORTED_PRODUCT_IDS = (MPC_LIVE_PRODUCT_ID, MPC_X_PRODUCT_ID, FORCE_PRODUCT_ID)
BROADCAST_ID = 127
PING_MSG_TYPE = 0
PONG_MSG_TYPE = 1
TEXT_MSG_TYPE = 16
COLOR_MSG_TYPE = 17
PING_MSG = SYSEX_MSG_HEADER + (BROADCAST_ID, PING_MSG_TYPE, SYSEX_END_BYTE)
INNER_MESSAGE_MAX_LENGTH = 251
NUM_MSG_IDENTIFYING_BYTES = 3
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/sysex.pyc
