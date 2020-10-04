# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\mixer.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import izip_longest
from ableton.v2.base import clamp, listens, liveobj_valid, forward_property
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v2.control_surface.control import ButtonControl, SendValueControl
from .elements import MAX_NUM_SENDS

class MixerComponent(MixerComponentBase):
    num_sends_control = SendValueControl()
    master_button = ButtonControl()

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(*a, **k)
        self._last_selected_track = None
        self._last_track_offset = None
        self.__on_offsets_changed.subject = self._provider
        self.__on_offsets_changed(self._provider.track_offset, self._provider.scene_offset)
        return

    def __getattr__(self, name):
        if name.startswith(b'set_') and name.endswith(b's'):
            return partial(self._set_channel_strip_controls, name[4:-1])
        raise AttributeError

    def on_num_sends_changed(self):
        self.num_sends_control.value = clamp(self.num_sends, 0, MAX_NUM_SENDS)

    @property
    def max_track_offset(self):
        return max(0, len(self._provider.tracks_to_use()) - self._provider.num_tracks)

    def _on_selected_track_changed(self):
        selected_track = self.song.view.selected_track
        button_color = b'DefaultButton.On'
        if selected_track != self.song.master_track:
            self._last_selected_track = selected_track
            button_color = b'DefaultButton.Off'
        self.master_button.color = button_color

    @listens(b'offset')
    def __on_offsets_changed(self, track_offset, _):
        max_track_offset = self.max_track_offset
        if max_track_offset == 0 or track_offset < max_track_offset:
            self._last_track_offset = track_offset

    def set_send_controls(self, controls):
        self._send_controls = controls
        for strip, row in izip_longest(self._channel_strips, controls.rows() if controls else []):
            strip.set_send_controls(row)

    def set_send_value_displays(self, displays):
        for strip, row in izip_longest(self._channel_strips, displays.rows() if displays else []):
            strip.set_send_value_displays(row)

    def set_selected_track_mute_button(self, button):
        self._selected_strip.mpc_mute_button.set_control_element(button)

    set_selected_track_arm_button = forward_property(b'_selected_strip')(b'set_arm_button')
    set_selected_track_solo_button = forward_property(b'_selected_strip')(b'set_solo_button')

    def set_track_type_controls(self, controls):
        for strip, control in izip_longest(self._channel_strips, controls or []):
            strip.track_type_control.set_control_element(control)

    def _set_channel_strip_controls(self, name, controls):
        for strip, control in izip_longest(self._channel_strips, controls or []):
            set_method = getattr(strip, (b'set_{}').format(name), None)
            if not set_method:
                set_method = getattr(strip, name, None).set_control_element
            set_method(control)

        return

    def set_solo_mute_buttons(self, buttons):
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.solo_mute_button.set_control_element(button)

    @master_button.pressed
    def master_button_value(self, _button):
        master_track = self.song.master_track
        if self.song.view.selected_track != master_track:
            self.song.view.selected_track = master_track
        else:
            self.song.view.selected_track = self._last_selected_track if liveobj_valid(self._last_selected_track) else self.song.tracks[0]
        if self._provider.track_offset < self.max_track_offset:
            self._provider.track_offset = self.max_track_offset
        else:
            self._provider.track_offset = self._last_track_offset
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/mixer.pyc
