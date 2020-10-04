# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackMeterMixerComponent.py
# Compiled at: 2017-03-07 13:28:53
from functools import partial
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from TrackMeterComponent import TrackMeterComponent
from Utils import right_justify_track_components
justify_function = right_justify_track_components

class TrackMeterMixerComponent(CompoundComponent):
    """ TrackMeterMixerComponent works with SlaveManager and handles setting the tracks
    for a set of TrackMeterComponents. This is meant to be used with the
    SpecialMixerComponent. """

    def __init__(self, slave_manager, num_buttons, num_tracks=8, limit_to_0_db=False, should_invert_buttons=True, right_just_returns=True, name='Meter_Mixer_Control', *a, **k):
        super(TrackMeterMixerComponent, self).__init__(name=name, *a, **k)
        self._right_justify_returns = bool(right_just_returns)
        self._components = []
        for i in xrange(num_tracks):
            comp = TrackMeterComponent(num_buttons, limit_to_0_db=limit_to_0_db, should_invert_buttons=should_invert_buttons, name='Track_Meter_%s' % i)
            self._components.append(comp)
            self.register_component(comp)

        self._reassign_tracks.subject = slave_manager
        self._reassign_tracks(slave_manager.track_offset)

    def __getattr__(self, name):
        """ Override to extract component index to set buttons for. """
        if name.startswith('set_meter_buttons_'):
            return partial(self._set_meter_buttons, int(name[(-1)]))
        if name.startswith('set_volume_buttons_'):
            return partial(self._set_volume_buttons, int(name[(-1)]))

    def _set_meter_buttons(self, index, buttons):
        assert index in xrange(len(self._components))
        self._components[index].set_meter_buttons(buttons)

    def _set_volume_buttons(self, index, buttons):
        assert index in xrange(len(self._components))
        self._components[index].set_volume_buttons(buttons)

    @subject_slot('track_offset')
    def _reassign_tracks(self, offset):
        """ Called when the mixer component's offset changes. """
        tracks = self._reassign_tracks.subject.tracks_to_use
        if self._right_justify_returns:
            justify_function(self.song(), tracks, offset, self._components)
        else:
            for index, comp in enumerate(self._components):
                track_offset = offset + index
                if track_offset in xrange(len(tracks)):
                    comp.set_track(tracks[track_offset])
                else:
                    comp.set_track(None)

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackMeterMixerComponent.pyc
