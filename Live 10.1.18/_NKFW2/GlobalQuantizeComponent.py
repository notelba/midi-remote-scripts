# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\GlobalQuantizeComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from SpecialControl import RadioButtonGroup
from consts import NOTE_RATE_GLOBAL_QUANTIZE_RATES, NO_TRIPLET_NOTE_RATE_GLOBAL_QUANTIZE_RATES
NUM_RATES = len(NOTE_RATE_GLOBAL_QUANTIZE_RATES)

class NoteRateGlobalQuantizeComponent(ControlSurfaceComponent):
    """ NoteRateGlobalQuantizeComponent provides access to the global quantize note rates.
    If less than 5 buttons are used, triplet rates won't be available. """

    def __init__(self, name='Global_Quantization_Control', num_buttons=NUM_RATES, *a, **k):
        super(NoteRateGlobalQuantizeComponent, self).__init__(name=name, *a, **k)
        no_triplets = num_buttons < 5
        self._rates = NO_TRIPLET_NOTE_RATE_GLOBAL_QUANTIZE_RATES if no_triplets else NOTE_RATE_GLOBAL_QUANTIZE_RATES
        self._quantize_buttons = RadioButtonGroup(num_buttons, 0, checked_color='GlobalQuantize.Selected', unchecked_color='GlobalQuantize.NotSelected')
        self._on_quantize_button_value.subject = self._quantize_buttons
        self._on_global_quantize_changed.subject = self.song()
        self._on_global_quantize_changed()

    def set_quantize_buttons(self, buttons):
        """ Sets the group of buttons to use for selecting quantization. """
        self._quantize_buttons.set_buttons(buttons)

    @subject_slot('checked_index')
    def _on_quantize_button_value(self, index):
        if self.is_enabled():
            self.song().clip_trigger_quantization = self._rates[index]

    def update(self):
        super(NoteRateGlobalQuantizeComponent, self).update()
        self._on_global_quantize_changed()

    @subject_slot('clip_trigger_quantization')
    def _on_global_quantize_changed(self):
        if self.is_enabled():
            rate = self.song().clip_trigger_quantization
            if rate in self._rates:
                self._quantize_buttons.set_checked_index(self._rates.index(rate))
            else:
                self._quantize_buttons.set_checked_index(-1)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/GlobalQuantizeComponent.pyc
