# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\skin.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import merge_skins, Skin
from ableton.v2.control_surface.elements import Color
from novation.colors import Rgb
from novation.skin import skin as base_skin

class Colors:

    class Mode:

        class Session:
            Launch = Color((Rgb.PALE_GREEN_HALF.midi_value, Rgb.WHITE_HALF.midi_value))
            Mixer = Color((Rgb.CREAM.midi_value, Rgb.WHITE_HALF.midi_value))
            Overview = Color((Rgb.BLUE.midi_value, Rgb.WHITE_HALF.midi_value))


skin = merge_skins(*(base_skin, Skin(Colors)))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_X/skin.pyc
