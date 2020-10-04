# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\clip_actions.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface.components import ClipActionsComponent as ClipActionsComponentBase
from ableton.v2.control_surface.control import ButtonControl
from .control import SendReceiveValueControl
RecordingQ = Live.Song.RecordingQuantization

def is_valid_quantize_value(value):
    return RecordingQ.rec_q_quarter <= value <= RecordingQ.rec_q_thirtysecond


class ClipActionsComponent(ClipActionsComponentBase):
    quantization_value_control = SendReceiveValueControl()
    quantize_button = ButtonControl()
    quantize_color_control = ButtonControl()

    def __init__(self, *a, **k):
        super(ClipActionsComponent, self).__init__(*a, **k)
        self._quantization_value = RecordingQ.rec_q_sixtenth
        self.quantization_value_control.value = self._quantization_value - 1
        self.duplicate_button.pressed_color = b'Action.On'
        self.delete_button.pressed_color = b'Action.On'

    @quantization_value_control.value
    def quantizaton_value_control(self, value, _):
        self._quantization_value = value + 1

    @quantize_button.pressed
    def quantize_button(self, _):
        quantize_to = self._quantization_value
        if self._can_perform_clip_action() and is_valid_quantize_value(quantize_to):
            self.clip_slot.clip.quantize(quantize_to, 1.0)
        self._update_quantize_color_control()

    @quantize_button.released
    def quantize_button(self, _):
        self._update_quantize_color_control()

    def _update_action_buttons(self):
        super(ClipActionsComponent, self)._update_action_buttons()
        self._update_quantize_color_control()

    def _update_quantize_color_control(self):
        self.quantize_color_control.color = b'Action.QuantizeOn' if self.quantize_button.is_pressed and self._can_perform_clip_action() else b'Action.QuantizeOff'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/clip_actions.pyc
