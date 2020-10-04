# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\DefaultColors.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ButtonElement import Color

class SlowBlinkColor(Color):
    """ A Color that will blink slowly for use with BlinkingButtonElement. """

    def draw(self, interface):
        interface.send_value(self.midi_value)
        interface.blink(self.midi_value, slow_blink=True)


class FastBlinkColor(Color):
    """ A Color that will blink fast for use with BlinkingButtonElement. """

    def draw(self, interface):
        interface.send_value(self.midi_value)
        interface.blink(self.midi_value, slow_blink=False)


class DefaultColors(object):
    """ Colors to use for buttons with single color or no LED. """
    ON = Color(127)
    FAST_BLINK = FastBlinkColor(127)
    SLOW_BLINK = SlowBlinkColor(127)
    OFF = Color(0)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/DefaultColors.pyc
