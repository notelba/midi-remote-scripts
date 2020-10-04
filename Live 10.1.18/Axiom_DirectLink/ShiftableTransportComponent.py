# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_DirectLink\ShiftableTransportComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.TransportComponent import TransportComponent

class ShiftableTransportComponent(TransportComponent):
    """ Special transport class handling the seek buttons differently based on a shift button"""

    def __init__(self):
        self._shift_button = None
        self._shift_pressed = False
        TransportComponent.__init__(self)
        return

    def disconnect(self):
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        TransportComponent.disconnect(self)
        return

    def set_shift_button(self, button):
        assert button == None or isinstance(button, ButtonElement) and button.is_momentary()
        if self._shift_button != button:
            if self._shift_button != None:
                self._shift_button.remove_value_listener(self._shift_value)
                self._shift_pressed = False
            self._shift_button = button
            if self._shift_button != None:
                self._shift_button.add_value_listener(self._shift_value)
        return

    def _shift_value(self, value):
        assert self._shift_button != None
        assert value in range(128)
        if self.is_enabled():
            self._shift_pressed = value > 0
        return

    def _ffwd_value(self, value):
        assert self._ffwd_button != None
        assert value in range(128)
        if self._shift_pressed:
            self.song().current_song_time = self.song().last_event_time
        else:
            TransportComponent._ffwd_value(self, value)
        return

    def _rwd_value(self, value):
        assert self._rwd_button != None
        assert value in range(128)
        if self._shift_pressed:
            self.song().current_song_time = 0.0
        else:
            TransportComponent._rwd_value(self, value)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_DirectLink/ShiftableTransportComponent.pyc
