# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launch_Control\SpecialSessionComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from _Framework.SessionComponent import SessionComponent

class SpecialSessionComponent(SessionComponent):

    def set_clip_launch_buttons(self, buttons):
        for i, button in izip_longest(xrange(self._num_tracks), buttons or []):
            scene = self.selected_scene()
            slot = scene.clip_slot(i)
            slot.set_launch_button(button)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launch_Control/SpecialSessionComponent.pyc
