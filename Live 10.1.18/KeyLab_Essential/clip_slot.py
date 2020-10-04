# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\clip_slot.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase

class ClipSlotComponent(ClipSlotComponentBase):

    def __init__(self, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._led = None
        return

    def set_led(self, led):
        self._led = led

    def update(self):
        super(ClipSlotComponent, self).update()
        self._update_led()

    def _update_launch_button_color(self):
        self._update_led()

    def _update_led(self):
        if self.is_enabled() and self._led != None:
            value_to_send = self._empty_slot_color
            if liveobj_valid(self._clip_slot):
                track = self._clip_slot.canonical_parent
                slot_or_clip = self._clip_slot.clip if self.has_clip() else self._clip_slot
                value_to_send = self._led_feedback_value(track, slot_or_clip)
            self._led.set_light(value_to_send)
        return

    def _led_feedback_value(self, track, slot_or_clip):
        if self.has_clip():
            if slot_or_clip.is_triggered:
                if slot_or_clip.will_record_on_start:
                    return self._triggered_to_record_color
                return self._triggered_to_play_color
            else:
                if slot_or_clip.is_playing:
                    if slot_or_clip.is_recording:
                        return self._recording_color
                    return self._started_value
                return self._stopped_value

        return self._empty_slot_color
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_Essential/clip_slot.pyc
