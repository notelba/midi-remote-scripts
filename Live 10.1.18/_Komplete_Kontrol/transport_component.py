# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\transport_component.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.components import ToggleComponent
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class TransportComponent(TransportComponentBase):
    play_button = ButtonControl(color=b'Transport.PlayOff')
    jump_encoder = EncoderControl()
    loop_start_encoder = EncoderControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self.__on_signature_numerator_changed.subject = self.song
        self.__on_signature_denominator_changed.subject = self.song
        self._session_record_toggle = ToggleComponent(b'session_record', self.song, parent=self)
        self._calculate_distance_to_move()

    def set_play_button(self, button):
        self.play_button.set_control_element(button)

    def set_session_record_button(self, button):
        self._session_record_toggle.set_toggle_button(button)

    @play_button.pressed
    def play_button(self, _):
        self.song.start_playing()

    @jump_encoder.value
    def jump_encoder(self, value, _):
        self.song.jump_by(value * self._distance_to_move)

    @loop_start_encoder.value
    def loop_start_encoder(self, value, _):
        self.song.loop_start = max(0.0, self.song.loop_start + value * self._distance_to_move)

    @listens(b'signature_numerator')
    def __on_signature_numerator_changed(self):
        self._calculate_distance_to_move()

    @listens(b'signature_denominator')
    def __on_signature_denominator_changed(self):
        self._calculate_distance_to_move()

    def _calculate_distance_to_move(self):
        self._distance_to_move = 4.0 / self.song.signature_denominator * self.song.signature_numerator * 64

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self.play_button.color = b'Transport.PlayOn' if self.song.is_playing else b'Transport.PlayOff'

    def _update_stop_button_color(self):
        self.stop_button.color = b'Transport.PlayOff' if self.song.is_playing else b'Transport.PlayOn'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Komplete_Kontrol/transport_component.pyc
