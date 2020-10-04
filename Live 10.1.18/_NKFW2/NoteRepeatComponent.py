# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\NoteRepeatComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from SpecialControl import SpecialButtonControl, RadioButtonGroup
from PropertyControl import PropertyControl
from ControlUtils import set_group_button_lights
from ShowMessageMixin import ShowMessageMixin
from consts import RESOLUTIONS, NO_TRIPLET_RESOLUTIONS, RESOLUTION_NAMES, NO_TRIPLET_RESOLUTION_NAMES, DEFAULT_RESOLUTION_INDEX, NO_TRIPLET_DEFAULT_RESOLUTION_INDEX
NUM_RESOLUTIONS = len(RESOLUTIONS)

class NoteRepeatComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ NoteRepeatComponent handles enabling/disabling note repeat and controlling its
    rate and swing. This needs to be extended to add controls for controlling rate and
    swing. A standard implementation (StandardNoteRepeatComponent) is provided in this
    module. """
    __subject_events__ = ('repeat_enabled', 'rate', 'swing_amount')
    repeat_on_off_button = SpecialButtonControl(color='NoteRepeat.Off', on_color='NoteRepeat.On', disabled_color='NoteRepeat.Inactive')

    def __init__(self, name='Note_Repeat_Control', no_triplets=False, from_test=False, *a, **k):
        super(NoteRepeatComponent, self).__init__(name, *a, **k)
        self._resolutions = NO_TRIPLET_RESOLUTIONS if no_triplets else RESOLUTIONS
        self._resolution_names = NO_TRIPLET_RESOLUTION_NAMES if no_triplets else RESOLUTION_NAMES
        self._default_resolution = NO_TRIPLET_DEFAULT_RESOLUTION_INDEX if no_triplets else DEFAULT_RESOLUTION_INDEX
        self._repeat = None if from_test else self.canonical_parent._c_instance.note_repeat
        swing_transform = lambda x: '%s%%' % int(round(x * 200))
        self._swing_property = PropertyControl('swing_amount', self.song(), (0.0, 0.5), rel_thresh=2, quantized=False, display_name='Swing Amount', display_value_transform=swing_transform)
        self._last_recording_qntz = None
        self._on_swing_amount_changed.subject = self.song()
        self._tasks.add(self._set_defaults)
        return

    def disconnect(self):
        if self._last_recording_qntz is not None:
            self.song().midi_recording_quantization = self._last_recording_qntz
        super(NoteRepeatComponent, self).disconnect()
        self._swing_property.disconnect()
        self._resolutions = None
        self._resolution_names = None
        self._repeat = None
        return

    def set_swing_control(self, control):
        """ Sets the encoder to use for controlling swing amount. """
        self._swing_property.set_control(control)

    @property
    def repeat_enabled(self):
        """ Whether or not repeat is turned on. """
        return self._repeat.enabled

    def _get_rate(self):
        """ The note repeat rate. """
        return self._repeat.repeat_rate

    def _set_rate(self, rate_index):
        """ Sets note repeat rate if repeat is enabled, notifies listeners and shows info
        in status bar. """
        if not rate_index in xrange(len(self._resolutions)):
            raise AssertionError
            if self.is_enabled() and self._repeat.enabled:
                self._repeat.repeat_rate = self._resolutions[rate_index]
                self.notify_rate(self._repeat.repeat_rate)
                self._show_info()

    rate = property(_get_rate, _set_rate)

    def on_enabled_changed(self):
        """ Extends standard to refresh record quantization. """
        if self.canonical_parent:
            self.canonical_parent.schedule_message(1, self._refresh_record_quantization)
        super(NoteRepeatComponent, self).on_enabled_changed()

    @repeat_on_off_button.pressed
    def repeat_on_off_button(self, _):
        self._toggle_repeat_state()

    @repeat_on_off_button.released_delayed
    def repeat_on_off_button(self, _):
        self._toggle_repeat_state(True)

    @repeat_on_off_button.pressed_delayed
    def repeat_on_off_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    @repeat_on_off_button.released_immediately
    def repeat_on_off_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    def _toggle_repeat_state(self, is_release=False):
        """ Toggles note repeat rate, refreshes, record quantize, updates repeat button,
        notifies listeners and shows info in status bar. """
        if not is_release or self._repeat.enabled:
            self._repeat.enabled = not self._repeat.enabled
            self._refresh_record_quantization()
            self._update_repeat_button()
            self.notify_repeat_enabled(self._repeat.enabled)
            self.notify_rate(self._repeat.repeat_rate)
            self.notify_swing_amount(self.song().swing_amount)
            self._show_info()

    def _show_info(self):
        """ Shows note repeat status and rate in status bar. """
        rpt = self._repeat
        value = 'Off'
        if rpt.enabled:
            value = self._resolution_names[self._resolutions.index(rpt.repeat_rate)]
        self.component_message('Note Repeat', value)

    def _set_defaults(self, _=None):
        """ Disables note repeat and sets rate to default rate (1/16ths)
        and swing to default (off). """
        self._repeat.enabled = False
        self._repeat.repeat_rate = self._resolutions[self._default_resolution]
        self.song().swing_amount = 0.0

    def _refresh_record_quantization(self, _=None):
        """ Handles disabling record quantization if repeat is enabled or
        re-enabling it otherwise. """
        if self.is_enabled() and self._repeat.enabled:
            self._last_recording_qntz = self.song().midi_recording_quantization
            self.song().midi_recording_quantization = 0
        elif self._last_recording_qntz is not None:
            self.song().midi_recording_quantization = self._last_recording_qntz
            self._last_recording_qntz = None
        return

    def update(self):
        super(NoteRepeatComponent, self).update()
        if self.is_enabled():
            self._swing_property.update()

    def _update_repeat_button(self):
        self.repeat_on_off_button.is_on = self._repeat.enabled

    @subject_slot('swing_amount')
    def _on_swing_amount_changed(self):
        self.update()
        self.notify_swing_amount(self.song().swing_amount)


class StandardNoteRepeatComponent(NoteRepeatComponent):
    """ StandardNoteRepeatComponent is a NoteRepeatComponent set up to be controlled by
    a group of buttons.  If less than 5 buttons are used, triplet resolutions won't be
    available. """

    def __init__(self, num_buttons=NUM_RESOLUTIONS, cut_from_top=True, *a, **k):
        no_triplets = num_buttons < 5
        super(StandardNoteRepeatComponent, self).__init__(no_triplets=no_triplets, *a, **k)
        self._rate_buttons = RadioButtonGroup(num_buttons, 0, False, checked_color='NoteRepeat.Rate.Selected', unchecked_color='NoteRepeat.Rate.NotSelected', disabled_color='NoteRepeat.Inactive')
        self._offset = len(self._resolutions) - num_buttons if cut_from_top else 0
        self._on_rate_button_value.subject = self._rate_buttons
        self._swing_buttons = None
        self._num_swing_buttons = None
        return

    def set_rate_buttons(self, buttons):
        """ Sets the buttons to use for controlling repeat rate. """
        self._rate_buttons.set_buttons(buttons)

    def set_swing_buttons(self, buttons):
        """ Sets the buttons to use for controlling swing amount. """
        self._swing_buttons = list(buttons) if buttons else []
        self._swing_buttons.reverse()
        self._num_swing_buttons = len(self._swing_buttons) - 1
        self._on_swing_button_value.replace_subjects(self._swing_buttons)
        self._update_swing_buttons()

    def _toggle_repeat_state(self, is_release=False):
        """ Extends standard to disable rate buttons when note repeat is not on. """
        super(StandardNoteRepeatComponent, self)._toggle_repeat_state(is_release)
        rpt = self._repeat
        self._rate_buttons.set_checked_index(self._resolutions.index(rpt.repeat_rate) - self._offset)
        self._rate_buttons.set_enabled(rpt.enabled)
        self._update_swing_buttons()

    @subject_slot('checked_index')
    def _on_rate_button_value(self, index):
        if self.is_enabled():
            self.rate = index + self._offset

    @subject_slot_group('value')
    def _on_swing_button_value(self, value, button):
        if value and self._repeat.enabled:
            btn_index = self._swing_buttons.index(button)
            self.song().swing_amount = 0.5 / self._num_swing_buttons * btn_index
            value = ('{0}%').format(int(self.song().swing_amount * 200))
            self.component_message('Swing Amount', value)

    def update(self):
        super(StandardNoteRepeatComponent, self).update()
        self._update_swing_buttons()

    def _update_swing_buttons(self):
        if self.is_enabled() and self._swing_buttons:
            if self._repeat.enabled:
                swing_val = self.song().swing_amount
                step = 0.5 / self._num_swing_buttons
                for i, button in enumerate(self._swing_buttons):
                    button.set_light('NoteRepeat.Swing.On' if i * step <= swing_val else 'NoteRepeat.Swing.Off')

            else:
                set_group_button_lights(self._swing_buttons, 'NoteRepeat.Inactive')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/NoteRepeatComponent.pyc
