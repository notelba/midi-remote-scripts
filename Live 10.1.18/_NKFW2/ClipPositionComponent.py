# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipPositionComponent.py
# Compiled at: 2017-04-24 12:52:35
import Live
from math import modf
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.Util import nop
from ControlUtils import set_group_button_lights, set_group_button_light, is_button_pressed
from consts import MIN_CLIP_LOOP_LENGTH

class ClipPositionComponent(ControlSurfaceComponent):
    """ ClipPositionComponent is the base class for a component that uses
    buttons to affect/reflect the playing position of a clip. """

    def __init__(self, playhead_color='Clip.Playhead.Even', target_clip_comp=None, off_method=nop, *a, **k):
        super(ClipPositionComponent, self).__init__(*a, **k)
        self._position_buttons = None
        self._realign_button = None
        self._clip = None
        self._playhead_value = playhead_color
        self._last_playing_position = -1
        self._on_target_clip_changed.subject = target_clip_comp
        self._off_method = off_method
        return

    def disconnect(self):
        super(ClipPositionComponent, self).disconnect()
        self._position_buttons = None
        self._realign_button = None
        self._clip = None
        self._off_method = None
        return

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, clip):
        self.set_clip(clip)

    def set_clip(self, clip):
        """ Sets the clip to use and sets up listener. """
        assert clip is None or isinstance(clip, Live.Clip.Clip)
        self._clip = clip if clip and (clip.is_midi_clip or clip.warping) else None
        self._on_playing_position_changed.subject = self._clip
        self._on_playing_position_changed()
        return

    def set_position_buttons(self, buttons):
        """ Sets the buttons to use for affecting/reflect playing position. """
        self._position_buttons = list(buttons) if buttons else None
        self._on_position_buttons_value.replace_subjects(buttons or [])
        self._clear_position_buttons()
        return

    def set_realign_button(self, button):
        """ Sets the realign modifier to use. """
        self._realign_button = button

    @subject_slot_group('value')
    def _on_position_buttons_value(self, value, button):
        """ Calculates the position within the clip that is associated with the given
        button and calls overridable methods to handle performing the position action.
        If the realign button is pressed, this will realign the clip's playing position
        with that of the song. """
        if self.is_enabled() and self._clip:
            if value:
                if is_button_pressed(self._realign_button):
                    self.realign_playing_position()
                else:
                    start_offset = 0.0 + int(self._clip.looping) * self._clip.loop_start
                    btn_pos = (self._clip.loop_end - start_offset) / len(self._position_buttons) * self._position_buttons.index(button) + start_offset
                    end = self._clip.loop_end
                    if self._clip.looping and end > self._clip.end_marker:
                        end = self._clip.end_marker
                    if 0.0 <= btn_pos <= end - MIN_CLIP_LOOP_LENGTH:
                        self.perform_position_action(btn_pos)
            else:
                self._off_method()

    def perform_position_action(self, position):
        """ Called when a button is pressed, a clip is present and the associated position
        is usable. To be overridden to perform the required action. """
        raise NotImplementedError

    def realign_playing_position(self):
        """ Realign the clip's playing position with that of the song. """
        clip_fraction, clip_beat = modf(self._clip.playing_position)
        clip_fraction = float('%.4f' % clip_fraction)
        clip_beat = int(clip_beat) % self.song().signature_numerator
        song_fraction, song_beat = modf(self.song().current_song_time)
        song_fraction = float('%.4f' % song_fraction)
        song_beat = int(song_beat) % self.song().signature_numerator
        diff_fraction = song_fraction - clip_fraction
        diff_beat = song_beat - clip_beat
        self._clip.move_playing_pos(diff_beat + diff_fraction)

    def update(self):
        super(ClipPositionComponent, self).update()
        self._clear_position_buttons()
        self.set_clip(self._clip)

    def _clear_position_buttons(self):
        if self.is_enabled() and self._position_buttons:
            set_group_button_lights(self._position_buttons, 'DefaultButton.Off')

    @subject_slot('playing_position')
    def _on_playing_position_changed(self):
        """ Updates button LEDs to reflect playhead position. """
        if self.is_enabled() and self._position_buttons:
            if self._clip:
                num_buttons = len(self._position_buttons)
                if (self._clip.is_playing or self._clip.is_triggered) and self._clip.loop_start <= self._clip.playing_position <= self._clip.loop_end:
                    start_offset = 0.0 + int(self._clip.looping) * self._clip.loop_start
                    position = int((self._clip.playing_position - start_offset) / ((self._clip.loop_end - start_offset) / num_buttons))
                    if position in xrange(num_buttons) and position != self._last_playing_position:
                        set_group_button_light(self._position_buttons, self._last_playing_position, 'DefaultButton.Off')
                        set_group_button_light(self._position_buttons, position, self._playhead_value)
                        self._last_playing_position = position
                else:
                    set_group_button_light(self._position_buttons, self._last_playing_position, 'DefaultButton.Off')
            else:
                set_group_button_lights(self._position_buttons, 'Clip.NoClip')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipPositionComponent.pyc
