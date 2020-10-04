# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackClipPlayComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.SubjectSlot import subject_slot
from ClipComponent import TrackClipComponent
from ClipChopComponent import ClipChopComponent
from ClipScrubComponent import ClipScrubComponent
from ClipLoopComponent import ClipLoopComponent
from ClipPitchComponent import ClipPitchComponent

class TrackClipPlayComponent(TrackClipComponent):
    """ TrackClipComponent that contains a chop and loop component as well as an optional
    scrub and pitch component. """

    def __init__(self, launch_qntz_comp, move_start, use_odd_colors, use_scrub=False, use_pitch=False, scrub_realign_on_release=False, qntz_comp=None, *a, **k):
        super(TrackClipPlayComponent, self).__init__(qntz_comp, *a, **k)
        self._chop_component = self._create_chop_component(launch_qntz_comp, use_odd_colors)
        self._loop_component = self._create_loop_component(move_start, use_odd_colors)
        self._scrub_component = None
        if bool(use_scrub):
            self._scrub_component = self._create_scrub_component(use_odd_colors, scrub_realign_on_release)
            self.register_components(self._scrub_component)
        self._pitch_component = None
        if bool(use_pitch):
            self._pitch_component = self._create_pitch_component(launch_qntz_comp)
            self.register_component(self._pitch_component)
        self.register_components(self._chop_component, self._loop_component)
        return

    @subject_slot('target_track')
    def set_track(self, track):
        """ Extends standard to set track for pitch component. """
        super(TrackClipPlayComponent, self).set_track(track)
        if self._pitch_component:
            self._pitch_component.set_track(track)

    def on_clip_changed(self):
        """ Sets the clip for the sub-components. """
        clip = self.clip
        self._chop_component.set_clip(clip)
        self._loop_component.set_clip(clip)
        if self._scrub_component:
            self._scrub_component.set_clip(clip)
        if self._pitch_component:
            self._pitch_component.set_clip(clip)

    def set_chop_buttons(self, buttons):
        """ Sets the buttons to use for the chop component. """
        self._chop_component.set_position_buttons(buttons)

    def set_scrub_buttons(self, buttons):
        """ Sets the buttons to use for the scrub component. """
        if self._scrub_component:
            self._scrub_component.set_position_buttons(buttons)

    def set_loop_buttons(self, buttons):
        """ Sets the buttons to use for the loop component. """
        self._loop_component.set_loop_buttons(buttons)

    def set_pitch_buttons(self, buttons):
        """ Sets the buttons to use for the pitch component. """
        if self._pitch_component:
            self._pitch_component.set_pitch_matrix(buttons)

    def set_realign_button(self, button):
        """ Sets the realign button to use for the chop and scrub components. """
        self._chop_component.set_realign_button(button)
        if self._scrub_component:
            self._scrub_component.set_realign_button(button)

    def set_select_button(self, button):
        """ Sets the select button to use for the pitch component. """
        if self._pitch_component:
            self._pitch_component.set_select_button(button)

    def set_legato_button(self, button):
        """ Sets the legato button to use for the pitch component. """
        if self._pitch_component:
            self._pitch_component.set_legato_button(button)

    def set_use_odd_colors(self, use_odd_colors):
        """ Sets whether or not to use odd colors to with the loop component. """
        self._loop_component.set_use_odd_colors(use_odd_colors)

    def _create_chop_component(self, launch_qntz_comp, use_odd_colors):
        """ Returns the created chop component.  Broken out for extension. """
        color = 'Clip.Playhead.Odd' if use_odd_colors else 'Clip.Playhead.Even'
        return ClipChopComponent(launch_qntz_comp, playhead_color=color)

    def _create_scrub_component(self, use_odd_colors, scrub_realign_on_release):
        """ Returns the created scrub component.  Broken out for extension. """
        color = 'Clip.Scrubhead.Odd' if use_odd_colors else 'Clip.Scrubhead.Even'
        return ClipScrubComponent(playhead_color=color, realign_on_release=scrub_realign_on_release)

    def _create_loop_component(self, move_start, use_odd_colors):
        """ Returns the created loop component.  Broken out for extension. """
        return ClipLoopComponent(move_start, False, use_odd_colors=use_odd_colors)

    def _create_pitch_component(self, launch_qntz_comp):
        """ Returns the created pitch component.  Broken out for extension. """
        return ClipPitchComponent(launch_qntz_comp)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackClipPlayComponent.pyc
