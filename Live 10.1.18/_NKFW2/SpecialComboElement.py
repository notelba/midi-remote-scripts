# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialComboElement.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.ComboElement import ComboElement

class SpecialComboElement(ComboElement):
    """ SpecialComboElement extends ComboElement to include methods needed throughout
    the framework. This simply forwards calls to the wrapped control when it is owned.
    It also allows for alternate forms of variant enforcement for use with translated
    and multi-mode controls. """

    def __init__(self, *a, **k):
        self._reset_on_lost = k.pop('reset_on_lost', False)
        self._mod_based_enforce = k.pop('mod_based_enforce', self._reset_on_lost)
        super(SpecialComboElement, self).__init__(*a, **k)

    def message_type(self):
        return self._wrapped_control.message_type()

    def set_channel(self, value):
        if self.owns_control_element(self._wrapped_control):
            self._wrapped_control.set_channel(value)

    def set_identifier(self, value):
        if self.owns_control_element(self._wrapped_control):
            self._wrapped_control.set_identifier(value)

    def set_enabled(self, enable):
        if self.owns_control_element(self._wrapped_control):
            self._wrapped_control.set_enabled(enable)

    def set_light(self, value):
        if self.owns_control_element(self._wrapped_control):
            self._wrapped_control.set_light(value)

    def force_next_send(self):
        if self.owns_control_element(self._wrapped_control):
            self._wrapped_control.force_next_send()

    def use_default_message(self):
        if self.owns_control_element(self._wrapped_control):
            self._wrapped_control.use_default_message()

    def is_enabled(self):
        if self.owns_control_element(self._wrapped_control):
            return self._wrapped_control.is_enabled()
        return False

    def _enforce_control_invariant(self):
        """ Extends standard to reset wrapped control when ownership is lost. """
        super(SpecialComboElement, self)._enforce_control_invariant()
        if self._reset_on_lost and not self._combo_is_on() and self._wrapped_control:
            self._wrapped_control.use_default_message()
            self._wrapped_control.set_enabled(True)

    def _modifier_is_valid(self, mod):
        """ Optionally overrides standard so that enforement is purely based on whether
        modifiers are pressed. """
        if self._mod_based_enforce:
            return mod.is_pressed() == self._combo_modifiers[mod]
        return super(SpecialComboElement, self)._modifier_is_valid(mod)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialComboElement.pyc
