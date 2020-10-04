# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ScaleSettingsComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from PageSelector import PageSelector, Pageable
from ShowMessageMixin import ShowMessageMixin
from Scales import Scales, SCALE_TYPES, CHROMATIC_SCALE
from SpecialControl import SpecialButtonControl, RadioButtonGroup
from consts import NUM_TONICS, COMPOUND_NOTE_NAMES
TONIC_MATRIX_IDS = (-1, 1, 3, -1, 6, 8, 10, -1, 0, 2, 4, 5, 7, 9, 11, -1)
NUM_TONIC_BUTTONS = 16
SEQ_OFFSET = 0
FOURTHS_OFFSET = 3
CHROMATIC_OFFSET = 2
OFFSET_NAMES = ('Sequent', '2nds', '3rds', '4ths', '5ths', '6ths')

class ScaleDisplayingRadioButtonGroup(RadioButtonGroup):
    """ Specialized RadioButtonGroup that will display the selected tonic as well as
    which notes are within the selected scale. """

    def __init__(self, *a, **k):
        super(ScaleDisplayingRadioButtonGroup, self).__init__(*a, **k)
        self._scale_intervals = SCALE_TYPES[0].intervals
        self._is_in_key = True

    def set_scale_settings(self, intervals, in_key):
        """ Sets the scale intervals and in key status to display. """
        self._scale_intervals = intervals if in_key else CHROMATIC_SCALE.intervals
        self._is_in_key = in_key
        self.update()

    def update(self):
        if self._buttons:
            if self._is_enabled:
                for index, button in enumerate(self._buttons):
                    if button:
                        if index == self._current_index:
                            button.set_light('Instrument.Tonics.Selected')
                        elif (index - self._current_index) % NUM_TONICS in self._scale_intervals:
                            button.set_light('Instrument.Tonics.InKey')
                        else:
                            button.set_light('Instrument.Tonics.NotSelected')

            else:
                for button in self._buttons:
                    if button:
                        button.set_light('DefaultButton.Off')


class TonicSelector(PageSelector):
    """ Specialized PageSelector that uses the ScaleDisplayingRadioButtonGroup. """
    button_group_type = ScaleDisplayingRadioButtonGroup

    def set_scale_settings(self, scale, in_key):
        """ Delegates to ScaleDisplayingRadioButtonGroup to scale intervals and
        in key status. """
        self._page_buttons.set_scale_settings(scale, in_key)


class ScaleSettingsComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ ScaleSettingsComponent provides controls and methods for adjusting
    scale settings and also provides notifications upon changes. """
    __subject_events__ = ('scale_settings', )
    in_key_button = SpecialButtonControl(color='Instrument.Scales.InKeyOff', on_color='Instrument.Scales.InKeyOn')
    offset_toggle_button = SpecialButtonControl(color='Instrument.Scales.SequentOff', on_color='Instrument.Scales.SequentOn', disabled_color='DefaultButton.Off')
    orientation_button = SpecialButtonControl(color='Instrument.Scales.HorizontalOff', on_color='Instrument.Scales.HorizontalOn', disabled_color='DefaultButton.Off')

    def __init__(self, name='Scale_Settings_Control', num_scale_select_buttons=None, in_key_by_default=True, *a, **k):
        super(ScaleSettingsComponent, self).__init__(name=name, *a, **k)
        self._scales = Scales(num_scale_select_buttons)
        self._scale_selector = PageSelector(self._scales, page_button_led_values=('DefaultButton.Off',
                                                                                  'Instrument.Scales.NotSelected',
                                                                                  'Instrument.Scales.Selected'), page_nav_led_values=('Navigation.Disabled',
                                                                                                                                      'Navigation.ScalesEnabled'))
        self._on_scale_changed.subject = self._scales
        self._tonics = Pageable(len(COMPOUND_NOTE_NAMES))
        self._tonic_selector = TonicSelector(self._tonics, page_nav_led_values=('Navigation.Disabled',
                                                                                'Navigation.TonicsEnabled'))
        self._on_tonic_changed.subject = self._tonics
        self._offsets = Pageable(len(OFFSET_NAMES))
        self._offset_selector = PageSelector(self._offsets, page_button_led_values=('DefaultButton.Off',
                                                                                    'Instrument.Offsets.NotSelected',
                                                                                    'Instrument.Offsets.Selected'), page_nav_led_values=('Navigation.Disabled',
                                                                                                                                         'Navigation.OffsetsEnabled'))
        self._offsets.set_page_index(FOURTHS_OFFSET)
        self._offsets.can_select_pages = lambda : False
        self._offset_selector.set_enabled(False)
        self._on_offset_changed.subject = self._offsets
        self._in_key = bool(in_key_by_default)
        self._orientation_is_horizontal = False
        self._can_change_layout = False
        self._can_change_orientation = False
        song_scale_name = self.song().scale_name
        if song_scale_name:
            for index, scale in enumerate(SCALE_TYPES):
                if scale.name == song_scale_name:
                    self._scales.set_page_index(index)
                    break

        else:
            self.song().scale_name = self._scales.scale.name
        self._tonics.set_page_index(self.song().root_note)
        self._tonic_selector.set_scale_settings(self._scales.scale.intervals, self._in_key)

    def disconnect(self):
        self._scale_selector.disconnect()
        self._tonic_selector.disconnect()
        self._offset_selector.disconnect()
        super(ScaleSettingsComponent, self).disconnect()
        self._scales = None
        self._tonics = None
        self._offsets = None
        return

    @property
    def scale(self):
        """ Returns the currently selected scale object. """
        return self._scales.scale

    @property
    def tonic(self):
        """ Returns the currently selected tonic (as an int). """
        return self._tonics.page_index

    @property
    def in_key(self):
        """ Returns whether in key is active. """
        return self._in_key

    @property
    def sequent_layout(self):
        """ Returns whether the current layout is sequent. """
        return self._offsets.page_index == SEQ_OFFSET

    @property
    def row_offset(self):
        """ Returns the current row offset. """
        if self.in_key:
            return self._offsets.page_index
        return self._offsets.page_index + CHROMATIC_OFFSET

    @property
    def orientation_is_horizontal(self):
        """ Returns whether the current orientation is horizontal. """
        return self._orientation_is_horizontal

    def _get_can_change_layout(self):
        return self._can_change_layout

    def _set_can_change_layout(self, can_change):
        self._can_change_layout = bool(can_change)
        self._offsets.can_select_pages = lambda : self._can_change_layout
        self._offset_selector.set_enabled(self._can_change_layout)
        if not self._can_change_layout:
            self._can_change_orientation = False
        self._notify_scale_settings()

    can_change_layout = property(_get_can_change_layout, _set_can_change_layout)

    def _get_can_change_orientation(self):
        return self._can_change_orientation

    def _set_can_change_orientation(self, can_change):
        self._can_change_orientation = bool(can_change)
        self._notify_scale_settings()

    can_change_orientation = property(_get_can_change_orientation, _set_can_change_orientation)

    def set_scale_buttons(self, buttons):
        """ Sets the group of buttons to use for direct scale selection. """
        self._scale_selector.set_page_buttons(buttons)

    def set_prev_scale_button(self, button):
        """ Sets the button to use for moving to the previous scale. """
        self._scale_selector.set_prev_page_button(button)

    def set_next_scale_button(self, button):
        """ Sets the button to use for moving to the next scale. """
        self._scale_selector.set_next_page_button(button)

    def set_tonic_buttons(self, buttons):
        """ Sets the group of 16 buttons to use for direct tonic selection.
        Dummy listeners will be added for the 4 buttons that are unused. """
        assert buttons is None or len(list(buttons)) == NUM_TONIC_BUTTONS
        unused_buttons = []
        tonic_buttons = None
        if buttons:
            buttons = list(buttons)
            tonic_buttons = [ None for index in xrange(NUM_TONICS) ]
            for index, tonic in enumerate(TONIC_MATRIX_IDS):
                if tonic == -1:
                    unused_buttons.append(buttons[index])
                    if self.is_enabled() and buttons[index]:
                        buttons[index].set_light('DefaultButton.Off')
                else:
                    tonic_buttons[tonic] = buttons[index]

        self._tonic_selector.set_page_buttons(tonic_buttons)
        self._on_unused_tonic_button_value.replace_subjects(unused_buttons)
        return

    def set_prev_tonic_button(self, button):
        """ Sets the button to use for moving to the previous tonic. """
        self._tonic_selector.set_prev_page_button(button)

    def set_next_tonic_button(self, button):
        """ Sets the button to use for moving to the next tonic. """
        self._tonic_selector.set_next_page_button(button)

    def set_offset_buttons(self, buttons):
        """ Sets the group of buttons to use for direct offset selection. """
        self._offset_selector.set_page_buttons(buttons)

    def set_prev_offset_button(self, button):
        """ Sets the button to use for moving to the previous offset. """
        self._offset_selector.set_prev_page_button(button)

    def set_next_offset_button(self, button):
        """ Sets the button to use for moving to the next offset. """
        self._offset_selector.set_next_page_button(button)

    @in_key_button.pressed
    def in_key_button(self, _):
        self._in_key = not self._in_key
        self._notify_scale_settings()
        self.component_message('In Key', 'Yes' if self._in_key else 'No')

    @offset_toggle_button.pressed
    def offset_toggle_button(self, _):
        if self._can_change_layout:
            self._offsets.set_page_index(SEQ_OFFSET if self._offsets.page_index else FOURTHS_OFFSET)

    @orientation_button.pressed
    def orientation_button(self, _):
        if self._can_change_orientation:
            self._orientation_is_horizontal = not self._orientation_is_horizontal
            self._notify_scale_settings()
            self.component_message('Orientation', 'Horizontal' if self._orientation_is_horizontal else 'Vertical')

    @subject_slot_group('value')
    def _on_unused_tonic_button_value(self, value, button):
        pass

    @subject_slot('page_index')
    def _on_scale_changed(self):
        self._scale_selector.update()
        self._notify_scale_settings()
        self.song().scale_name = self._scales.scale.name
        self.component_message('Scale Type', self._scales.scale.name)

    @subject_slot('page_index')
    def _on_tonic_changed(self):
        self._tonic_selector.update()
        self._notify_scale_settings()
        self.song().root_note = self._tonics.page_index
        self.component_message('Root Note', COMPOUND_NOTE_NAMES[self._tonics.page_index])

    @subject_slot('page_index')
    def _on_offset_changed(self):
        self._offset_selector.update()
        self._notify_scale_settings()
        self.component_message('Offset', OFFSET_NAMES[self._offsets.page_index])

    def _notify_scale_settings(self):
        self.notify_scale_settings()
        self._tonic_selector.set_scale_settings(self._scales.scale.intervals, self._in_key)
        self._update_optional_controls()

    def update(self):
        super(ScaleSettingsComponent, self).update()
        self._scale_selector.update()
        self._tonic_selector.update()
        self._offset_selector.update()
        self._update_optional_controls()

    def _update_optional_controls(self):
        if self.is_enabled():
            self.in_key_button.is_on = self._in_key
            self.offset_toggle_button.enabled = self._can_change_layout
            if self._can_change_layout:
                self.offset_toggle_button.is_on = self.sequent_layout
            self.orientation_button.enabled = self._can_change_orientation
            if self._can_change_orientation:
                self.orientation_button.is_on = self._orientation_is_horizontal
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ScaleSettingsComponent.pyc
