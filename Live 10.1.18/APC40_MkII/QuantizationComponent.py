# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40_MkII\QuantizationComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Control import RadioButtonControl, control_list
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
AVAILABLE_QUANTIZATION = [
 Live.Song.Quantization.q_no_q,
 Live.Song.Quantization.q_8_bars,
 Live.Song.Quantization.q_4_bars,
 Live.Song.Quantization.q_2_bars,
 Live.Song.Quantization.q_bar,
 Live.Song.Quantization.q_quarter,
 Live.Song.Quantization.q_eight,
 Live.Song.Quantization.q_sixtenth]

class QuantizationComponent(ControlSurfaceComponent):
    quantization_buttons = control_list(RadioButtonControl)

    def __init__(self, *a, **k):
        super(QuantizationComponent, self).__init__(*a, **k)
        self.quantization_buttons.control_count = len(AVAILABLE_QUANTIZATION) + 1
        self._on_clip_trigger_quantization_changed.subject = self.song()
        self._on_clip_trigger_quantization_changed()

    @quantization_buttons.checked
    def quantization_buttons(self, button):
        if 0 <= button.index < len(AVAILABLE_QUANTIZATION):
            quantization = AVAILABLE_QUANTIZATION[button.index]
            if quantization != self.song().clip_trigger_quantization:
                self.song().clip_trigger_quantization = quantization

    @subject_slot(b'clip_trigger_quantization')
    def _on_clip_trigger_quantization_changed(self):
        self._get_button(self.song().clip_trigger_quantization).is_checked = True

    def _get_button(self, quantization):
        if quantization in AVAILABLE_QUANTIZATION:
            return self.quantization_buttons[AVAILABLE_QUANTIZATION.index(quantization)]
        return self.quantization_buttons[(-1)]
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC40_MkII/QuantizationComponent.pyc
