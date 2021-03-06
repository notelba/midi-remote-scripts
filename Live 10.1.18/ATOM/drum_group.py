# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\drum_group.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from .note_pad import NotePadMixin
COMPLETE_QUADRANTS_RANGE = xrange(4, 116)
MAX_QUADRANT_INDEX = 7
NUM_PADS = 16
PADS_PER_ROW = 4

class DrumGroupComponent(NotePadMixin, DrumGroupComponentBase):

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        color = self._color_for_pad(pad) if liveobj_valid(pad) else b'DrumGroup.PadEmpty'
        if color == b'DrumGroup.PadFilled':
            button_row, _ = button.coordinate
            button_index = (self.matrix.height - button_row - 1) * PADS_PER_ROW
            pad_row_start_note = self._drum_group_device.visible_drum_pads[button_index].note
            pad_quadrant = MAX_QUADRANT_INDEX
            if pad_row_start_note in COMPLETE_QUADRANTS_RANGE:
                pad_quadrant = (pad_row_start_note - 1) / NUM_PADS
            color = (b'DrumGroup.PadQuadrant{}').format(pad_quadrant)
        button.color = color
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/drum_group.pyc
