# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ResettingMixerComponent.py
# Compiled at: 2017-10-14 18:54:45
from itertools import izip_longest
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from ResettingChannelStripComponent import ResettingChannelStripComponent
from Utils import right_justify_track_components
justify_function = right_justify_track_components

class ResettingMixerComponent(CompoundComponent):
    """ ResettingMixerComponent works with a SlaveManager to control a group of
    ResettingChannelStripComponents. """

    def __init__(self, slave_manager, num_tracks=8, right_just_returns=True, name='Resetting_Mixer_Control', *a, **k):
        super(ResettingMixerComponent, self).__init__(name=name, *a, **k)
        self._right_justify_returns = bool(right_just_returns)
        self._channel_strips = []
        for _ in xrange(num_tracks):
            strip = self.register_component(ResettingChannelStripComponent())
            self._channel_strips.append(strip)

        self._reassign_tracks.subject = slave_manager
        self._reassign_tracks(slave_manager.track_offset)

    def set_reset_volume_buttons(self, buttons):
        """ Sets the buttons to use for resetting volume. """
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.set_reset_volume_button(button)

    def set_reset_pan_buttons(self, buttons):
        """ Sets the buttons to use for resetting pan. """
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.set_reset_pan_button(button)

    def set_reset_send_a_buttons(self, buttons):
        """ Sets the buttons to use for resetting send A. """
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.set_reset_send_a_button(button)

    def set_reset_send_b_buttons(self, buttons):
        """ Sets the buttons to use for resetting send B. """
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.set_reset_send_b_button(button)

    @subject_slot('track_offset')
    def _reassign_tracks(self, offset):
        tracks = self._reassign_tracks.subject.tracks_to_use
        if self._right_justify_returns:
            justify_function(self.song(), tracks, offset, self._channel_strips)
        else:
            for index, comp in enumerate(self._channel_strips):
                track_offset = offset + index
                if track_offset in xrange(len(tracks)):
                    comp.set_track(tracks[track_offset])
                else:
                    comp.set_track(None)

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ResettingMixerComponent.pyc
