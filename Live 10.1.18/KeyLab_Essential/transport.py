# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\transport.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ToggleComponent, TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl

class TransportComponent(TransportComponentBase):
    play_button = ButtonControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._punch_in_toggle = ToggleComponent(b'punch_in', self.song, parent=self)
        self._punch_out_toggle = ToggleComponent(b'punch_out', self.song, parent=self)

    def set_play_button(self, button):
        self.play_button.set_control_element(button)
        self._update_play_button_color()

    def _update_button_states(self):
        self._update_play_button_color()
        self._update_stop_button_color()

    def _update_play_button_color(self):
        self.play_button.color = b'Transport.PlayOn' if self.song.is_playing else b'Transport.PlayOff'

    def _update_stop_button_color(self):
        self.stop_button.color = b'Transport.StopOff' if self.song.is_playing else b'Transport.StopOn'

    @play_button.pressed
    def play_button(self, _):
        if not self.song.is_playing:
            self.song.is_playing = True

    def _ffwd_value(self, value):
        super(TransportComponent, self)._ffwd_value(value)
        self._ffwd_button.set_light(b'DefaultButton.On' if value else b'DefaultButton.Off')

    def _rwd_value(self, value):
        super(TransportComponent, self)._rwd_value(value)
        self._rwd_button.set_light(b'DefaultButton.On' if value else b'DefaultButton.Off')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_Essential/transport.pyc
