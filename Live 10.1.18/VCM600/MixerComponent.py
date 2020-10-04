# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\MixerComponent.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.MixerComponent import MixerComponent as MixerComponentBase
from .TrackEQComponent import TrackEQComponent
from .TrackFilterComponent import TrackFilterComponent

class MixerComponent(MixerComponentBase):

    def __init__(self, num_tracks, *a, **k):
        self._track_eqs = [ TrackEQComponent() for _ in xrange(num_tracks) ]
        self._track_filters = [ TrackFilterComponent() for _ in xrange(num_tracks) ]
        super(MixerComponent, self).__init__(num_tracks, *a, **k)
        map(self.register_components, self._track_eqs)
        map(self.register_components, self._track_filters)

    def track_eq(self, index):
        assert index in range(len(self._track_eqs))
        return self._track_eqs[index]

    def track_filter(self, index):
        assert index in range(len(self._track_filters))
        return self._track_filters[index]

    def _reassign_tracks(self):
        super(MixerComponent, self)._reassign_tracks()
        tracks = self.tracks_to_use()
        for index in range(len(self._channel_strips)):
            track_index = self._track_offset + index
            track = tracks[track_index] if len(tracks) > track_index else None
            if len(self._track_eqs) > index:
                self._track_eqs[index].set_track(track)
            if len(self._track_filters) > index:
                self._track_filters[index].set_track(track)

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/VCM600/MixerComponent.pyc
