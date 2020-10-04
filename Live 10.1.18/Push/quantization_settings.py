# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\quantization_settings.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.control import TextDisplayControl
from pushbase.quantization_component import QuantizationSettingsComponent as QuantizationSettingsComponentBase, QUANTIZATION_NAMES, quantize_amount_to_string

class QuantizationSettingsComponent(QuantizationSettingsComponentBase):
    display_line1 = TextDisplayControl(segments=('', '', '', '', '', '', '', ''))
    display_line2 = TextDisplayControl(segments=('Swing', 'Quantize', 'Quantize', '',
                                                 '', '', '', 'Record'))
    display_line3 = TextDisplayControl(segments=('Amount', 'To', 'Amount', '', '',
                                                 '', '', 'Quantize'))
    display_line4 = TextDisplayControl(segments=('', '', '', '', '', '', '', ''))

    def __init__(self, *a, **k):
        super(QuantizationSettingsComponent, self).__init__(*a, **k)
        self._update_swing_amount_display()
        self._update_quantize_to_display()
        self._update_quantize_amount_display()
        self._update_record_quantization_display()
        self.__on_swing_amount_changed.subject = self.song
        self.__on_record_quantization_index_changed.subject = self
        self.__on_record_quantization_enabled_changed.subject = self
        self.__on_quantize_to_index_changed.subject = self
        self.__on_quantize_amount_changed.subject = self

    def _update_swing_amount_display(self):
        self.display_line1[0] = str(int(self.song.swing_amount * 200.0)) + b'%'

    def _update_record_quantization_display(self):
        record_quantization_on = self.record_quantization_toggle_button.is_toggled
        self.display_line1[-1] = QUANTIZATION_NAMES[self.record_quantization_index]
        self.display_line4[-1] = b'[  On  ]' if record_quantization_on else b'[  Off ]'

    def _update_quantize_to_display(self):
        self.display_line1[1] = QUANTIZATION_NAMES[self.quantize_to_index]

    def _update_quantize_amount_display(self):
        self.display_line1[2] = quantize_amount_to_string(self.quantize_amount)

    @listens(b'quantize_to_index')
    def __on_quantize_to_index_changed(self, _):
        self._update_quantize_to_display()

    @listens(b'quantize_amount')
    def __on_quantize_amount_changed(self, _):
        self._update_quantize_amount_display()

    @listens(b'swing_amount')
    def __on_swing_amount_changed(self):
        self._update_swing_amount_display()

    @listens(b'record_quantization_index')
    def __on_record_quantization_index_changed(self, _):
        self._update_record_quantization_display()

    @listens(b'record_quantization_enabled')
    def __on_record_quantization_enabled_changed(self, _):
        self._update_record_quantization_display()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push/quantization_settings.pyc
