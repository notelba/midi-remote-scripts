# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\DummySkin.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.Skin import Skin
from DefaultColors import DefaultColors

class Colors:
    """ Skin to use for buttons with no LEDs. """

    class DefaultButton:
        On = DefaultColors.ON
        Off = DefaultColors.OFF
        Disabled = DefaultColors.OFF

    class ColorChoices:
        OFF = DefaultColors.OFF
        ON = DefaultColors.ON


def make_default_skin():
    return Skin(Colors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/DummySkin.pyc
