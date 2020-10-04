# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackMixerWrapper.py
# Compiled at: 2017-03-07 13:28:53
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
SENDS_OFFSET = 3

class TrackMixerWrapper(ControlSurfaceComponent):
    """ TrackMixerWrapper wraps a track's mixer device parameters so that it can
    be used just like any other device. """
    __subject_events__ = ('parameters', )

    def __init__(self, name='Track_Mixer_Device', *a, **k):
        super(TrackMixerWrapper, self).__init__(name=name, *a, **k)
        self._parameters = []
        self._track = None
        self._on_returns_changed.subject = self.song()
        return

    def disconnect(self):
        super(TrackMixerWrapper, self).disconnect()
        self._parameters = None
        self._track = None
        return

    @property
    def track(self):
        return self._track

    @property
    def parameters(self):
        return self._parameters

    @property
    def class_name(self):
        return 'MixerDevice'

    def set_track(self, track):
        assert track is None or isinstance(track, Live.Track.Track)
        self._track = track
        self.update()
        return

    def update(self, notify=False):
        """ Updates the parameter list based on the track type and will also notify
        parameter listeners if specified.  This is needed in the case of returns being
        added or removed. """
        super(TrackMixerWrapper, self).update()
        self._parameters = []
        if self._track:
            tm = self._track.mixer_device
            self._parameters = [tm.volume, tm.panning]
            if self._track != self.song().master_track:
                self._parameters.append(tm.track_activator)
                for s in tm.sends:
                    self._parameters.append(s)

            if notify:
                self.notify_parameters()

    @subject_slot('return_tracks')
    def _on_returns_changed(self):
        if self._track and self._track != self.song().master_track:
            self.update(True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackMixerWrapper.pyc
