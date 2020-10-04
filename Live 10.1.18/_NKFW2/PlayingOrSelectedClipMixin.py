# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\PlayingOrSelectedClipMixin.py
# Compiled at: 2017-09-30 15:26:23
import Live
from _Framework.Disconnectable import Disconnectable
from _Framework.SubjectSlot import subject_slot
from Utils import live_object_is_valid

class PlayingOrSelectedClipMixin(Disconnectable):
    """ PlayingOrSelectedClipMixin handles determining the clip to control on a track -
    either the playing (if there is one) or selected clip.  Users of this mixin must
    implement a set_clip(self, clip) method. """

    def __init__(self, targets_comp=None, *a, **k):
        super(PlayingOrSelectedClipMixin, self).__init__(*a, **k)
        self._track = None
        self.set_track.subject = targets_comp
        return

    def disconnect(self):
        super(PlayingOrSelectedClipMixin, self).disconnect()
        self._track = None
        return

    @subject_slot('target_track')
    def set_track(self, track):
        """ Sets the track this component should monitor and adds listeners. """
        assert track is None or isinstance(track, Live.Track.Track)
        self._track = None
        self.set_clip(None)
        self._on_slot_has_clip_changed.subject = None
        if track in self.song().tracks:
            self._track = track
        self._on_playing_slot_index_changed.subject = self._track
        self._on_playing_slot_index_changed()
        return

    def update(self):
        super(PlayingOrSelectedClipMixin, self).update()
        self.set_track(self._track)

    @subject_slot('playing_slot_index')
    def _on_playing_slot_index_changed(self):
        """ Called on playing slot changes to set the clip to control. If none, will try
        to connect to selected clip or add listener on selected slot. """
        if self.is_enabled() and self._track:
            slot_index = self._track.playing_slot_index
            if slot_index >= 0 and self._track.clip_slots[slot_index].has_clip:
                self.set_clip(self._track.clip_slots[slot_index].clip)
            else:
                self.set_clip(None)
                self.on_selected_scene_changed()
        return

    @subject_slot('has_clip')
    def _on_slot_has_clip_changed(self):
        self.on_selected_scene_changed()

    def on_selected_scene_changed(self):
        """ Called on scene changes to set the clip to control (or adds slot listener)
        if one already hasn't been set. """
        super(PlayingOrSelectedClipMixin, self).on_selected_scene_changed()
        if self.is_enabled() and self._track and (not live_object_is_valid(self._clip) or not self._clip.is_playing):
            slot = self._track.clip_slots[list(self.song().scenes).index(self.song().view.selected_scene)]
            if slot and slot.has_clip:
                self.set_clip(slot.clip)
            else:
                self.set_clip(None)
            self._on_slot_has_clip_changed.subject = slot
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/PlayingOrSelectedClipMixin.pyc
