# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Tranzport\consts.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
NOTE_OFF_STATUS = 128
NOTE_ON_STATUS = 144
CC_STATUS = 176
NUM_NOTES = 127
NUM_CC_NO = 127
NUM_CHANNELS = 15
NUM_PAGES = 4
PAGES_NAMES = (
 ('P', 'o', 's', 'i', 't', 'i', 'o', 'n', ' ', '&', ' ', 'T', 'e', 'm', 'p', 'o'),
 ('C', 'l', 'i', 'p', ' ', '&', ' ', 'T', 'e', 'm', 'p', 'o'),
 ('V', 'o', 'l', 'u', 'm', 'e', ' ', '&', ' ', 'P', 'a', 'n', 'n', 'i', 'n', 'g'),
 ('L', 'o', 'o', 'p', ' ', 'S', 'e', 't', 't', 'i', 'n', 'g', 's'),
 ('S', 'e', 'n', 'd', ' ', 'S', 'e', 't', 't', 'i', 'n', 'g', 's'))
TRANZ_NATIVE_MODE = (240, 0, 1, 64, 16, 1, 0, 247)
TRANZ_TRANS_SECTION = range(91, 96)
TRANZ_RWD = 91
TRANZ_FFWD = 92
TRANZ_STOP = 93
TRANZ_PLAY = 94
TRANZ_REC = 95
TRANZ_PREV_TRACK = 48
TRANZ_NEXT_TRACK = 49
TRANZ_ARM_TRACK = 0
TRANZ_MUTE_TRACK = 16
TRANZ_SOLO_TRACK = 8
TRANZ_ANY_SOLO = 115
TRANZ_TRACK_SECTION = (
 TRANZ_PREV_TRACK,
 TRANZ_NEXT_TRACK,
 TRANZ_ARM_TRACK,
 TRANZ_MUTE_TRACK,
 TRANZ_SOLO_TRACK,
 TRANZ_ANY_SOLO)
TRANZ_LOOP = 86
TRANZ_PUNCH_IN = 87
TRANZ_PUNCH_OUT = 88
TRANZ_PUNCH = 120
TRANZ_LOOP_SECTION = (TRANZ_LOOP, TRANZ_PUNCH_IN, TRANZ_PUNCH_OUT, TRANZ_PUNCH)
TRANZ_PREV_CUE = 84
TRANZ_ADD_CUE = 82
TRANZ_NEXT_CUE = 85
TRANZ_CUE_SECTION = (TRANZ_PREV_CUE, TRANZ_ADD_CUE, TRANZ_NEXT_CUE)
TRANZ_UNDO = 76
TRANZ_SHIFT = 121
TRANZ_DICT = {b'0': 48, 
   b'1': 49, 
   b'2': 50, 
   b'3': 51, 
   b'4': 52, 
   b'5': 53, 
   b'6': 54, 
   b'7': 55, 
   b'8': 56, 
   b'9': 57, 
   b'A': 65, 
   b'B': 66, 
   b'C': 67, 
   b'D': 68, 
   b'E': 69, 
   b'F': 70, 
   b'G': 71, 
   b'H': 72, 
   b'I': 73, 
   b'J': 74, 
   b'K': 75, 
   b'L': 76, 
   b'M': 77, 
   b'N': 78, 
   b'O': 79, 
   b'P': 80, 
   b'Q': 81, 
   b'R': 82, 
   b'S': 83, 
   b'T': 84, 
   b'U': 85, 
   b'V': 86, 
   b'W': 87, 
   b'X': 88, 
   b'Y': 89, 
   b'Z': 90, 
   b'a': 97, 
   b'b': 98, 
   b'c': 99, 
   b'd': 100, 
   b'e': 101, 
   b'f': 102, 
   b'g': 103, 
   b'h': 104, 
   b'i': 105, 
   b'j': 106, 
   b'k': 107, 
   b'l': 108, 
   b'm': 109, 
   b'n': 110, 
   b'o': 111, 
   b'p': 112, 
   b'q': 113, 
   b'r': 114, 
   b's': 115, 
   b't': 116, 
   b'u': 117, 
   b'v': 118, 
   b'w': 119, 
   b'x': 120, 
   b'y': 121, 
   b'z': 122, 
   b'@': 64, 
   b' ': 32, 
   b'.': 46, 
   b',': 44, 
   b':': 58, 
   b';': 59, 
   b'<': 60, 
   b'>': 62, 
   b'[': 91, 
   b']': 93, 
   b'_': 95, 
   b'-': 16, 
   b'|': 124, 
   b'&': 38}
SYSEX_START = (240, 0, 1, 64, 16, 0)
SYSEX_END = (247, )
CLEAR_LINE = (32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
              32, 32)
LED_ON = 127
LED_OFF = 0
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Tranzport/consts.pyc
