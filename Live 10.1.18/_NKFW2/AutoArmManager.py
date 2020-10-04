# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\AutoArmManager.py
# Compiled at: 2017-05-29 15:43:11
from _Framework.SubjectSlot import SlotManager, subject_slot

class AutoArmManager(SlotManager):
    """ AutoArmManager handles automatically arming MIDI tracks upon selection for
    use with modes that need it. """

    def __init__(self, target_track_comp, *a, **k):
        self._track = None
        self._auto_armed_track = None
        self._is_auto_arming = False
        super(AutoArmManager, self).__init__(*a, **k)
        self._on_target_track_changed.subject = target_track_comp
        self._on_target_track_changed(target_track_comp.target_track)
        return

    def disconnect(self):
        self._clear_auto_arm()
        super(AutoArmManager, self).disconnect()
        self._track = None
        self._auto_armed_track = None
        return

    def set_is_auto_arming(self, auto_arm):
        """ Sets whether this component should autoarm tracks. """
        self._is_auto_arming = auto_arm
        self._handle_auto_arm()

    @subject_slot('target_track')
    def _on_target_track_changed(self, track):
        """ Sets the track this component should use. """
        self._track = None
        if track and track.has_midi_input:
            self._track = track
        self._on_implicit_arm_changed.subject = self._track
        self._handle_auto_arm()
        return

    @subject_slot('implicit_arm')
    def _on_implicit_arm_changed(self):
        """ Ensures that the track this instance is working with cannot be disarmed
        by another instance. """
        if self._auto_armed_track and self._is_auto_arming:
            self._auto_armed_track.implicit_arm = True

    def _handle_auto_arm(self):
        """ Clears last autoarmed track and arms the current track. """
        self._clear_auto_arm()
        if self._is_auto_arming and self._track and self._track.can_be_armed and self._track.has_midi_input:
            self._auto_armed_track = self._track
            self._track.implicit_arm = True

    def _clear_auto_arm(self):
        """ Disarms the autoarmed track if there is one. """
        if self._auto_armed_track and self._auto_armed_track.can_be_armed and self._auto_armed_track.implicit_arm:
            self._auto_armed_track.implicit_arm = False
            self._auto_armed_track = None
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/AutoArmManager.pyc
