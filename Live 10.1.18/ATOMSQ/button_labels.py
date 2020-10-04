# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\button_labels.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import control_list
from .control import DisplayControl
BUTTON_LABELS_MAP = {b'song': ('Solo', 'Mute', 'Arm', 'Clip', 'Scene', 'Stop'), 
   b'instrument': ('-', '-', '-', '-', '-', '-'), 
   b'editor': ('Lock', '< Device', 'Device >', 'On/Off', '< Bank', 'Bank >'), 
   b'user': ('User 1', 'User 2', 'User 3', 'User 4', 'User 5', 'User 6')}

class ButtonLabelsComponent(Component):
    display_lines = control_list(DisplayControl, control_count=6)

    def show_button_labels_for_mode(self, mode_name):
        if mode_name in BUTTON_LABELS_MAP:
            for display, text in zip(self.display_lines, BUTTON_LABELS_MAP[mode_name]):
                display.message = text
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/button_labels.pyc
