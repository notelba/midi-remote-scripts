# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SlaveManager.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.SubjectSlot import SlotManager, Subject, subject_slot

class SlaveManager(SlotManager, Subject):
    """ SlaveManager observes the track offset of a master component (SessionComponent or
    SpecialMixerComponent) and notifies interested subjects. """
    __subject_events__ = ('track_offset', )

    def __init__(self, song, *a, **k):
        super(SlaveManager, self).__init__(*a, **k)
        self._track_offset = -1
        self._master_component = None
        self._on_visible_tracks_changed.subject = song
        self._on_return_tracks_changed.subject = song
        return

    def disconnect(self):
        super(SlaveManager, self).disconnect()
        self._master_component = None
        return

    def set_master_component(self, component):
        """ Sets the component to slave to. """
        self._master_component = component
        self._on_offsets_changed.subject = component
        self.update()

    @property
    def track_offset(self):
        """ Returns the current track offset. """
        return self._track_offset

    @property
    def tracks_to_use(self):
        """ Returns the master's tracks_to_use if one exists. """
        if self._master_component:
            return self._master_component.tracks_to_use()
        else:
            return

    def update(self):
        self._track_offset = -1
        self._on_offsets_changed()

    @subject_slot('offset')
    def _on_offsets_changed(self):
        """ Called when the master component's offset changes and calls reassign_tracks
        if track offset is different from current. """
        master = self._on_offsets_changed.subject
        if master:
            master_offset = master.track_offset()
            if self._track_offset != master_offset:
                self._track_offset = master_offset
                self.notify_track_offset(self._track_offset)

    @subject_slot('visible_tracks')
    def _on_visible_tracks_changed(self):
        self.update()

    @subject_slot('return_tracks')
    def _on_return_tracks_changed(self):
        self.update()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SlaveManager.pyc
