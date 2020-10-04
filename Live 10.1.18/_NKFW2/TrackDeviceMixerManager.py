# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackDeviceMixerManager.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.SubjectSlot import SlotManager, subject_slot
from TrackDeviceManager import TrackDeviceManager
from Utils import right_justify_track_components
justify_function = right_justify_track_components

class TrackDeviceMixerManager(SlotManager):
    """ TrackDeviceMixerManager works with the SlaveManager and manages a group of
    TrackDeviceManagers. """

    def __init__(self, slave_manager, num_tracks=8, use_wrappers=False, right_just_returns=True, *a, **k):
        super(TrackDeviceMixerManager, self).__init__(*a, **k)
        self._right_justify_returns = bool(right_just_returns)
        self._song = None
        self._slave_manager = slave_manager
        self._reassign_tracks.subject = slave_manager
        self._components = [ TrackDeviceManager(use_wrapper=use_wrappers) for _ in xrange(num_tracks)
                           ]
        self._reassign_tracks(slave_manager.track_offset)
        return

    def set_song(self, song):
        """ Sets the song instance to control. """
        self._song = song
        if self._right_justify_returns:
            self._reassign_tracks(self._slave_manager.track_offset)

    def get_track_manager(self, index):
        """ Returns the TrackDeviceManager associated with the given index. """
        assert index in xrange(len(self._components))
        return self._components[index]

    @subject_slot('track_offset')
    def _reassign_tracks(self, offset):
        tracks = self._slave_manager.tracks_to_use
        if self._right_justify_returns and self._song:
            justify_function(self._song, tracks, offset, self._components)
        else:
            for index, comp in enumerate(self._components):
                track_offset = offset + index
                if track_offset in xrange(len(tracks)):
                    comp.set_track(tracks[track_offset])
                else:
                    comp.set_track(None)

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackDeviceMixerManager.pyc
