# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\color_sysex_element.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import nop
from ableton.v2.control_surface.elements import ColorSysexElement as ColorSysexElementBase

class ColorSysexElement(ColorSysexElementBase):

    class ProxiedInterface(ColorSysexElementBase.ProxiedInterface):
        set_light = nop
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/SL_MkIII/color_sysex_element.pyc
