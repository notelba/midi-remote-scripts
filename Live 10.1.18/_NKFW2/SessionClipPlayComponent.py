# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SessionClipPlayComponent.py
# Compiled at: 2017-04-24 12:52:35
from functools import partial
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from TrackClipPlayComponent import TrackClipPlayComponent

class SessionClipPlayComponent(CompoundComponent):
    """ SessionClipPlayComponent works with a SlaveManager to manage a group of
    TrackClipPlayComponent. """

    def __init__(self, slave_manager, num_tracks, launch_qntz_comp, move_start, use_scrub=False, qntz_comp=None, scrub_realign_on_release=False, autoname=True, name='Session_Matrix_Clip_Control', *a, **k):
        super(SessionClipPlayComponent, self).__init__(name=name, *a, **k)
        self._num_tracks = num_tracks
        self._use_scrub = bool(use_scrub)
        self._track_components = [ self._create_track_component(i, launch_qntz_comp, move_start, i % 2 != 0, self._use_scrub, scrub_realign_on_release, qntz_comp) for i in xrange(num_tracks)
                                 ]
        if bool(autoname):
            for i, comp in enumerate(self._track_components):
                comp._chop_component.name = '%s_Clip_Chop_Strip' % i
                comp._loop_component.name = '%s_Clip_Loop_Strip' % i
                if self._use_scrub:
                    comp._scrub_component.name = '%s_Clip_Scrub_Strip' % i
                self.register_component(comp)

        self._reassign_tracks.subject = slave_manager
        self._reassign_tracks(slave_manager.track_offset)

    def set_realign_button(self, button):
        """ Sets the realign button to use for the chop and scrub components. """
        for comp in self._track_components:
            comp.set_realign_button(button)

    def __getattr__(self, name):
        """ Override to extract component index to set buttons for. """
        if name.startswith('set_chop_buttons_'):
            return partial(self._set_chop_buttons, int(name[(-1)]))
        if name.startswith('set_scrub_buttons_') and self._use_scrub:
            return partial(self._set_scrub_buttons, int(name[(-1)]))
        if name.startswith('set_loop_buttons_'):
            return partial(self._set_loop_buttons, int(name[(-1)]))

    def _set_chop_buttons(self, index, buttons):
        assert index in xrange(self._num_tracks)
        self._track_components[index].set_chop_buttons(buttons)

    def _set_scrub_buttons(self, index, buttons):
        assert index in xrange(self._num_tracks)
        self._track_components[index].set_scrub_buttons(buttons)

    def _set_loop_buttons(self, index, buttons):
        assert index in xrange(self._num_tracks)
        self._track_components[index].set_loop_buttons(buttons)

    @subject_slot('track_offset')
    def _reassign_tracks(self, offset):
        """ Called when the SessionComponent offset changes to update assigned tracks of
        the TrackChopAndLoopComponent. """
        tracks = self.song().visible_tracks
        for index, comp in enumerate(self._track_components):
            track_offset = offset + index
            if track_offset in xrange(len(tracks)):
                comp.set_track(tracks[track_offset])
            else:
                comp.set_track(None)

        return

    def _create_track_component(self, _, launch_qntz_comp, move_start, use_odd_colors, use_scrub, scrub_realign_on_release, qntz_comp):
        """ Creates a track component to use with this component. This is broken out so
        that it can be overridden.  The first, unused here, arg is the index of the
        component."""
        return TrackClipPlayComponent(launch_qntz_comp, move_start, use_odd_colors, use_scrub=use_scrub, scrub_realign_on_release=scrub_realign_on_release, qntz_comp=qntz_comp, is_private=True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SessionClipPlayComponent.pyc
