# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\pad_button_element.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const
from ableton.v2.control_surface.elements import ButtonElement

class PadButtonElement(ButtonElement):
    """
    Button element for holding Push pressure-sensitive pad. The pad_id
    parameter defines the Pad coordine id used in the sysex protocol.
    """

    class ProxiedInterface(ButtonElement.ProxiedInterface):
        sensitivity_profile = const(None)

    def __init__(self, pad_id=None, pad_sensitivity_update=None, *a, **k):
        assert pad_id is not None
        super(PadButtonElement, self).__init__(*a, **k)
        self._sensitivity_profile = b'default'
        self._pad_id = pad_id
        self._pad_sensitivity_update = pad_sensitivity_update
        return

    def _get_sensitivity_profile(self):
        return self._sensitivity_profile

    def _set_sensitivity_profile(self, profile):
        if profile != self._sensitivity_profile and self._pad_sensitivity_update is not None:
            self._sensitivity_profile = profile
            self._pad_sensitivity_update.set_pad(self._pad_id, profile)
        return

    sensitivity_profile = property(_get_sensitivity_profile, _set_sensitivity_profile)

    def reset(self):
        self.sensitivity_profile = b'default'
        super(PadButtonElement, self).reset()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/pushbase/pad_button_element.pyc
