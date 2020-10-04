# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipQuantizeComponent.py
# Compiled at: 2017-05-29 15:43:11
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from ShowMessageMixin import ShowMessageMixin
from consts import RECORD_QUANTIZE_RATES, RECORD_QUANTIZE_NAMES, DEFAULT_CLIP_QUANTIZE_INDEX, MIDI_RANGE

class ClipQuantizeComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ ClipQuantizeComponent is the base component for a class that can control the
    quantization rate and amount to use when quantizing clips. """
    __subject_events__ = ('quantize_to', 'quantize_amount')

    def __init__(self, name='Clip_Quantization_Control', *a, **k):
        super(ClipQuantizeComponent, self).__init__(name, *a, **k)
        self._quantize_to = DEFAULT_CLIP_QUANTIZE_INDEX
        self._quantize_amount = 1.0

    def quantize_clip(self, clip):
        """ Quantizes the given clip with the current settings. """
        if clip:
            clip.quantize(self.quantize_to + 1, self.quantize_amount)
            self.component_message('Quantized To', self._quantize_info())

    def quantize_pitch(self, clip, pitch):
        """ Quantizes the given pitch in the given MIDI clip with the
        current settings. """
        assert pitch in MIDI_RANGE
        if clip and clip.is_midi_clip:
            clip.quantize_pitch(pitch, self.quantize_to + 1, self.quantize_amount)
            self.component_message('Quantized To', self._quantize_info())

    @property
    def quantize_rate(self):
        """ The rate to quantize to. """
        return RECORD_QUANTIZE_RATES[self._quantize_to]

    def _get_quantize_to(self):
        """ The index of the rate (within RECORD_QUANTIZE_RATES) to quantize to. """
        return self._quantize_to

    def _set_quantize_to(self, qntz_index):
        """ Sets the quantization index to quantize to, notifies listeners and shows
        info in status bar. """
        assert qntz_index in xrange(len(RECORD_QUANTIZE_RATES))
        if self.is_enabled():
            self._quantize_to = qntz_index
            self.notify_quantize_to()
            self._show_status_bar_info()

    quantize_to = property(_get_quantize_to, _set_quantize_to)

    def _get_quantize_amount(self):
        """ The quantization strength. """
        return self._quantize_amount

    def _set_quantize_amount(self, amount):
        """ Sets the quantization amount/strength to use, notifies listeners and shows
        info in status bar. """
        assert 0.0 <= amount <= 1.0
        if self.is_enabled():
            self._quantize_amount = amount
            self.notify_quantize_amount()
            self._show_status_bar_info()

    quantize_amount = property(_get_quantize_amount, _set_quantize_amount)

    def _show_status_bar_info(self):
        self.component_message('Clip Quantization', self._quantize_info())

    def _quantize_info(self):
        return ('{0} at {1}%').format(RECORD_QUANTIZE_NAMES[self._quantize_to], int(self._quantize_amount * 100))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipQuantizeComponent.pyc
