# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\grid_resolution.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import listenable_property, product
from ableton.v2.control_surface.control import control_list, ControlManager, RadioButtonControl
GridQuantization = Live.Clip.GridQuantization
QUANTIZATION_FACTOR = 24
QUANTIZATION_LIST = [
 2.0,
 3.0,
 4.0,
 6.0,
 8.0,
 12.0,
 16.0,
 24.0]
CLIP_VIEW_GRID_LIST = tuple(product([
 GridQuantization.g_thirtysecond,
 GridQuantization.g_sixteenth,
 GridQuantization.g_eighth,
 GridQuantization.g_quarter], [
 True, False]))
CLIP_LENGTH_LIST = [
 2.0,
 4.0,
 4.0,
 8.0,
 8.0,
 16.0,
 16.0,
 32.0]
DEFAULT_INDEX = 3

class GridResolution(ControlManager):
    quantization_buttons = control_list(RadioButtonControl, checked_color=b'NoteEditor.QuantizationSelected', unchecked_color=b'NoteEditor.QuantizationUnselected', control_count=8)
    index = listenable_property.managed(DEFAULT_INDEX)

    def __init__(self, *a, **k):
        super(GridResolution, self).__init__(*a, **k)
        self.index = DEFAULT_INDEX
        self.quantization_buttons[self.index].is_checked = True

    @property
    def step_length(self):
        return QUANTIZATION_LIST[self.index] / QUANTIZATION_FACTOR

    @property
    def clip_grid(self):
        return CLIP_VIEW_GRID_LIST[self.index]

    @property
    def clip_length(self):
        return CLIP_LENGTH_LIST[self.index]

    @quantization_buttons.checked
    def quantization_buttons(self, button):
        self.index = button.index
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/pushbase/grid_resolution.pyc
