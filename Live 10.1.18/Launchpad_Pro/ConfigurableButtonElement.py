# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\ConfigurableButtonElement.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import SkinColorMissingError
from _Framework.ButtonElement import ButtonElement, ON_VALUE, OFF_VALUE

class ConfigurableButtonElement(ButtonElement):
    """
    Special button class (adapted from Push script for LP Pro)
    that can be configured with custom on- and off-values.

    A ConfigurableButtonElement can have states other than True or
    False, which can be defined by setting the 'states' property.
    Thus 'set_light' can take any state or skin color.
    """
    default_states = {True: b'DefaultButton.On', False: b'DefaultButton.Disabled'}
    send_depends_on_forwarding = False

    def __init__(self, is_momentary, msg_type, channel, identifier, skin=None, default_states=None, *a, **k):
        super(ConfigurableButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin=skin, **k)
        if default_states is not None:
            self.default_states = default_states
        self.states = dict(self.default_states)
        return

    @property
    def _on_value(self):
        return self.states[True]

    @property
    def _off_value(self):
        return self.states[False]

    @property
    def on_value(self):
        return self._try_fetch_skin_value(self._on_value)

    @property
    def off_value(self):
        return self._try_fetch_skin_value(self._off_value)

    def _try_fetch_skin_value(self, value):
        try:
            return self._skin[value]
        except SkinColorMissingError:
            return value

    def reset(self):
        self.set_light(b'DefaultButton.Disabled')
        self.reset_state()

    def reset_state(self):
        self.states = dict(self.default_states)
        super(ConfigurableButtonElement, self).reset_state()
        self.set_enabled(True)

    def set_on_off_values(self, on_value, off_value):
        self.states[True] = on_value
        self.states[False] = off_value

    def set_enabled(self, enabled):
        self.suppress_script_forwarding = not enabled

    def is_enabled(self):
        return not self.suppress_script_forwarding

    def set_light(self, value):
        super(ConfigurableButtonElement, self).set_light(self.states.get(value, value))

    def send_value(self, value, **k):
        if value is ON_VALUE:
            self._do_send_on_value()
        elif value is OFF_VALUE:
            self._do_send_off_value()
        else:
            super(ConfigurableButtonElement, self).send_value(value, **k)

    def _do_send_on_value(self):
        self._skin[self._on_value].draw(self)

    def _do_send_off_value(self):
        self._skin[self._off_value].draw(self)

    def script_wants_forwarding(self):
        return not self.suppress_script_forwarding
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro/ConfigurableButtonElement.pyc
