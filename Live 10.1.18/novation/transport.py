# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\transport.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, ToggleButtonControl

class TransportComponent(TransportComponentBase):
    play_button = ToggleButtonControl(toggled_color=b'Transport.PlayOn', untoggled_color=b'Transport.PlayOff')
    capture_midi_button = ButtonControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._metronome_toggle.view_transform = lambda v: b'Transport.MetronomeOn' if v else b'Transport.MetronomeOff'
        self.__on_can_capture_midi_changed.subject = self.song
        self.__on_can_capture_midi_changed()

    @play_button.toggled
    def _on_play_button_toggled(self, is_toggled, _):
        if is_toggled:
            self.song.stop_playing()
        self.song.is_playing = is_toggled

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
        except RuntimeError:
            pass

    @listens(b'can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.color = (b'Transport.Capture{}').format(b'On' if self.song.can_capture_midi else b'Off')

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self.continue_playing_button.color = (b'Transport.Continue{}').format(b'Off' if self.song.is_playing else b'On')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/transport.pyc
