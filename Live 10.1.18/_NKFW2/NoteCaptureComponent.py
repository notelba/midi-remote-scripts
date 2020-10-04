# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\NoteCaptureComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.SubjectSlot import subject_slot
from AbstractInstrumentComponent import AbstractInstrumentComponent
from SpecialControl import SpecialButtonControl
from ControlUtils import reset_button, reset_group_buttons, assign_button_to_note, is_button_pressed
from ClipUtils import get_pitch_list, pitch_is_sharp, get_pitch_range_as_string
from consts import MIDI_RANGE

class NoteCaptureComponent(AbstractInstrumentComponent):
    """ NoteCaptureComponent sets up a matrix for playing notes captured from MIDI clips.
    Clips need to contain at least two notes to be captured from. """
    capture_button = SpecialButtonControl(color='Global.CannotCapture', on_color='Global.CanCapture')

    def __init__(self, translation_ch=0, scroll_button_color='Navigation.OctavesEnabled', handle_modifier_leds=True, targets_comp=None, quantize_comp=None, name='Note_Capture_Control', *a, **k):
        super(NoteCaptureComponent, self).__init__(scroll_button_color=scroll_button_color, handle_modifier_leds=handle_modifier_leds, target_clip_comp=targets_comp, quantize_comp=quantize_comp, name=name, *a, **k)
        self._translation_channel = translation_ch
        self._matrix = None
        self._num_buttons = 0
        self._captured_notes = None
        return

    def disconnect(self):
        super(NoteCaptureComponent, self).disconnect()
        self._matrix = None
        self._captured_notes = None
        return

    def set_clip(self, clip):
        """ Extends standard to update capture button LED. """
        super(NoteCaptureComponent, self).set_clip(clip)
        self._update_capture_button()

    def set_matrix(self, matrix):
        """ Sets the matrix to use for playing captured notes. """
        self._unused_pads = []
        self._used_pads = []
        matrix_to_reset = matrix if matrix else self._matrix
        reset_group_buttons(matrix_to_reset)
        self._matrix = matrix
        if matrix:
            self._num_buttons = matrix.width() * matrix.height()
            self._assign_notes_to_matrix()

    def can_scroll_up(self):
        return self._can_scroll_octave(False)

    def can_scroll_down(self):
        return self._can_scroll_octave(True)

    def _can_scroll_octave(self, is_decrease):
        if not self.is_enabled() or not self._captured_notes:
            return False
        factor = 1 if is_button_pressed(self._shift_button) else 12
        if is_decrease:
            return self._captured_notes[0] - factor + self._octave_offset in MIDI_RANGE
        return self._captured_notes[(-1)] + factor + self._octave_offset in MIDI_RANGE

    def reset(self):
        self._octave_offset = 0
        self.update()
        self._display_note_range()

    def increment_scroll_position(self, factor):
        if not is_button_pressed(self._shift_button):
            factor *= 12
        if self._can_scroll_octave(factor < 0):
            self._octave_offset += factor
            self.update()
            self._display_note_range()

    @capture_button.pressed
    def capture_button(self, _):
        self.capture_from_clip()

    def capture_from_clip(self):
        """ Captures notes from the current clip and assigns them to the matrix. """
        if self._clip and self._num_buttons:
            notes = get_pitch_list(self._clip)
            if len(notes) > 1:
                self._octave_offset = 0
                self._captured_notes = notes[:self._num_buttons]
                self.update()
                self._display_note_range()

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        self._scroller.update()

    def update(self):
        super(NoteCaptureComponent, self).update()
        self._assign_notes_to_matrix()
        self._update_capture_button()

    def _display_note_range(self):
        nr = (
         self._captured_notes[0] + self._octave_offset,
         self._captured_notes[(-1)] + self._octave_offset)
        self.component_message('Note Range', get_pitch_range_as_string(nr))

    def _assign_notes_to_matrix(self):
        if self.is_enabled() and self._matrix:
            self._used_pads = []
            self._unused_pads = []
            if self._captured_notes:
                num_notes = len(self._captured_notes)
                w, h = self._matrix.width(), self._matrix.height()
                for btn, (column, row) in self._matrix.iterbuttons():
                    if btn:
                        inv_row = h - 1 - row
                        note_index = inv_row * w + column
                        if note_index in xrange(num_notes):
                            note = self._captured_notes[note_index] + self._octave_offset
                            color = 'Instrument.Notes.Sharp' if pitch_is_sharp(note) else 'Instrument.Notes.Natural'
                            assign_button_to_note(btn, note, channel=self._translation_channel, color=color)
                            self._used_pads.append(btn)
                        else:
                            reset_button(btn)
                            self._unused_pads.append(btn)

            else:
                reset_group_buttons(self._matrix)
                self._unused_pads = self._matrix
            self.handle_unused_pads()

    def _update_capture_button(self):
        self.capture_button.is_on = self._clip is not None
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/NoteCaptureComponent.pyc
