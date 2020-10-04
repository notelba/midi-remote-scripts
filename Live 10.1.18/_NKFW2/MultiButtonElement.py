# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\MultiButtonElement.py
# Compiled at: 2017-03-07 13:28:52
from SpecialButtonElement import SpecialButtonElement

class MultiButtonElement(SpecialButtonElement):
    """ Special button element for use with a button on a controller that sends the same
    MIDI message on different MIDI channels at different times.

    Inits a list of slave button elements that it forwards all sent values to and also
    receives values from. """

    def __init__(self, is_momentary, msg_type, channel, identifier, skin=None, slave_channels=None, name='', *a, **k):
        super(MultiButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin, *a, **k)
        self.name = name
        self._slave_buttons = [ SlaveButtonElement(self, is_momentary, msg_type, slave_channel, identifier, skin, name=(name + '_ch_' + str(slave_channel + 1)), *a, **k) for slave_channel in slave_channels
                              ]

    def reset(self):
        super(MultiButtonElement, self).reset()
        for button in self._slave_buttons:
            button.reset()

    def set_light(self, value):
        super(MultiButtonElement, self).set_light(value)
        for button in self._slave_buttons:
            button.set_light(value)

    def send_value(self, value, **k):
        super(MultiButtonElement, self).send_value(value, **k)
        for button in self._slave_buttons:
            button.send_value(value, **k)


class SlaveButtonElement(SpecialButtonElement):
    """ Special button element that forwards all values it receives back
    to its associated master button. """

    def __init__(self, master, is_momentary, msg_type, channel, identifier, skin=None, *a, **k):
        super(SlaveButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin, *a, **k)
        self._master_button = master

    def receive_value(self, value):
        super(SlaveButtonElement, self).receive_value(value)
        self._master_button.receive_value(value)

    def script_wants_forwarding(self):
        return True
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/MultiButtonElement.pyc
