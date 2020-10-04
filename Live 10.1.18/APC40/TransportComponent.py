# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40\TransportComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Control import ButtonControl
from _Framework.TransportComponent import TransportComponent as TransportComponentBase
from _Framework.SubjectSlot import subject_slot

class TransportComponent(TransportComponentBase):
    """ TransportComponent that only uses certain buttons if a shift button is pressed """
    rec_quantization_button = ButtonControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._last_quant_value = Live.Song.RecordingQuantization.rec_q_eight
        self._on_quantization_changed.subject = self.song()
        self._update_quantization_state()
        self.set_quant_toggle_button = self.rec_quantization_button.set_control_element

    @rec_quantization_button.pressed
    def rec_quantization_button(self, value):
        assert self._last_quant_value != Live.Song.RecordingQuantization.rec_q_no_q
        quant_value = self.song().midi_recording_quantization
        if quant_value != Live.Song.RecordingQuantization.rec_q_no_q:
            self._last_quant_value = quant_value
            self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q
        else:
            self.song().midi_recording_quantization = self._last_quant_value

    @subject_slot(b'midi_recording_quantization')
    def _on_quantization_changed(self):
        if self.is_enabled():
            self._update_quantization_state()

    def _update_quantization_state(self):
        quant_value = self.song().midi_recording_quantization
        quant_on = quant_value != Live.Song.RecordingQuantization.rec_q_no_q
        if quant_on:
            self._last_quant_value = quant_value
        self.rec_quantization_button.color = b'DefaultButton.On' if quant_on else b'DefaultButton.Off'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC40/TransportComponent.pyc
