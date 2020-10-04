# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BLOCKS\button.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import in_range
from ableton.v2.control_surface.elements import ButtonElement as ButtonElementBase

class ButtonElement(ButtonElementBase):

    def set_light(self, value):
        if isinstance(value, int) and in_range(value, 0, 128):
            self.send_value(value)
        else:
            super(ButtonElement, self).set_light(value)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/BLOCKS/button.pyc
