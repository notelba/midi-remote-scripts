# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\VelocityLevelsComponent.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from _NKFW2.ControlUtils import reset_group_buttons

class VelocityLevelsComponent(ControlSurfaceComponent):
    """ VelocityLevelsComponent allows a matrix to be used for playing a single note with
    differing levels of velocity. """

    def __init__(self, original_ch=0, translation_ch=9, translation_ids=None, invert_rows=True, *a, **k):
        super(VelocityLevelsComponent, self).__init__(*a, **k)
        self.is_private = True
        self._original_channel = original_ch
        self._translation_channel = translation_ch
        self._translation_ids = translation_ids
        self._invert_rows = bool(invert_rows)
        self._velocity_notes = []
        self._note = 36
        self._velocity_matrix = None
        self._velocity_levels = None
        return

    def disconnect(self):
        super(VelocityLevelsComponent, self).disconnect()
        self._translation_ids = None
        self._velocity_notes = None
        self._velocity_matrix = None
        self._velocity_levels = None
        return

    def set_velocity_levels(self, levels):
        """ Sets the velocity levels object. """
        self._velocity_levels = levels
        self._on_last_played_level.subject = levels
        self.update()

    def set_note_component(self, component):
        """ Sets the component to use for determining the note to control. The component
        must have an observable selected_note property. """
        self.set_note.subject = component
        if component:
            self.set_note(component.selected_note)

    def set_velocity_matrix(self, matrix):
        """ Sets the matrix to use for playing notes. """
        self._velocity_notes = []
        matrix_to_reset = matrix if matrix else self._velocity_matrix
        reset_group_buttons(matrix_to_reset)
        matrix_as_list = []
        if matrix:
            if self._invert_rows:
                x_range = xrange(matrix.height() - 1, -1, -1)
            else:
                x_range = xrange(matrix.height())
            width = matrix.width()
            count = 0
            for row in x_range:
                for col in xrange(width):
                    button = matrix.get_button(col, row)
                    if button:
                        matrix_as_list.append(button)
                        button_id = button.message_identifier()
                        if self._translation_ids:
                            button_id = self._translation_ids[count]
                            button.set_identifier(button_id)
                        self._velocity_notes.append(button_id)
                        button.set_channel(self._original_channel)
                        button.set_enabled(False)
                    count += 1

        self._velocity_matrix = matrix_as_list
        self.update()

    @subject_slot('selected_note')
    def set_note(self, note, _=False):
        """ Sets the notes to control. """
        self._note = note
        self.update()

    @subject_slot('last_played_level')
    def _on_last_played_level(self):
        self._update_all_pad_leds()

    def update(self):
        super(VelocityLevelsComponent, self).update()
        if self._velocity_levels:
            self._velocity_levels.enabled = self.is_enabled()
            self._velocity_levels.source_channel = self._original_channel
            self._velocity_levels.notes = self._velocity_notes
            self._velocity_levels.target_note = self._note
            self._velocity_levels.target_channel = self._translation_channel
        self._update_all_pad_leds()

    def _get_last_played_velocity_index(self):
        played_index = -1
        if self._velocity_levels:
            last_played = self._velocity_levels.last_played_level
            levels = list(self._velocity_levels.levels)
            if last_played in levels:
                played_index = levels.index(last_played)
                if played_index > len(self._velocity_matrix):
                    played_index = -1
        return played_index

    def _update_all_pad_leds(self):
        if self.is_enabled() and self._velocity_matrix:
            played_index = self._get_last_played_velocity_index()
            for i, button in enumerate(self._velocity_matrix):
                if button:
                    button.force_next_send()
                    if i == played_index:
                        button.set_light('VelocityLevels.Selected')
                    else:
                        button.set_light('VelocityLevels.NotSelected')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/VelocityLevelsComponent.pyc
