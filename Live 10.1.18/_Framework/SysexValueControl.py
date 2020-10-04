# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\SysexValueControl.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .InputControlElement import InputControlElement, MIDI_SYSEX_TYPE

class SysexValueControl(InputControlElement):
    """
    Sysex value control receives a sysex message, identified by a
    prefix.  The value can be requested with a value_enquiry MIDI
    message to the controller.
    """

    def __init__(self, message_prefix=None, value_enquiry=None, default_value=None, *a, **k):
        super(SysexValueControl, self).__init__(msg_type=MIDI_SYSEX_TYPE, sysex_identifier=message_prefix, *a, **k)
        self._value_enquiry = value_enquiry
        self._default_value = default_value

    def send_value(self, value_bytes):
        self.send_midi(self.message_sysex_identifier() + value_bytes + (247, ))

    def enquire_value(self):
        assert self._value_enquiry != None
        self.send_midi(self._value_enquiry)
        return

    def reset(self):
        if self._default_value != None:
            self.send_value(self._default_value)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Framework/SysexValueControl.pyc
