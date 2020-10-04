# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_DirectLink\PeekableEncoderElement.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *

class PeekableEncoderElement(EncoderElement):
    """ Encoder that can be connected and disconnected to a specific parameter """

    def __init__(self, msg_type, channel, identifier, map_mode):
        EncoderElement.__init__(self, msg_type, channel, identifier, map_mode)
        self._peek_mode = False

    def set_peek_mode(self, peek_mode):
        assert isinstance(peek_mode, type(False))
        if self._peek_mode != peek_mode:
            self._peek_mode = peek_mode
            self._request_rebuild()

    def get_peek_mode(self):
        return self._peek_mode

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        current_parameter = self._parameter_to_map_to
        if self._peek_mode:
            self._parameter_to_map_to = None
        InputControlElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        self._parameter_to_map_to = current_parameter
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_DirectLink/PeekableEncoderElement.pyc
