# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\LaunchQuantizeComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from SpecialControl import RadioButtonGroup
from ShowMessageMixin import ShowMessageMixin
from consts import LAUNCH_QUANTIZE_RATES, NO_TRIPLET_LAUNCH_QUANTIZE_RATES, LAUNCH_QUANTIZE_NAMES, NO_TRIPLET_LAUNCH_QUANTIZE_NAMES, DEFAULT_LAUNCH_QUANTIZE_INDEX, NO_TRIPLET_DEFAULT_LAUNCH_QUANTIZE_INDEX
NUM_RATES = len(LAUNCH_QUANTIZE_RATES)

class LaunchQuantizeComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ LaunchQuantizeComponent determines the quantization rate to use for
    launching clips. A standard implementation (StandardLaunchQuantizeComponent) is
    provided in this module. """
    __subject_events__ = ('quantization', )

    def __init__(self, name='Launch_Quantization_Control', no_triplets=False, *a, **k):
        super(LaunchQuantizeComponent, self).__init__(name, *a, **k)
        self._rates = NO_TRIPLET_LAUNCH_QUANTIZE_RATES if no_triplets else LAUNCH_QUANTIZE_RATES
        self._names = NO_TRIPLET_LAUNCH_QUANTIZE_NAMES if no_triplets else LAUNCH_QUANTIZE_NAMES
        self._default_index = NO_TRIPLET_DEFAULT_LAUNCH_QUANTIZE_INDEX if no_triplets else DEFAULT_LAUNCH_QUANTIZE_INDEX
        self._quantization = self._rates[self._default_index]

    def _get_quantization(self):
        return self._quantization

    def _set_quantization(self, qntz_index):
        assert qntz_index in xrange(len(self._rates))
        if self.is_enabled():
            self._quantization = self._rates[qntz_index]
            self.notify_quantization(self._quantization)
            self.component_message('Launch Quantization', self._names[qntz_index])

    quantization = property(_get_quantization, _set_quantization)


class StandardLaunchQuantizeComponent(LaunchQuantizeComponent):
    """ StandardLaunchQuantizeComponent is a LaunchQuantizeComponent set up to be
    controlled by a group of buttons.  If less than 5 buttons are used, triplet
    rates won't be available. """

    def __init__(self, num_buttons=NUM_RATES, *a, **k):
        no_triplets = num_buttons < 5
        super(StandardLaunchQuantizeComponent, self).__init__(no_triplets=no_triplets, *a, **k)
        self._quantize_buttons = RadioButtonGroup(num_buttons, self._default_index, checked_color='LaunchQuantize.Selected', unchecked_color='LaunchQuantize.NotSelected')
        self._on_quantize_button_value.subject = self._quantize_buttons

    def set_quantize_buttons(self, buttons):
        self._quantize_buttons.set_buttons(buttons)

    def update(self):
        super(StandardLaunchQuantizeComponent, self).update()
        self._quantize_buttons.update()

    @subject_slot('checked_index')
    def _on_quantize_button_value(self, index):
        if self.is_enabled():
            self.quantization = index
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/LaunchQuantizeComponent.pyc
