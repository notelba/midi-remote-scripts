# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\TrackArmState.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .SubjectSlot import Subject, subject_slot, SlotManager

class TrackArmState(Subject, SlotManager):
    __subject_events__ = ('arm', )

    def __init__(self, track=None, *a, **k):
        super(TrackArmState, self).__init__(*a, **k)
        self.set_track(track)

    def set_track(self, track):
        self._track = track
        self._arm = track and track.can_be_armed and (track.arm or track.implicit_arm)
        subject = track if track and track.can_be_armed else None
        self._on_explicit_arm_changed.subject = subject
        self._on_implicit_arm_changed.subject = subject
        return

    @subject_slot(b'arm')
    def _on_explicit_arm_changed(self):
        self._on_arm_changed()

    @subject_slot(b'implicit_arm')
    def _on_implicit_arm_changed(self):
        self._on_arm_changed()

    def _on_arm_changed(self):
        new_state = self._track.arm or self._track.implicit_arm
        if self._arm != new_state:
            self._arm = new_state
            self.notify_arm()

    def _get_arm(self):
        if self._track.can_be_armed:
            return self._arm
        return False

    def _set_arm(self, new_state):
        if self._track.can_be_armed:
            self._track.arm = new_state
            if not new_state:
                self._track.implicit_arm = False
        self._arm = new_state

    arm = property(_get_arm, _set_arm)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Framework/TrackArmState.pyc
