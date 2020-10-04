# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\fixed_length_recording.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
NUM_LENGTHS = 8

def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


class FixedLengthRecording(object):
    """
    Handles recording a fixed length clip
    based on a fixed length setting
    """

    def __init__(self, song=None, fixed_length_setting=None, *a, **k):
        assert song is not None
        assert fixed_length_setting is not None
        super(FixedLengthRecording, self).__init__(*a, **k)
        self._song = song
        self._fixed_length_setting = fixed_length_setting
        return

    def should_start_recording_in_slot(self, clip_slot):
        return track_can_record(clip_slot.canonical_parent) and not clip_slot.is_recording and not clip_slot.has_clip and self._fixed_length_setting.enabled

    def start_recording_in_slot(self, clip_slot):
        if self.should_start_recording_in_slot(clip_slot):
            clip_slot.fire(record_length=self._fixed_length_setting.get_selected_length(self._song))
        else:
            clip_slot.fire()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/fixed_length_recording.pyc
