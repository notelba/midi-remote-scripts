# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SimplerComponent.py
# Compiled at: 2017-03-07 13:28:53
import Live
from AbstractInstrumentComponent import AbstractInstrumentComponent, subject_slot, subject_slot_group
from consts import MIDI_RANGE, SIMPLER_START_NOTE
from ControlUtils import is_button_pressed, reset_button, reset_group_buttons, assign_button_to_note
WIDTH = 4
MAX_WIDTH = WIDTH * 2

class SimplerComponent(AbstractInstrumentComponent):
    """ SimplerComponent allows a matrix to be used for playing slices
    in Simpler.

    This utilizes several modifiers as well as modifier combinations most of which
    are covered in AbstractInstrumentComponent:
    Select + pad =     Select slice (Shift + Pad if Select is not present) """
    __subject_events__ = ('selected_note', )

    def __init__(self, slice_ch, scroll_button_color='Navigation.SimplerEnabled', handle_modifier_leds=True, targets_comp=None, quantize_comp=None, name='Simpler_Control', *a, **k):
        super(SimplerComponent, self).__init__(scroll_button_color=scroll_button_color, handle_modifier_leds=handle_modifier_leds, target_clip_comp=targets_comp, quantize_comp=quantize_comp, name=name, octave_size=4, *a, **k)
        self._slice_channel = slice_ch
        self._matrix = None
        self._simpler = None
        self._on_target_simpler_changed.subject = targets_comp
        self._row_xrange = None
        self._num_slices = 0
        self._num_note_controls = 0
        self._selected_slice_index = -1
        return

    def disconnect(self):
        super(SimplerComponent, self).disconnect()
        self._matrix = None
        self._simpler = None
        self._row_xrange = None
        return

    @property
    def selected_note(self):
        """ Returns the note associated with the selected slice or 0. """
        if self._selected_slice_index != -1:
            return self._selected_slice_index + SIMPLER_START_NOTE + self._octave_offset
        return 0

    def set_simpler(self, simpler):
        """ Sets the Simpler to play/control and sets up all listeners. """
        self._selected_slice_index = -1
        self._simpler = simpler
        self._on_sample_changed.subject = simpler or None
        self._on_playback_mode_changed.subject = simpler or None
        self._on_selected_slice_changed.subject = simpler.view if simpler else None
        self._on_sample_changed()
        return

    def set_matrix(self, matrix):
        """ Sets the matrix to use for playing Simpler. The matrix must be
        at least 4 wide. """
        assert matrix is None or matrix.width() >= WIDTH
        matrix_to_reset = matrix if matrix else self._matrix
        reset_group_buttons(matrix_to_reset)
        self._matrix = matrix
        if matrix:
            self._num_note_controls = len(list(matrix))
            self._row_xrange = xrange(matrix.height() - 1, -1, -1)
            self.set_simpler(self._simpler)
        return

    def can_scroll_up(self):
        return self._can_scroll_octave(False)

    def can_scroll_down(self):
        return self._can_scroll_octave(True)

    def reset(self):
        self._reset_slices_and_octave()
        self.update()
        self._display_slice_range()

    def increment_scroll_position(self, factor):
        """ Extends standard to display slice range on changes. """
        super(SimplerComponent, self).increment_scroll_position(factor)
        self._display_slice_range()

    def should_enable_scroller(self):
        return self._is_slicing()

    def _can_scroll_octave(self, is_decrease):
        if self._is_slicing() and self._num_note_controls < self._num_slices:
            if is_decrease:
                return self._octave_offset > 0
            else:
                return self._num_slices - self._num_note_controls - self._octave_offset > 0

        return False

    def _reset_slices_and_octave(self):
        self._num_slices = 0
        self._octave_offset = 0

    def _display_slice_range(self):
        if self._used_pads:
            start = SIMPLER_START_NOTE
            s_range = '%s - %s' % (self._used_pads[0].message_identifier() - start + 1,
             self._used_pads[(-1)].message_identifier() - start + 1)
            self.component_message('Slice Range', s_range)

    @subject_slot_group('value')
    def on_used_pad_value(self, value, button):
        if self._is_slicing():
            if is_button_pressed(self._delete_button):
                self.handle_note_delete(value != 0, button.message_identifier())
            elif value:
                if self.select_pressed():
                    pad_idx = self._used_pads.index(button) + self._octave_offset
                    if pad_idx < self._num_slices:
                        self._simpler.view.selected_slice = self._simpler.sample.slices[pad_idx]
                elif is_button_pressed(self._quantize_button):
                    self.handle_note_quantize()

    @subject_slot('target_simpler')
    def _on_target_simpler_changed(self, simpler):
        self.set_simpler(simpler)

    @subject_slot('sample')
    def _on_sample_changed(self):
        """ Sets the Simpler sample to play/control and sets up all listeners. """
        self._reset_slices_and_octave()
        self._selected_slice_index = -1
        sample = None
        if self._simpler and self._simpler.sample:
            sample = self._simpler.sample
            if self._simpler.view.selected_slice in sample.slices:
                self._selected_slice_index = sample.slices.index(self._simpler.view.selected_slice)
            self.notify_selected_note(self.selected_note)
        self._on_slices_changed.subject = sample
        self.update()
        return

    @subject_slot('slices')
    def _on_slices_changed(self):
        if self._is_slicing():
            new_num_slices = len(self._simpler.sample.slices)
            if self._num_slices != new_num_slices:
                self._reset_slices_and_octave()
                self.update()

    @subject_slot('playback_mode')
    def _on_playback_mode_changed(self):
        self.update()

    @subject_slot('selected_slice')
    def _on_selected_slice_changed(self):
        if self._is_slicing():
            if self._simpler.view.selected_slice in self._simpler.sample.slices:
                self._selected_slice_index = self._simpler.sample.slices.index(self._simpler.view.selected_slice)
                self.notify_selected_note(self.selected_note)
            self._update_slice_pad_leds()

    def _is_slicing(self):
        return self._simpler is not None and self._simpler.sample and self._simpler.playback_mode == Live.SimplerDevice.PlaybackMode.slicing

    def update(self):
        if self._is_slicing():
            self._num_slices = len(self._simpler.sample.slices)
        super(SimplerComponent, self).update()
        self._update_all_slice_pad_settings()
        self._update_slice_pad_leds()

    def _update_all_slice_pad_settings(self):
        if self.is_enabled() and self._matrix:
            self._unused_pads = []
            self._used_pads = []
            if self._is_slicing():
                last_id = SIMPLER_START_NOTE + self._octave_offset
                has_side_by_side = self._matrix.width() == MAX_WIDTH
                for row in self._row_xrange:
                    for col in xrange(WIDTH):
                        self._update_slice_pad_settings(row, col, last_id)
                        last_id += 1

                if has_side_by_side:
                    for row in self._row_xrange:
                        for col in xrange(WIDTH, MAX_WIDTH):
                            self._update_slice_pad_settings(row, col, last_id)
                            last_id += 1

            else:
                reset_group_buttons(self._matrix)
                self._unused_pads = self._matrix
        self.handle_unused_pads()

    def _update_slice_pad_settings(self, row, column, identifier_to_set):
        pad = self._matrix.get_button(column, row)
        if pad:
            if identifier_to_set in MIDI_RANGE:
                assign_button_to_note(pad, identifier_to_set, channel=self._slice_channel, force_next=False)
                self._used_pads.append(pad)
            else:
                reset_button(pad)
                self._unused_pads.append(pad)

    def _update_slice_pad_leds(self):
        if self.is_enabled() and self._matrix:
            for pad in self._matrix:
                if pad and pad in self._used_pads:
                    num_slice = pad.message_identifier() - SIMPLER_START_NOTE
                    pad.force_next_send()
                    value = 'Simpler.SlicePad' if num_slice < self._num_slices else 'Simpler.SlicePadEmpty'
                    pad.set_light('Simpler.SlicePadSelected' if num_slice == self._selected_slice_index else value)
                else:
                    pad.set_light('DefaultButton.Off')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SimplerComponent.pyc
