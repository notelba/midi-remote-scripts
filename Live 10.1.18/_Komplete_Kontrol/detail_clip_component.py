# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\detail_clip_component.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import liveobj_valid, listens
from ableton.v2.control_surface.component import Component
from ableton.v2.control_surface.control import ButtonControl
RecordingQuantization = Live.Song.RecordingQuantization

class DetailClipComponent(Component):
    quantize_notes_button = ButtonControl()
    delete_notes_button = ButtonControl()

    def __init__(self, *a, **k):
        super(DetailClipComponent, self).__init__(*a, **k)
        self._record_quantization = RecordingQuantization.rec_q_sixtenth
        self.__on_record_quantization_changed.subject = self.song
        self.__on_record_quantization_changed()
        self.__on_detail_clip_changed.subject = self.song.view
        self.__on_detail_clip_changed()

    @listens(b'detail_clip')
    def __on_detail_clip_changed(self):
        clip = self.song.view.detail_clip
        if liveobj_valid(clip) and clip.is_midi_clip:
            self.quantize_notes_button.enabled = True
            self.delete_notes_button.enabled = True
        else:
            self.quantize_notes_button.enabled = False
            self.delete_notes_button.enabled = False

    @listens(b'midi_recording_quantization')
    def __on_record_quantization_changed(self):
        if self.song.midi_recording_quantization:
            self._record_quantization = self.song.midi_recording_quantization

    @quantize_notes_button.pressed
    def quantize_notes_button(self, _):
        self.song.view.detail_clip.quantize(self._record_quantization, 1.0)

    @delete_notes_button.pressed
    def delete_notes_button(self, _):
        clip = self.song.view.detail_clip
        clip.remove_notes(0, 0, clip.loop_end, 128)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Komplete_Kontrol/detail_clip_component.pyc
