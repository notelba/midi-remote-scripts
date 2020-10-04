# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\NoteLaneComponent.py
# Compiled at: 2017-07-03 23:51:28
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group, CallableSubjectSlotGroup
from _Framework.Util import nop
from ClipUtils import get_notes_at_position, create_sequence_clip, NOTE_VELO, NOTE_LENGTH, NOTE_MUTED, NOTE_PITCH, NOTE_TIME
from ControlUtils import set_group_button_lights, reset_group_buttons, get_group_buttons_pressed
VELO_HIGH_START = 86
VELO_MID_START = 43
EVEN_STEP_COLORS = ('Sequence.Step.Even.OnLow', 'Sequence.Step.Even.OnMid', 'Sequence.Step.Even.OnHigh')
ODD_STEP_COLORS = ('Sequence.Step.Odd.OnLow', 'Sequence.Step.Odd.OnMid', 'Sequence.Step.Odd.OnHigh')
TONIC_STEP_COLORS = ('Sequence.Step.Tonic.OnLow', 'Sequence.Step.Tonic.OnMid', 'Sequence.Step.Tonic.OnHigh')

class NoteLaneComponent(ControlSurfaceComponent):
    """ NoteLaneComponent provides step-sequencing capabilities for a single note
    lane in a clip. """

    def __init__(self, num_steps, row_width, note=36, channel=0, enumerate_ids=False, use_odd_colors=False, resolution_comp=None, page_comp=None, note_comp=None, velo_comp=None, targets_comp=None, *a, **k):
        super(NoteLaneComponent, self).__init__(*a, **k)
        self.is_private = True
        self._original_num_steps = num_steps
        self._num_steps = num_steps
        self._row_width = row_width
        self._note = note_comp.selected_note if note_comp else note
        self._channel = channel
        self._enumerate_ids = enumerate_ids
        self._clip = None
        self._track = None
        self._current_lane = None
        self._resolution = resolution_comp.resolution if resolution_comp else 0.25
        self._is_triplet = False
        self._row_triplet_cutoff = 6 if row_width == 8 else 3
        self._start_time = 0.0
        self._step_colors = ODD_STEP_COLORS if use_odd_colors else EVEN_STEP_COLORS
        self._use_odd_colors = use_odd_colors
        self._original_sequence_buttons = []
        self._sequence_buttons = []
        self._unused_sequence_buttons = []
        self._unused_sequence_listener = self.register_slot_manager(CallableSubjectSlotGroup(event='value', listener=nop, function=nop))
        self._velocity_component = velo_comp
        self.set_clip.subject = targets_comp
        self.set_track.subject = targets_comp
        self.set_resolution.subject = resolution_comp
        self.set_start_time.subject = page_comp
        self.set_note.subject = note_comp
        return

    def disconnect(self):
        super(NoteLaneComponent, self).disconnect()
        self._clip = None
        self._track = None
        self._current_lane = None
        self._step_colors = None
        self._original_sequence_buttons = None
        self._sequence_buttons = None
        self._unused_sequence_buttons = None
        self._unused_sequence_listener = None
        self._velocity_component = None
        return

    def set_note_component(self, component):
        """ Sets the component to use for determining the note to sequence. The component
        must have an observable selected_note property. """
        self.set_note.subject = component
        if component:
            self._note = component.selected_note
        self._on_notes_changed()

    @subject_slot('selected_note')
    def set_note(self, note, is_tonic=False):
        """ Sets the note number to sequence as well as the step colors to use based
        on whether the note is the tonic note. """
        self._note = note
        if is_tonic:
            self._step_colors = TONIC_STEP_COLORS
        else:
            self._step_colors = ODD_STEP_COLORS if self._use_odd_colors else EVEN_STEP_COLORS
        self._on_notes_changed()

    @subject_slot('target_clip')
    def set_clip(self, clip):
        """ Sets the clip to sequence into. """
        self._current_lane = None
        self._start_time = 0.0
        self._clip = clip if clip and clip.is_midi_clip else None
        self._on_notes_changed.subject = self._clip
        self._on_notes_changed()
        return

    @subject_slot('target_track')
    def set_track(self, track):
        """ Sets the track associated with the clip. This is needed for creating new
        clips. """
        self._track = track if track and track.has_midi_input else None
        return

    @subject_slot('resolution')
    def set_resolution(self, resolution, is_triplet=None):
        """ Sets the resolution to use for sequencing. """
        self._is_triplet = is_triplet if is_triplet is not None else self.set_resolution.subject.is_triplet
        self._num_steps = self._original_num_steps
        if self._is_triplet:
            self._num_steps -= self._original_num_steps / 4
        self._resolution = resolution
        self._refresh_sequence_button_observers()
        return

    @subject_slot('start_time')
    def set_start_time(self, time):
        """ Sets the time to start sequencing from. """
        self._start_time = time
        self._on_notes_changed()

    def set_sequence_buttons(self, buttons):
        """ Sets the buttons to use for sequencing. """
        matrix_to_reset = buttons if buttons else self._original_sequence_buttons
        self._original_sequence_buttons = list(buttons) if buttons else []
        reset_group_buttons(matrix_to_reset)
        self._refresh_sequence_button_observers()

    def _refresh_sequence_button_observers(self):
        self._sequence_buttons = []
        self._unused_sequence_buttons = []
        if self._original_sequence_buttons:
            for index, button in enumerate(self._original_sequence_buttons):
                if button:
                    if self._is_triplet and index % self._row_width >= self._row_triplet_cutoff:
                        self._unused_sequence_buttons.append(button)
                    else:
                        button.set_channel(self._channel)
                        if self._enumerate_ids:
                            button.set_identifier(index)
                        self._sequence_buttons.append(button)

        if self._unused_sequence_listener:
            self._unused_sequence_listener.replace_subjects(self._unused_sequence_buttons)
        self._on_sequence_button_value.replace_subjects(self._sequence_buttons)
        self._on_notes_changed()

    @subject_slot_group('value')
    def _on_sequence_button_value(self, value, _):
        if self._track and value and self._note != -1:
            pressed = get_group_buttons_pressed(self._sequence_buttons)
            start = pressed[0] * self._resolution + self._start_time
            length = self._resolution
            if len(pressed) == 2:
                length = self._resolution * (pressed[1] - pressed[0] + 1)
            current_notes = get_notes_at_position(self._current_lane, start, length)
            if current_notes and len(pressed) == 1:
                for note in current_notes:
                    self._clip.remove_notes(note[NOTE_TIME], note[NOTE_PITCH], note[NOTE_LENGTH], 1)

            else:
                velo = 100
                if self._velocity_component:
                    velo = self._velocity_component.get_velocity(value)
                note = (
                 self._note, start, length, velo, False)
                if self._clip:
                    self._clip.set_notes((note,))
                else:
                    clip = create_sequence_clip(self.application(), self._track)
                    clip.set_notes((note,))

    @subject_slot('notes')
    def _on_notes_changed(self):
        self._current_lane = None
        if self._clip and self._note != -1:
            self._current_lane = self._clip.get_notes(self._start_time, self._note, self._num_steps * self._resolution, 1)
        self._update_sequence_buttons()
        return

    def _update_sequence_buttons(self):
        if self.is_enabled():
            if self._sequence_buttons:
                if self._clip and self._current_lane:
                    for index, button in enumerate(self._sequence_buttons):
                        self._update_sequence_button(index, button)

                else:
                    set_group_button_lights(self._sequence_buttons, 'Sequence.Step.%s' % ('Unusable' if self._note == -1 else 'Off'))
            if self._unused_sequence_buttons:
                set_group_button_lights(self._unused_sequence_buttons, 'Sequence.Step.Unusable')

    def _update_sequence_button(self, button_index, button):
        if self.is_enabled() and button:
            btn_pos = button_index * self._resolution + self._start_time
            current_notes = get_notes_at_position(self._current_lane, btn_pos, self._resolution)
            button.set_light(self._get_color_for_step(current_notes))

    def _get_color_for_step(self, current_notes):
        """ Returns the color to use for a step based on the muted status and velocity
        of the notes at the step. """
        if current_notes:
            high_velo = current_notes[0][NOTE_VELO]
            is_muted = False
            for note in current_notes:
                if note[NOTE_MUTED]:
                    is_muted = True
                    break
                if note[NOTE_VELO] > high_velo:
                    high_velo = note[NOTE_VELO]

            if is_muted:
                return 'Sequence.Step.Muted'
            if high_velo >= VELO_HIGH_START:
                return self._step_colors[2]
            if high_velo >= VELO_MID_START:
                return self._step_colors[1]
            return self._step_colors[0]
        return 'Sequence.Step.Off'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/NoteLaneComponent.pyc
