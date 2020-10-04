# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\IdentifiableControlSurface.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from .ControlSurface import ControlSurface
from . import Task
SYSEX_IDENTITY_REQUEST = (240, 126, 0, 6, 1, 247)

class IdentifiableControlSurface(ControlSurface):
    """
    Control surface that sends an identity request to verify the right device is
    linked to it.
    If the data bytes of the response start with product_id_bytes, the device will
    call on_identified.
    Data bytes start at index 5 and cannot be longer than 12 bytes.
    """
    identity_request_delay = 0.5
    identity_request = SYSEX_IDENTITY_REQUEST

    def __init__(self, product_id_bytes=None, *a, **k):
        super(IdentifiableControlSurface, self).__init__(*a, **k)
        assert product_id_bytes is not None
        assert len(product_id_bytes) < 12
        self._product_id_bytes = product_id_bytes
        self._identity_response_pending = False
        self._request_task = self._tasks.add(Task.sequence(Task.wait(self.identity_request_delay), Task.run(self._send_identity_request)))
        self._request_task.kill()
        return

    def on_identified(self):
        raise NotImplementedError

    def port_settings_changed(self):
        self._request_task.restart()

    def handle_sysex(self, midi_bytes):
        if self._is_identity_response(midi_bytes):
            product_id_bytes = self._extract_product_id_bytes(midi_bytes)
            if product_id_bytes == self._product_id_bytes:
                self._request_task.kill()
                if self._identity_response_pending:
                    self.on_identified()
                    self._identity_response_pending = False
            else:
                self.log_message(b'MIDI device responded with wrong product id (%s != %s).' % (
                 str(self._product_id_bytes), str(product_id_bytes)))
        else:
            super(IdentifiableControlSurface, self).handle_sysex(midi_bytes)

    def _is_identity_response(self, midi_bytes):
        return midi_bytes[3:5] == (6, 2)

    def _extract_product_id_bytes(self, midi_bytes):
        return midi_bytes[5:5 + len(self._product_id_bytes)]

    def _send_identity_request(self):
        self._identity_response_pending = True
        self._send_midi(self.identity_request)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Framework/IdentifiableControlSurface.pyc
