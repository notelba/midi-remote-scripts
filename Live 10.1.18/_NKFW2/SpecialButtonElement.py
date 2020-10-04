# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialButtonElement.py
# Compiled at: 2017-12-01 02:00:32
from _Framework.ButtonElement import ButtonElement, DummyUndoStepHandler, Skin

class SpecialButtonElement(ButtonElement):
    """ SpecialButtonElement extends ButtonElement to provide methods for setting on/off
    LED values of the button and specifically turning it on/off. Also, allows the button
    to be disabled so that it can be used for sending data to MIDI tracks. """

    def __init__(self, is_momentary, msg_type, channel, identifier, skin=Skin(), undo_step_handler=DummyUndoStepHandler(), *a, **k):
        self._is_enabled = True
        self._ignore_next_off_values = False
        self._off_value = 0
        skin_value = skin._colors.get('DefaultButton.Off', None)
        if skin_value is not None:
            self._off_value = int(skin_value)
        super(SpecialButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin, undo_step_handler, *a, **k)
        return

    def disconnect(self):
        """ Overrides standard to call a forced turn_off instead of reset. """
        self.force_next_send()
        self.turn_off()

    def is_enabled(self):
        """ Returns whether this button is enabled. """
        return self._is_enabled

    def set_led(self, is_on):
        """ Toggles the LED on or off. """
        if bool(is_on):
            self.turn_on()
        else:
            self.turn_off()

    def turn_on(self):
        """ Turns the LED on. """
        self.set_light('DefaultButton.On')

    def turn_off(self):
        """ Turns the LED off. """
        self.set_light('DefaultButton.Off')

    def reset(self):
        """ Same as turn_off. """
        self.set_light('DefaultButton.Off')

    def _do_send_value(self, value, channel=None):
        """ Extends standard to do nothing if is off value and ignoring next off values
        unless the send is forced. """
        if value == self._off_value and self._ignore_next_off_values and not self._force_next_send:
            return
        self._ignore_next_off_values = False
        super(SpecialButtonElement, self)._do_send_value(value, channel)

    def set_enabled(self, enabled, ignore_next_off_values=False):
        """ Enables/disables the button. When disabled, it can be used for sending data
        to MIDI tracks. This can optionally cause the button to ignore the next off values
        it's sent to prevent its LED from being turned off when enabled. """
        if self._is_enabled != bool(enabled):
            self._is_enabled = bool(enabled)
            self._ignore_next_off_values = self._is_enabled and bool(ignore_next_off_values)
            self._request_rebuild()
        elif self._ignore_next_off_values != bool(ignore_next_off_values):
            self._ignore_next_off_values = False

    def script_wants_forwarding(self):
        """ Returns whether or not the button should be used in the script or to send
        data to MIDI tracks. """
        return ButtonElement.script_wants_forwarding(self) and self._is_enabled
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialButtonElement.pyc
