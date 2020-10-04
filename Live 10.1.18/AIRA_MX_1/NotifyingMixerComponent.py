# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AIRA_MX_1\NotifyingMixerComponent.py
# Compiled at: 2020-07-31 16:19:16
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.MixerComponent import MixerComponent
from _Framework.Control import ButtonControl

class NotifyingMixerComponent(MixerComponent):
    """
    Special mixer class that uses return tracks alongside midi and
    audio tracks and includes controls for incrementing/decrementing
    between sends.
    """
    send_index_up_button = ButtonControl()
    send_index_down_button = ButtonControl()
    modifier_button = ButtonControl(color=0, pressed_color=127)

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    @send_index_up_button.pressed
    def send_index_up_button(self, button):
        self._adjust_send_index(1)

    @send_index_down_button.pressed
    def send_index_down_button(self, button):
        self._adjust_send_index(-1)

    def _adjust_send_index(self, factor):
        new_index = self.send_index + factor
        if 0 <= new_index < self.num_sends:
            self.send_index = new_index
            self._show_msg_callback(b'Tone/Filter Controlling Send: %s' % self.song().return_tracks[self.send_index].name)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/AIRA_MX_1/NotifyingMixerComponent.pyc
