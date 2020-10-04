# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_FA\skin.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import Color
from ableton.v2.control_surface import Skin

class Colors:

    class DefaultButton:
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)

    class Transport:
        PlayOn = Color(127)
        PlayOff = Color(0)

    class Recording:
        On = Color(127)
        Off = Color(0)


def make_default_skin():
    return Skin(Colors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Roland_FA/skin.pyc
