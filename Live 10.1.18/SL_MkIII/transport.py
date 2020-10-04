# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\transport.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._loop_toggle.view_transform = lambda v: b'Transport.LoopOn' if v else b'Transport.LoopOff'
        self._record_toggle.view_transform = lambda v: b'Recording.On' if v else b'Recording.Off'

    def set_seek_forward_button(self, ffwd_button):
        super(TransportComponent, self).set_seek_forward_button(ffwd_button)
        self._update_seek_button(self._ffwd_button)

    def set_seek_backward_button(self, rwd_button):
        super(TransportComponent, self).set_seek_backward_button(rwd_button)
        self._update_seek_button(self._rwd_button)

    def _ffwd_value(self, value):
        super(TransportComponent, self)._ffwd_value(value)
        self._update_seek_button(self._ffwd_button)

    def _rwd_value(self, value):
        super(TransportComponent, self)._rwd_value(value)
        self._update_seek_button(self._rwd_button)

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self._update_continue_playing_button()

    def _update_continue_playing_button(self):
        self.continue_playing_button.color = b'Transport.PlayOn' if self.song.is_playing else b'Transport.PlayOff'

    def _update_seek_button(self, button):
        if self.is_enabled() and button != None:
            button.set_light(b'Transport.SeekOn' if button.is_pressed() else b'Transport.SeekOff')
        return

    def _update_stop_button_color(self):
        self.stop_button.color = b'Transport.StopEnabled' if self.play_button.is_toggled else b'Transport.StopDisabled'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/SL_MkIII/transport.pyc
