# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\PlayheadComponent.py
# Compiled at: 2017-05-15 14:39:56
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class PlayheadComponent(ControlSurfaceComponent):
    """ PlayheadComponent displays a clip's playing position for use in
    step-sequencing. """

    def __init__(self, resolution_comp, page_comp, notes=range(8), triplet_notes=range(6), feedback_channels=None, targets_comp=None, *a, **k):
        super(PlayheadComponent, self).__init__(*a, **k)
        self.is_private = True
        self._playhead = None
        self._clip = None
        self._notes = list(notes)
        self._triplet_notes = list(triplet_notes)
        self._feedback_channels = feedback_channels or []
        self.set_clip.subject = targets_comp
        self._on_resolution_changed.subject = resolution_comp
        self._on_start_time_changed.subject = page_comp
        return

    def disconnect(self):
        super(PlayheadComponent, self).disconnect()
        self._playhead = None
        self._clip = None
        self._notes = None
        self._triplet_notes = None
        self._feedback_channels = None
        return

    def set_playhead(self, playhead):
        """ Sets the playhead object to use. """
        self._playhead = playhead
        self.update()

    @subject_slot('target_clip')
    def set_clip(self, clip):
        """ Sets the clip to display the playhead for. """
        self._clip = clip if clip and clip.is_midi_clip else None
        self._on_playing_status_changed.subject = self._clip
        self._on_song_is_playing_changed.subject = self.song() if self._clip else None
        self.update()
        return

    @subject_slot('resolution')
    def _on_resolution_changed(self, _):
        self.update()

    @subject_slot('start_time')
    def _on_start_time_changed(self, _):
        self.update()

    @subject_slot('playing_status')
    def _on_playing_status_changed(self):
        self.update()

    @subject_slot('is_playing')
    def _on_song_is_playing_changed(self):
        self.update()

    def update(self):
        super(PlayheadComponent, self).update()
        if self._playhead:
            if self.is_enabled() and self.song().is_playing and self._clip and self._clip.is_playing:
                clip_slot = self._clip.canonical_parent
                track = clip_slot.canonical_parent if clip_slot else None
            else:
                track = None
            self._playhead.track = track
            self._playhead.clip = self._clip if track else None
            self._playhead.set_feedback_channels(self._feedback_channels)
            if track:
                res = self._on_resolution_changed.subject
                page = self._on_start_time_changed.subject
                notes = self._triplet_notes if res.is_triplet else self._notes
                self._playhead.notes = notes
                self._playhead.start_time = page.start_time
                self._playhead.step_length = res.resolution
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/PlayheadComponent.pyc
