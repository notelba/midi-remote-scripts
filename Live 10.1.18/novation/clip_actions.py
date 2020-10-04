# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\clip_actions.py
# Compiled at: 2020-06-11 14:05:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import duplicate_clip_loop
from ableton.v2.control_surface.components import ClipActionsComponent as ClipActionsComponentBase
from .blinking_button import BlinkingButtonControl

class ClipActionsComponent(ClipActionsComponentBase):
    quantization_component = None
    quantize_button = BlinkingButtonControl(color=b'Action.Quantize', blink_on_color=b'Action.QuantizePressed', blink_off_color=b'Action.Quantize')
    double_loop_button = BlinkingButtonControl(color=b'Action.Double', blink_on_color=b'Action.DoublePressed', blink_off_color=b'Action.Double')
    __events__ = ('can_perform_clip_actions', )

    def __init__(self, *a, **k):
        super(ClipActionsComponent, self).__init__(*a, **k)
        self.delete_button.color = b'Action.Delete'
        self.delete_button.pressed_color = b'Action.DeletePressed'
        self.duplicate_button.color = b'Action.Duplicate'
        self.duplicate_button.pressed_color = b'Action.DuplicatePressed'

    @quantize_button.pressed
    def quantize_button(self, _):
        if self.quantization_component:
            self.quantization_component.quantize_clip(self.clip_slot.clip)
            self.quantize_button.start_blinking()

    @double_loop_button.pressed
    def double_loop_button(self, _):
        duplicate_clip_loop(self.clip_slot.clip)
        self.double_loop_button.start_blinking()

    def delete_pitch(self, pitch):
        clip = self.clip_slot.clip
        loop_length = clip.loop_end - clip.loop_start
        clip.remove_notes(clip.loop_start, pitch, loop_length, 1)

    def delete_clip(self):
        self.clip_slot.delete_clip()

    def _update_action_buttons(self):
        super(ClipActionsComponent, self)._update_action_buttons()
        can_perform_clip_action = self._can_perform_clip_action()
        self.quantize_button.enabled = can_perform_clip_action
        self.notify_can_perform_clip_actions(can_perform_clip_action)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/clip_actions.pyc
