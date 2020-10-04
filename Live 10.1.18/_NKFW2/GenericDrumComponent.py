# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\GenericDrumComponent.py
# Compiled at: 2017-03-07 13:28:52
from AbstractInstrumentComponent import AbstractInstrumentComponent
from ControlUtils import reset_group_buttons, assign_button_to_note
from ClipUtils import get_pitch_range_as_string
from consts import MIDI_RANGE
WIDTH = 4
MAX_WIDTH = WIDTH * 2
MIN_NOTE = 4

class GenericDrumComponent(AbstractInstrumentComponent):
    """ GenericDrumComponent sets up a matrix for playing a generic drum instrument. """

    def __init__(self, translation_ch=0, invert_rows=True, start_note=36, scroll_button_color='Navigation.DrumRackEnabled', handle_modifier_leds=True, targets_comp=None, quantize_comp=None, octave_size=32, name='Generic_Drum_Control', *a, **k):
        super(GenericDrumComponent, self).__init__(name=name, scroll_button_color=scroll_button_color, handle_modifier_leds=handle_modifier_leds, target_clip_comp=targets_comp, quantize_comp=quantize_comp, octave_size=octave_size, *a, **k)
        self._translation_channel = translation_ch
        self._invert_rows = bool(invert_rows)
        self._start_note = start_note
        self._current_start_note = start_note
        self._highest_note = start_note
        self._num_buttons = octave_size
        self._row_xrange = None
        self._matrix = None
        return

    def disconnect(self):
        super(GenericDrumComponent, self).disconnect()
        self._row_xrange = None
        self._matrix = None
        return

    def set_matrix(self, matrix):
        """ Sets the matrix to use for playing drum instruments. """
        self._used_pads = []
        matrix_to_reset = matrix if matrix else self._matrix
        reset_group_buttons(matrix_to_reset)
        self._matrix = matrix
        if matrix:
            if self._invert_rows:
                self._row_xrange = xrange(matrix.height() - 1, -1, -1)
            else:
                self._row_xrange = xrange(matrix.height())
            self._num_buttons = len(matrix)
            self._update_all_pad_settings()

    def can_scroll_up(self):
        return self._can_scroll_octave(False)

    def can_scroll_down(self):
        return self._can_scroll_octave(True)

    def _can_scroll_octave(self, is_decrease):
        if not self.is_enabled():
            return False
        else:
            if is_decrease:
                return self._current_start_note > MIN_NOTE
            return self._num_buttons + self._current_start_note + self._octave_size in MIDI_RANGE

    def reset(self):
        self._octave_offset = 0
        self.update()
        self._display_note_range()

    def increment_scroll_position(self, factor):
        """ Extends standard to display note range on changes. """
        super(GenericDrumComponent, self).increment_scroll_position(factor)
        self._display_note_range()

    def update(self):
        super(GenericDrumComponent, self).update()
        self._update_all_pad_settings()

    def _display_note_range(self):
        self.component_message('Note Range', get_pitch_range_as_string((self._current_start_note,
         self._highest_note)))

    def _update_all_pad_settings(self):
        self._used_pads = []
        if self.is_enabled() and self._matrix:
            last_id = self._start_note + self._octave_offset
            self._current_start_note = last_id
            has_side_by_side = self._matrix.width() == MAX_WIDTH
            for row in self._row_xrange:
                for col in xrange(WIDTH):
                    self._update_pad_settings(row, col, last_id)
                    last_id += 1

            if has_side_by_side:
                for row in self._row_xrange:
                    for col in xrange(WIDTH, MAX_WIDTH):
                        self._update_pad_settings(row, col, last_id)
                        last_id += 1

            self._highest_note = last_id - 1

    def _update_pad_settings(self, row, column, identifier_to_set):
        pad = self._matrix.get_button(column, row)
        if pad:
            lower_rows = row in xrange(4)
            lower_cols = column in xrange(4)
            if lower_rows:
                color = 'GenericDrum.Quad_0' if lower_cols else 'GenericDrum.Quad_1'
            else:
                color = 'GenericDrum.Quad_2' if lower_cols else 'GenericDrum.Quad_3'
            assign_button_to_note(pad, identifier_to_set, channel=self._translation_channel, color=color)
            self._used_pads.append(pad)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/GenericDrumComponent.pyc
