# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipCreator.py
# Compiled at: 2017-03-07 13:28:52
import Live
_Q = Live.Song.Quantization
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from ShowMessageMixin import ShowMessageMixin
MAX_NUM_BARS = 32
BAR_RANGE = xrange(1, MAX_NUM_BARS + 1)
ABS_BAR_OPTS = (0, 1, 2, 4, 8, 16, 24, 32)
ABS_SCALE_FACTOR = 16

class ClipCreator(ControlSurfaceComponent, ShowMessageMixin):
    """ Component for determining fixed recording length as well as creating fixed
    length clips. """
    __subject_events__ = ('fixed_length_enabled', 'fixed_length')

    def __init__(self, name='Clip_Creator', default_num_bars=2, default_state=False, is_private=True, *a, **k):
        super(ClipCreator, self).__init__(name=name, *a, **k)
        self.is_private = bool(is_private)
        self._num_bars = default_num_bars
        self._fixed_length_enabled = bool(default_state)
        self._absolute_fixed_length_control = None
        self._last_absolute_value = -1
        self._allow_length_change_to_enable = True
        return

    def disconnect(self):
        super(ClipCreator, self).disconnect()
        self._absolute_fixed_length_control = None
        return

    def create_clip(self, slot, launch=True):
        """ Creates and (optionally) launches a MIDI clip in the given slot that will
        be the set fixed length. """
        assert slot.clip is None and slot.canonical_parent.has_midi_input
        slot.create_clip(self.fixed_length)
        if slot.clip:
            track = slot.canonical_parent
            slot.clip.name = '%s %s' % (list(track.clip_slots).index(slot) + 1, track.name)
        if launch:
            slot.fire(force_legato=True, launch_quantization=_Q.q_no_q)
        return

    def set_absolute_fixed_length_control(self, control):
        """ Sets the absolute control to use for adjusting and enabling/disabling
        fixed length. """
        self._last_absolute_value = -1
        self._on_absolute_fixed_length_control_value.subject = control

    def set_allow_length_change_to_enable(self, allow):
        """ Sets whether or not changing fixed length will enable fixed length if it
        isn't already enabled. """
        self._allow_length_change_to_enable = allow

    def _get_num_bars(self):
        return self._num_bars

    def _set_num_bars(self, num_bars):
        """ Sets fixed length to the given number of bars.  This is needed when setting
        fixed length in alternate ways as _get_fixed_length doesn't return num_bars. """
        self._set_fixed_length(num_bars)

    num_bars = property(_get_num_bars, _set_num_bars)

    def _get_fixed_length(self):
        return 4.0 / self.song().signature_denominator * self.song().signature_numerator * self._num_bars

    def _set_fixed_length(self, num_bars):
        """ Sets fixed length to the given number of bars
        (in range of 1 - 32 inclusive). """
        assert num_bars in BAR_RANGE
        self._num_bars = num_bars
        self.notify_fixed_length()
        if not self.fixed_length_enabled and self._allow_length_change_to_enable:
            self.fixed_length_enabled = True
        else:
            self._show_fixed_length()

    fixed_length = property(_get_fixed_length, _set_fixed_length)

    def _get_fixed_length_enabled(self):
        return self._fixed_length_enabled

    def _set_fixed_length_enabled(self, value):
        self._fixed_length_enabled = bool(value)
        self.notify_fixed_length_enabled()
        self._show_fixed_length()

    fixed_length_enabled = property(_get_fixed_length_enabled, _set_fixed_length_enabled)

    def _show_fixed_length(self):
        """ Displays the current fixed recording length/state in the status bar. """
        if self.fixed_length_enabled:
            tag = ' Bars' if self._num_bars > 1 else ' Bar'
            self.component_message('Fixed Length', str(self._num_bars) + tag)
        else:
            self.component_message('Fixed Length', 'Off')

    @subject_slot('value')
    def _on_absolute_fixed_length_control_value(self, value):
        scaled_value = value / ABS_SCALE_FACTOR
        if scaled_value != self._last_absolute_value:
            self._last_absolute_value = scaled_value
            if scaled_value:
                self.fixed_length = ABS_BAR_OPTS[scaled_value]
            elif self._fixed_length_enabled:
                self.fixed_length_enabled = False
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipCreator.pyc
