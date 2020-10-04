# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\drum_group_component.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from pushbase.drum_group_component import DrumGroupComponent as DrumGroupComponentBase

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, selector=None, *a, **k):
        super(DrumGroupComponent, self).__init__(*a, **k)
        self._selector = selector

    def select_drum_pad(self, drum_pad):
        self._selector.on_select_drum_pad(drum_pad)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push/drum_group_component.pyc
