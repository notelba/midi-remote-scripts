# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\fixed_length.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, control_list
from .fixed_length_recording import FixedLengthRecording
NUM_LENGTHS = 8

class FixedLengthSetting(object):
    """ Stores the fixed length setting """

    def __init__(self, *a, **k):
        super(FixedLengthSetting, self).__init__(*a, **k)
        self._selected_index = 0
        self._enabled = False

    @property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        assert isinstance(value, int)
        self._selected_index = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        assert isinstance(value, bool)
        self._enabled = value

    def get_selected_length(self, song):
        """ Returns the current fixed length setting in absolute beat time """
        fixed_length_in_bars = self._selected_index + 1
        fixed_length_in_beats = fixed_length_in_bars * 4
        return fixed_length_in_beats * float(song.signature_numerator) / song.signature_denominator


class FixedLengthComponent(Component):
    """
    UI component for fixed length

    Toggles fixed length mode on a short press and
    enables the FixedLengthSettingComponent while held
    """
    fixed_length_button = ButtonControl(color=b'FixedLength.Off')

    def __init__(self, fixed_length_setting=None, *a, **k):
        super(FixedLengthComponent, self).__init__(*a, **k)
        assert fixed_length_setting is not None
        self.settings_component = FixedLengthSettingComponent(fixed_length_setting=fixed_length_setting, parent=self, is_enabled=False)
        self._fixed_length_setting = fixed_length_setting
        return

    @fixed_length_button.pressed
    def fixed_length_button(self, button):
        button.color = b'FixedLength.On'

    @fixed_length_button.released_immediately
    def fixed_length_button(self, _):
        self._fixed_length_setting.enabled = not self._fixed_length_setting.enabled
        self._update_fixed_length_button()

    @fixed_length_button.pressed_delayed
    def fixed_length_button(self, button):
        self._fixed_length_setting.enabled = True
        self.settings_component.set_enabled(True)
        button.color = b'FixedLength.Held'

    @fixed_length_button.released
    def fixed_length_button(self, _):
        self._update_fixed_length_button()
        self.settings_component.set_enabled(False)

    def _update_fixed_length_button(self):
        self.fixed_length_button.color = (b'FixedLength.{}').format(b'On' if self._fixed_length_setting.enabled else b'Off')


class FixedLengthSettingComponent(Component):
    """ UI component for selecting a length for fixed length recording """
    length_option_buttons = control_list(ButtonControl, color=b'FixedLength.Option', control_count=NUM_LENGTHS)

    def __init__(self, fixed_length_setting=None, *a, **k):
        super(FixedLengthSettingComponent, self).__init__(*a, **k)
        assert fixed_length_setting is not None
        self._fixed_length_setting = fixed_length_setting
        self._update_length_option_buttons()
        return

    @length_option_buttons.pressed
    def length_option_buttons(self, button):
        self._fixed_length_setting.selected_index = button.index
        self._update_length_option_buttons()

    @length_option_buttons.released
    def length_option_buttons(self, _):
        self._update_length_option_buttons()

    def _update_length_option_buttons(self):
        for index, button in enumerate(self.length_option_buttons):
            if button.is_pressed:
                button.color = b'FixedLength.OptionHeld'
            else:
                button.color = (b'FixedLength.{}').format(b'OptionInRange' if index <= self._fixed_length_setting.selected_index else b'Option')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/fixed_length.pyc
