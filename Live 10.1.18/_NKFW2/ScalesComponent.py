# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ScalesComponent.py
# Compiled at: 2017-10-03 17:20:13
from AbstractInstrumentComponent import AbstractInstrumentComponent, subject_slot
from ScaleSettingsComponent import ScaleSettingsComponent
from Scales import CHROMATIC_SCALE
from consts import NUM_TONICS, MIDI_RANGE
from ControlUtils import reset_button, reset_group_buttons, assign_button_to_note
from ClipUtils import get_pitch_range_as_string

class ScalesComponent(AbstractInstrumentComponent):
    """ ScalesComponent works in conjunction with the ScaleSettingsComponent
    to assign scales to a matrix. """

    def __init__(self, scale_settings_component, translation_chs, scroll_button_color='Navigation.OctavesEnabled', handle_modifier_leds=True, target_clip_comp=None, quantize_comp=None, static_offset=36, name='Scale_Control', *a, **k):
        assert isinstance(scale_settings_component, ScaleSettingsComponent)
        assert static_offset in MIDI_RANGE
        super(ScalesComponent, self).__init__(scroll_button_color=scroll_button_color, handle_modifier_leds=handle_modifier_leds, target_clip_comp=target_clip_comp, quantize_comp=quantize_comp, name=name, *a, **k)
        self._settings = scale_settings_component
        self._on_scale_settings_changed.subject = self._settings
        self._translation_channels = translation_chs
        self._matrix = None
        self._note_range = []
        self._static_offset = static_offset
        self._octave_offset = static_offset
        return

    def disconnect(self):
        super(ScalesComponent, self).disconnect()
        self._settings = None
        self._translation_channels = None
        self._matrix = None
        self._note_range = None
        return

    def set_matrix(self, matrix):
        """ Sets the matrix to use for playing scales. The matrix must be
        8 columns wide. """
        self._unused_pads = []
        self._used_pads = []
        matrix_to_reset = matrix if matrix else self._matrix
        reset_group_buttons(matrix_to_reset)
        self._matrix = matrix
        if matrix:
            self._settings.can_change_layout = True
            self._settings.can_change_orientation = matrix.width() == matrix.height()
            self.update()

    def can_scroll_up(self):
        return self._can_scroll_octave(False)

    def can_scroll_down(self):
        return self._can_scroll_octave(True)

    def _can_scroll_octave(self, is_decrease):
        if not self.is_enabled() or not self._note_range:
            return False
        if is_decrease:
            return self._note_range[0] - 12 in MIDI_RANGE
        return self._note_range[1] + 12 in MIDI_RANGE

    def reset(self):
        self._octave_offset = self._static_offset
        self.update()
        self._display_note_range()

    def increment_scroll_position(self, factor):
        """ Extends standard to display note range on changes. """
        super(ScalesComponent, self).increment_scroll_position(factor)
        self._display_note_range()

    def update(self):
        super(ScalesComponent, self).update()
        self._on_scale_settings_changed()

    def _display_note_range(self):
        self.component_message('Note Range', get_pitch_range_as_string(set(self._note_range)))

    @subject_slot('scale_settings')
    def _on_scale_settings_changed(self):
        self._note_range = []
        if self.is_enabled() and self._matrix:
            if self._settings.sequent_layout:
                if self._settings.in_key:
                    all_notes = self._get_sequent_layout()
                else:
                    all_notes = self._get_chromatic_sequent_layout()
            else:
                all_notes = self._get_non_sequent_layout()
            if self._settings.can_change_orientation and self._settings.orientation_is_horizontal:
                all_notes = list(reversed(zip(*all_notes)[::-1]))
            self._assign_notes_to_matrix(all_notes)
            self._scroller.update()

    def _get_non_sequent_layout(self):
        scale = self._settings.scale.intervals if self._settings.in_key else CHROMATIC_SCALE.intervals
        num_intervals = len(scale)
        row_offset = self._settings.row_offset
        all_notes = []
        w, h = self._matrix.width(), self._matrix.height()
        for row in xrange(h):
            current_note_row = []
            interval_offset = row_offset * row
            for col in xrange(w):
                interval_index = col + interval_offset
                octave_offset = interval_index / num_intervals
                note = self._calculate_note(scale[(interval_index % num_intervals)], octave_offset)
                current_note_row.append(note)

            all_notes.append(current_note_row)

        return all_notes

    def _get_sequent_layout(self):
        scale = self._settings.scale.intervals
        num_intervals = len(scale)
        all_notes = []
        w, h = self._matrix.width(), self._matrix.height()
        for row in xrange(h):
            current_note_row = []
            octave_offset = row * 12
            for col in xrange(w):
                if col > num_intervals:
                    note = -1
                elif col == num_intervals:
                    note = octave_offset + scale[0] + 12
                else:
                    note = octave_offset + scale[col]
                current_note_row.append(self._calculate_note(note))

            all_notes.append(current_note_row)

        return all_notes

    def _get_chromatic_sequent_layout(self):
        all_notes = []
        w, h = self._matrix.width(), self._matrix.height()
        for row in xrange(h):
            current_note_row = []
            for col in xrange(w):
                current_note_row.append(self._calculate_note(row * w + col))

            all_notes.append(current_note_row)

        return all_notes

    def _calculate_note(self, interval, octave_offset=0):
        note = interval + octave_offset * 12 + self._octave_offset + self._settings.tonic
        if interval in MIDI_RANGE and note in MIDI_RANGE:
            if len(self._note_range) == 0:
                self._note_range = [
                 note, note]
            else:
                self._note_range[1] = note
            return note
        return -1

    def _assign_notes_to_matrix(self, all_notes):
        """ Sets up the matrix to play the notes of the assigned scale/layout. """
        if self.is_enabled() and self._matrix:
            self._used_pads = []
            self._unused_pads = []
            h = self._matrix.height()
            for btn, (column, row) in self._matrix.iterbuttons():
                if btn:
                    inv_row = h - 1 - row
                    note = all_notes[inv_row][column]
                    if note in MIDI_RANGE:
                        led_value = 'Instrument.Notes.Tonic' if note % NUM_TONICS == self._settings.tonic else 'Instrument.Notes.InKey'
                        interval = (note - self._settings.tonic) % NUM_TONICS
                        if not self._settings.in_key and interval not in self._settings.scale.intervals:
                            led_value = 'Instrument.Notes.OutOfKey'
                        assign_button_to_note(btn, note, channel=self._translation_channels[column], color=led_value)
                        self._used_pads.append(btn)
                    else:
                        reset_button(btn)
                        self._unused_pads.append(btn)

            self.handle_unused_pads()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ScalesComponent.pyc
