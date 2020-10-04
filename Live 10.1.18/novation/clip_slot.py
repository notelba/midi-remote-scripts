# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\clip_slot.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, depends
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase

class FixedLengthClipSlotComponent(ClipSlotComponentBase):

    @depends(fixed_length_recording=const(None))
    def __init__(self, fixed_length_recording, *a, **k):
        assert fixed_length_recording is not None
        super(FixedLengthClipSlotComponent, self).__init__(*a, **k)
        self._fixed_length_recording = fixed_length_recording
        return

    def _do_launch_clip(self, fire_state):
        slot = self._clip_slot
        if self._fixed_length_recording.should_start_recording_in_slot(slot):
            self._fixed_length_recording.start_recording_in_slot(slot)
        else:
            super(FixedLengthClipSlotComponent, self)._do_launch_clip(fire_state)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/clip_slot.pyc
