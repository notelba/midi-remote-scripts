# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab\DisplayElement.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

class DisplayElement(PhysicalDisplayElement):
    _ascii_translations = {b'\x00': 0, 
       b' ': 32, 
       b'%': 37, 
       b'1': 49, 
       b'2': 50, 
       b'3': 51, 
       b'4': 52, 
       b'5': 53, 
       b'6': 54, 
       b'7': 55, 
       b'8': 56, 
       b'9': 57, 
       b':': 58, 
       b'?': 63, 
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
       b'z': 122}

    def _build_display_message(self, display):
        message_string = display.display_string
        first_segment = display._logical_segments[0]
        return chain(first_segment.position_identifier(), self._translate_string(message_string))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab/DisplayElement.pyc
