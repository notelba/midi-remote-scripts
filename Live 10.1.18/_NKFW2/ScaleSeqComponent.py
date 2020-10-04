# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ScaleSeqComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.SubjectSlot import subject_slot
from PolySeqComponent import PolySeqComponent
from ScaleSettingsComponent import ScaleSettingsComponent
from ResettableScrollComponent import ResettableScrollComponent, ResettableScrollable
from Scales import CHROMATIC_SCALE
from consts import MIDI_RANGE
from ControlUtils import skin_scroll_component
from ClipUtils import get_pitch_list, get_pitch_range_as_string

class ScaleSeqComponent(PolySeqComponent, ResettableScrollable):
    """ ScaleSeqComponent is a PolySeqComponent that uses scale quantization. """

    def __init__(self, scale_settings_component, *a, **k):
        if not isinstance(scale_settings_component, ScaleSettingsComponent):
            raise AssertionError
            name = k.pop('name', 'Scale_Sequence_Control')
            k['name'] = name
            self._static_offset = k.pop('static_offset', 60)
            self._use_tonic_colors = k.pop('use_tonic_colors', True)
            super(ScaleSeqComponent, self).__init__(*a, **k)
            self._fold_button = None
            self._current_notes = []
            self._folded_notes = []
            self._highest_note = 0
            self._semi_offset = 0
            self._folded_offset = 0
            self._is_folded = False
            self._settings = scale_settings_component
            self._on_scale_settings_changed.subject = self._settings
            prefer_playing = k.get('prefer_playing_clip', False)
            self.on_target_clip_changed.subject = prefer_playing or k.get('targets_comp', None)
        self._scroller = self.register_component(ResettableScrollComponent(self))
        skin_scroll_component(self._scroller, color='Navigation.OctaveEnabled')
        return

    def disconnect(self):
        super(ScaleSeqComponent, self).disconnect()
        self._fold_button = None
        self._settings = None
        self._current_notes = None
        self._folded_notes = None
        return

    def on_clip_changed(self):
        """ Sets the clip to observe for note changes and updates fold button. """
        self._on_notes_changed.subject = self._clip
        self._update_fold_button()

    @subject_slot('target_clip')
    def on_target_clip_changed(self, clip):
        """ Sets the clip to use for fold function.  This is only used when not
        prefer_playing_clip. """
        self._clip = clip if clip and clip.is_midi_clip else None
        self.on_clip_changed()
        return

    def set_fold_button(self, button):
        """ Sets the button to use for folding/unfolding notes. """
        self._fold_button = button
        self._on_fold_button_value.subject = button
        self._update_fold_button()

    def _set_sequence_buttons(self, index, buttons):
        """ Extends standard to update scale settings on first or last set of buttons
        are set. """
        super(ScaleSeqComponent, self)._set_sequence_buttons(index, buttons)
        if buttons and (index == 0 or index == self._num_note_lanes - 1):
            self._settings.can_change_layout = False
            self._on_scale_settings_changed(is_internal_call=True)

    def set_scroll_down_button(self, button):
        """ Sets the button to use for scrolling down. """
        self._scroller.set_scroll_down_button(button)

    def set_scroll_up_button(self, button):
        """ Sets the button to use for scrolling up. """
        self._scroller.set_scroll_up_button(button)

    def can_scroll_up(self):
        return self._can_scroll_octave(False)

    def can_scroll_down(self):
        return self._can_scroll_octave(True)

    def _can_scroll_octave(self, is_decrease):
        if not self.is_enabled() or not self._current_notes:
            return False
        if self._is_folded:
            if is_decrease:
                return self._folded_offset != 0
            return self._folded_offset + 1 <= len(self._folded_notes) - self._num_note_lanes
        if is_decrease:
            return self._current_notes[0] != 0
        return self._highest_note + 1 in MIDI_RANGE

    def scroll_up(self):
        self._increment_scroll_position(1)

    def scroll_down(self):
        self._increment_scroll_position(-1)

    def reset(self):
        self._semi_offset = 0
        self._folded_offset = 0
        self._on_scale_settings_changed(is_internal_call=True, should_display=True)

    def _increment_scroll_position(self, factor):
        is_decrease = factor < 0
        if self._can_scroll_octave(is_decrease):
            if self._is_folded:
                self._folded_offset += -1 if is_decrease else 1
            else:
                self._semi_offset += -1 if is_decrease else 1
            self._on_scale_settings_changed(is_internal_call=True, should_display=True)

    @subject_slot('value')
    def _on_fold_button_value(self, value):
        if value and (self._can_fold() or self._is_folded):
            self._folded_offset = 0
            self._is_folded = not self._is_folded
            self._on_scale_settings_changed(is_internal_call=True, should_display=True)

    def _can_fold(self):
        return len(get_pitch_list(self._clip)) > 1

    def update(self):
        super(ScaleSeqComponent, self).update()
        self._on_scale_settings_changed(is_internal_call=True)
        self._update_fold_button()

    @subject_slot('notes')
    def _on_notes_changed(self):
        if not self._is_folded:
            self._update_fold_button()

    @subject_slot('scale_settings')
    def _on_scale_settings_changed(self, is_internal_call=False, should_display=False):
        self._current_notes = []
        if self.is_enabled():
            if not is_internal_call or not self._is_folded:
                self._assign_to_scale_intervals()
            else:
                self._assign_to_clip_notes()
            self._scroller.update()
            self._update_fold_button()
            if should_display:
                self.component_message('Note Range', get_pitch_range_as_string(self._current_notes))

    def _assign_to_scale_intervals(self):
        intervals_to_use = self._settings.scale.intervals if self._settings.in_key else CHROMATIC_SCALE.intervals
        scale_len = len(intervals_to_use)
        for i, lane in enumerate(self._note_lane_components):
            interval_index = i + self._semi_offset
            octave_offset = 0
            if interval_index not in xrange(scale_len):
                octave_offset = interval_index / scale_len * 12
                interval_index %= scale_len
            note = intervals_to_use[interval_index] + self._settings.tonic + octave_offset + self._static_offset
            if note not in MIDI_RANGE:
                note = -1
            else:
                self._highest_note = note
            self._current_notes.append(note)
            lane.set_note(note, is_tonic=self._use_tonic_colors and note % 12 == self._settings.tonic)

    def _assign_to_clip_notes(self):
        self._folded_notes = get_pitch_list(self._clip)
        notes_len = len(self._folded_notes)
        start_offset = self._folded_offset
        for i, lane in enumerate(self._note_lane_components):
            index = i + start_offset
            if index < notes_len:
                note = self._folded_notes[index]
            else:
                note = -1
            self._current_notes.append(note)
            lane.set_note(note)

    def _update_fold_button(self):
        if self.is_enabled() and self._fold_button:
            if not self._is_folded and not self._can_fold():
                self._fold_button.set_light('DefaultButton.Off')
            else:
                self._fold_button.set_light('Sequence.Fold.On' if self._is_folded else 'Sequence.Fold.Off')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ScaleSeqComponent.pyc
