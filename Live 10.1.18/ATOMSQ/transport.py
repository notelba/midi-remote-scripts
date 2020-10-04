# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\transport.py
# Compiled at: 2020-06-08 15:00:06
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import clamp, listens
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class TransportComponent(TransportComponentBase):
    capture_midi_button = ButtonControl(color=b'Recording.On', pressed_color=b'Recording.Off')
    shift_button = ButtonControl(color=b'DefaultButton.Off', pressed_color=b'DefaultButton.On')
    prev_cue_button = ButtonControl(color=b'DefaultButton.Off', pressed_color=b'DefaultButton.On')
    next_cue_button = ButtonControl(color=b'DefaultButton.Off', pressed_color=b'DefaultButton.On')
    scroll_encoder = EncoderControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self.__on_can_capture_midi_changed.subject = self.song
        self.__on_can_capture_midi_changed()

    @scroll_encoder.value
    def scroll_encoder(self, value, _):
        factor = 1 if value > 0 else -1
        if self.shift_button.is_pressed:
            self.song.tempo = clamp(self.song.tempo + factor, 20, 999)
        else:
            self.song.jump_by(factor)

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
        except RuntimeError:
            pass

    @prev_cue_button.pressed
    def prev_cue_button(self, _):
        if self.song.can_jump_to_prev_cue:
            self.song.jump_to_prev_cue()

    @next_cue_button.pressed
    def next_cue_button(self, _):
        if self.song.can_jump_to_next_cue:
            self.song.jump_to_next_cue()

    @listens(b'can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.enabled = self.song.can_capture_midi
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/transport.pyc
