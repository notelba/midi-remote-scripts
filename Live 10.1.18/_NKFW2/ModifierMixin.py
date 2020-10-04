# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ModifierMixin.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.SubjectSlot import subject_slot
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Disconnectable import Disconnectable

class ModifierMixin(Disconnectable):
    """ ModifierMixin handles all of the modifier buttons a class may need.  It can purely
    provide setters and references to modifier buttons or it can also provide listeners,
    LED handling and call a callback upon modifier button values being received.

    This module also includes a ModifierOwnerComponent, which is just a CSC that
    implements this mixin."""

    def __init__(self, handle_modifier_leds=True, press_callback=None):
        super(ModifierMixin, self).__init__()
        self._handle_modifier_leds = bool(handle_modifier_leds)
        self._press_callback = press_callback
        self._shift_button = None
        self._select_button = None
        self._mute_button = None
        self._solo_button = None
        self._delete_button = None
        self._duplicate_button = None
        self._double_button = None
        self._quantize_button = None
        return

    def disconnect(self):
        super(ModifierMixin, self).disconnect()
        self._press_callback = None
        self._shift_button = None
        self._select_button = None
        self._mute_button = None
        self._solo_button = None
        self._delete_button = None
        self._duplicate_button = None
        self._double_button = None
        self._quantize_button = None
        return

    def set_shift_button(self, button):
        self._shift_button = button
        self._set_modifier(button, 'shift')

    def set_select_button(self, button):
        self._select_button = button
        self._set_modifier(button, 'select')

    def set_mute_button(self, button):
        self._mute_button = button
        self._set_modifier(button, 'mute')

    def set_solo_button(self, button):
        self._solo_button = button
        self._set_modifier(button, 'solo')

    def set_delete_button(self, button):
        self._delete_button = button
        self._set_modifier(button, 'delete')

    def set_duplicate_button(self, button):
        self._duplicate_button = button
        self._set_modifier(button, 'duplicate')

    def set_double_button(self, button):
        self._double_button = button
        self._set_modifier(button, 'double')

    def set_quantize_button(self, button):
        self._quantize_button = button
        self._set_modifier(button, 'quantize')

    def update_modifier_leds(self):
        if self.is_enabled() and self._handle_modifier_leds:
            if self._shift_button:
                self._shift_button.set_light('Modifiers.Shift')
            if self._select_button:
                self._select_button.set_light('Modifiers.Select')
            if self._mute_button:
                self._mute_button.set_light('Modifiers.Mute')
            if self._solo_button:
                self._solo_button.set_light('Modifiers.Solo')
            if self._delete_button:
                self._delete_button.set_light('Modifiers.Delete')
            if self._duplicate_button:
                self._duplicate_button.set_light('Modifiers.Duplicate')
            if self._double_button:
                self._double_button.set_light('Modifiers.Double')
            if self._quantize_button:
                self._quantize_button.set_light('Modifiers.Quantize')

    def _set_modifier(self, button, modifier_name):
        if self._handle_modifier_leds:
            getattr(self, '_on_%s_button_value' % modifier_name).subject = button
            if self.is_enabled() and button:
                button.set_light('Modifiers.%s' % modifier_name.title())

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        self._handle_modifier_value(value, 'shift')

    @subject_slot('value')
    def _on_select_button_value(self, value):
        self._handle_modifier_value(value, 'select')

    @subject_slot('value')
    def _on_mute_button_value(self, value):
        self._handle_modifier_value(value, 'mute')

    @subject_slot('value')
    def _on_solo_button_value(self, value):
        self._handle_modifier_value(value, 'solo')

    @subject_slot('value')
    def _on_delete_button_value(self, value):
        self._handle_modifier_value(value, 'delete')

    @subject_slot('value')
    def _on_duplicate_button_value(self, value):
        self._handle_modifier_value(value, 'duplicate')

    @subject_slot('value')
    def _on_double_button_value(self, value):
        self._handle_modifier_value(value, 'double')

    @subject_slot('value')
    def _on_quantize_button_value(self, value):
        self._handle_modifier_value(value, 'quantize')

    def _handle_modifier_value(self, value, modifier_name):
        if self.is_enabled():
            button = getattr(self, '_on_%s_button_value' % modifier_name).subject
            if button:
                if self._press_callback:
                    self._press_callback(bool(value), modifier_name)
                button.set_light('Modifiers.Pressed' if value else 'Modifiers.%s' % modifier_name.title())


class ModifierOwnerComponent(ControlSurfaceComponent, ModifierMixin):
    """ Simple component that implements the ModifierMixin. """

    def update(self):
        super(ModifierOwnerComponent, self).update()
        self.update_modifier_leds()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ModifierMixin.pyc
