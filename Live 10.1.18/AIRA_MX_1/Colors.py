# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AIRA_MX_1\Colors.py
# Compiled at: 2020-07-31 16:19:16
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import Color
BLINK_LED_CHANNEL = 14

class Blink(Color):

    def draw(self, interface):
        interface.send_value(self.midi_value)
        interface.send_value(0, channel=BLINK_LED_CHANNEL)


class Rgb:
    BLACK = Color(0)
    RED = Color(5)
    RED_BLINK = Blink(5)
    GREEN_HALF = Color(20)
    GREEN = Color(21)
    GREEN_BLINK = Blink(21)
    BLUE_HALF = Color(44)
    BLUE = Color(45)
    BLUE_BLINK = Blink(45)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/AIRA_MX_1/Colors.pyc
