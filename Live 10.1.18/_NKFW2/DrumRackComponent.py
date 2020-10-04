# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\DrumRackComponent.py
# Compiled at: 2017-09-30 15:26:22
from AbstractInstrumentComponent import AbstractInstrumentComponent, subject_slot, subject_slot_group
from ControlUtils import is_button_pressed, reset_button, reset_group_buttons, assign_button_to_note
from ClipUtils import delete_all_notes
from consts import MIDI_RANGE, MAX_DR_SCROLL_POS
WIDTH = 4
MAX_WIDTH = WIDTH * 2
PAGE_SIZE = 4
FULL_PAGE_OFFSET = 1
DEFAULT_SCROLL_POS = 9

class DrumRackComponent(AbstractInstrumentComponent):
    """ DrumRackComponent allows a matrix to be used to play and control a drum rack.
    This supports anywhere between a 4x4 and 8x8 matrix.

    This utilizes several modifiers as well as modifier combinations.
    Select + pad =     Select pad (Shift + Pad if Select is not present)
    Mute + pad =       Mute pad
    Solo + pad =       Solo pad
    Delete + pad =     Delete notes associated with pad or range of pads
    Quantize + pad =   Quantize notes associated with pad or range of pads
    Duplicate+ pad =   Commence pad copy.

    Shift is used here if Select is not present
    Select + Mute =    Unmute all pads
    Select + Solo =    Unsolo all pads
    Select + Delete =  Delete all notes
    Select + Quantize =Quantize all notes

    Shift + scroll =   Scroll by 1 (or 4) depending on default

    An optional implementation (ColoredDrumRackComponent) that allows the user to specify
    the colors to use is provided in this module. """
    __subject_events__ = ('selected_note', )

    def __init__(self, translation_ch=0, invert_rows=True, scroll_button_color='Navigation.DrumRackEnabled', handle_modifier_leds=True, scroll_by_4_by_default=True, targets_comp=None, quantize_comp=None, name='Drum_Rack_Control', *a, **k):
        super(DrumRackComponent, self).__init__(name=name, scroll_button_color=scroll_button_color, handle_modifier_leds=handle_modifier_leds, target_clip_comp=targets_comp, quantize_comp=quantize_comp, *a, **k)
        self._on_target_drum_rack_changed.subject = targets_comp
        self._translation_channel = translation_ch
        self._scroll_by_4_by_default = scroll_by_4_by_default
        self._invert_rows = bool(invert_rows)
        self._row_xrange = None
        self._selected_drum_pad = None
        self._drum_rack = None
        self._drum_matrix = None
        self._filled_value = 'DrumRack.PadFilled'
        self._empty_value = 'DrumRack.PadEmpty'
        self._selected_value = 'DrumRack.PadSelected'
        self._soloed_value = 'DrumRack.PadSoloed'
        self._muted_value = 'DrumRack.PadMuted'
        self._copy_pad_source_index = None
        return

    def disconnect(self):
        super(DrumRackComponent, self).disconnect()
        self._row_xrange = None
        self._selected_drum_pad = None
        self._drum_rack = None
        self._drum_matrix = None
        return

    @property
    def selected_note(self):
        """ Returns the note associated with the selected drum pad or 0. """
        if self._selected_drum_pad:
            return self._selected_drum_pad.note
        return 0

    def get_pad_filled_color(self, _):
        """ This will be called for all pads that are filled, but not muted, soloed or
        selected. The unused param here is the name of the pad so that this can be used
        to handle custom pad name-based coloring. """
        return self._filled_value

    def set_drum_matrix(self, matrix):
        """ Sets the matrix to use for playing/controlling the drum rack. """
        assert matrix is None or matrix.height() % 2 == 0
        self._unused_pads = []
        self._used_pads = []
        matrix_to_reset = matrix if matrix else self._drum_matrix
        reset_group_buttons(matrix_to_reset)
        self._drum_matrix = matrix
        if matrix:
            if self._invert_rows:
                self._row_xrange = xrange(matrix.height() - 1, -1, -1)
            else:
                self._row_xrange = xrange(matrix.height())
            self._update_all_pad_settings()
            self._update_all_pad_leds()
        return

    @subject_slot('target_drum_rack')
    def _on_target_drum_rack_changed(self, drum_rack):
        self.set_drum_rack(drum_rack)

    def set_drum_rack(self, drum_rack, force=False):
        """ Sets the drum rack to play/control and sets up all listeners. """
        if force or type(drum_rack) != type(self._drum_rack) or drum_rack != self._drum_rack:
            self._drum_rack = drum_rack
            drum_rack_view = drum_rack.view if drum_rack else None
            pads = drum_rack.drum_pads if drum_rack else []
            self._on_chains_changed.subject = drum_rack
            self._on_selected_drum_pad_changed.subject = drum_rack_view
            self._on_drum_pads_scroll_position_changed.subject = drum_rack_view
            self._on_solo_changed.replace_subjects(pads)
            self._on_mute_changed.replace_subjects(pads)
            self._update_all_pad_settings()
            self._scroller.set_enabled(self._drum_rack is not None)
            self._scroller.update()
            self._on_selected_drum_pad_changed(True)
        return

    def can_scroll_up(self):
        return self._drum_rack is not None and self._drum_rack.view.drum_pads_scroll_position < MAX_DR_SCROLL_POS

    def can_scroll_down(self):
        return self._drum_rack is not None and self._drum_rack.view.drum_pads_scroll_position > 0

    def reset(self):
        if self._drum_rack:
            self._drum_rack.view.drum_pads_scroll_position = DEFAULT_SCROLL_POS

    def increment_scroll_position(self, factor):
        """ This needs the quantized handling because full drum rack pages don't
        actually start until the 1st (instead of 0th) row. """
        current_pos = self._drum_rack.view.drum_pads_scroll_position
        should_quantize = self._scroll_by_4_by_default != is_button_pressed(self._shift_button)
        quantized_factor = PAGE_SIZE
        if should_quantize:
            distance = (current_pos - FULL_PAGE_OFFSET) % PAGE_SIZE
            if distance:
                if factor > 0:
                    quantized_factor = PAGE_SIZE - distance
                else:
                    quantized_factor = distance
        actual_factor = (quantized_factor if should_quantize else 1) * factor
        self._drum_rack.view.drum_pads_scroll_position = max(0, min(MAX_DR_SCROLL_POS, current_pos + actual_factor))

    def update(self):
        self.set_drum_rack(self._drum_rack, True)
        super(DrumRackComponent, self).update()

    def should_enable_scroller(self):
        return self._drum_rack is not None

    @subject_slot_group('value')
    def on_used_pad_value(self, value, button):
        if self._drum_rack:
            if is_button_pressed(self._delete_button):
                self.handle_note_delete(value != 0, button.message_identifier())
            elif value:
                pad_id = button.message_identifier()
                dr_pad = self._drum_rack.drum_pads[pad_id]
                if self.select_pressed():
                    self._drum_rack.view.selected_drum_pad = dr_pad
                    self.component_message('Pad Selection', dr_pad.name)
                elif is_button_pressed(self._mute_button):
                    dr_pad.mute = not dr_pad.mute
                elif is_button_pressed(self._solo_button):
                    dr_pad.solo = not dr_pad.solo
                elif is_button_pressed(self._quantize_button):
                    self.handle_note_quantize()
                elif is_button_pressed(self._duplicate_button):
                    self._handle_pad_copy(button, pad_id, dr_pad)

    def _handle_pad_copy(self, button, pad_id, dr_pad):
        if self._copy_pad_source_index is not None:
            if self._copy_pad_source_index != pad_id:
                src_name = self._drum_rack.drum_pads[self._copy_pad_source_index].name
                dst_name = dr_pad.name
                if dr_pad.chains:
                    dr_pad.delete_all_chains()
                self._drum_rack.copy_pad(self._copy_pad_source_index, pad_id)
                self._update_all_pad_leds()
                self.component_message('%s copied to %s' % (src_name, dst_name))
                self._copy_pad_source_index = None
        else:
            self._copy_pad_source_index = None
            if dr_pad.chains:
                self._copy_pad_source_index = pad_id
                button.set_light('DrumRack.PadCopySource')
                self.component_message('%s copied' % dr_pad.name, 'Press destination pad to paste')
        return

    @subject_slot('drum_pads_scroll_position')
    def _on_drum_pads_scroll_position_changed(self):
        self._scroller.update()
        self._update_all_pad_settings()
        self._update_all_pad_leds()

    @subject_slot('chains')
    def _on_chains_changed(self):
        if not is_button_pressed(self._duplicate_button):
            self._update_all_pad_settings()
            self._update_all_pad_leds()

    @subject_slot('selected_drum_pad')
    def _on_selected_drum_pad_changed(self, force=False):
        new_selection = self._drum_rack.view.selected_drum_pad if self._drum_rack else None
        if force or new_selection and new_selection != self._selected_drum_pad:
            self._selected_drum_pad = new_selection
            self.notify_selected_note(new_selection.note if new_selection else 0)
            self._update_all_pad_leds(True)
        return

    @subject_slot_group('solo')
    def _on_solo_changed(self, _):
        self._update_all_pad_leds(True)

    @subject_slot_group('mute')
    def _on_mute_changed(self, _):
        self._update_all_pad_leds(True)

    def handle_unall_functions(self):
        if self._drum_rack:
            if self.select_pressed():
                if is_button_pressed(self._mute_button):
                    for pad in self._drum_rack.drum_pads:
                        pad.mute = False

                    return True
                if is_button_pressed(self._solo_button):
                    for pad in self._drum_rack.drum_pads:
                        pad.solo = False

                    return True
                if is_button_pressed(self._delete_button) and self._clip:
                    delete_all_notes(self._clip)
                    return True
                if is_button_pressed(self._quantize_button) and self._clip and self._quantize_component:
                    self._quantize_component.quantize_clip(self._clip)
                    return True
        return False

    def _set_enabled_state_of_used_pads(self, state, _):
        if self._copy_pad_source_index is not None:
            self._update_all_pad_leds()
        self._copy_pad_source_index = None
        super(DrumRackComponent, self)._set_enabled_state_of_used_pads(state, _)
        return

    def _update_all_pad_settings(self):
        if self.is_enabled():
            self._unused_pads = []
            self._used_pads = []
            if self._drum_matrix:
                if self._drum_rack:
                    last_id = self._drum_rack.visible_drum_pads[0].note
                    has_side_by_side = self._drum_matrix.width() == MAX_WIDTH
                    for row in self._row_xrange:
                        for col in xrange(WIDTH):
                            self._update_pad_settings(row, col, last_id)
                            last_id += 1

                    if has_side_by_side:
                        for row in self._row_xrange:
                            for col in xrange(WIDTH, MAX_WIDTH):
                                self._update_pad_settings(row, col, last_id)
                                last_id += 1

                else:
                    reset_group_buttons(self._drum_matrix)
                    self._unused_pads = self._drum_matrix
        self.handle_unused_pads()

    def _update_pad_settings(self, row, column, identifier_to_set):
        pad = self._drum_matrix.get_button(column, row)
        if pad:
            if identifier_to_set in MIDI_RANGE:
                assign_button_to_note(pad, identifier_to_set, channel=self._translation_channel, force_next=False)
                self._used_pads.append(pad)
            else:
                reset_button(pad)
                self._unused_pads.append(pad)
            pad.force_next_send()

    def _update_all_pad_leds(self, force=False):
        if self.is_enabled() and self._drum_matrix:
            for pad in self._drum_matrix:
                self._update_pad_led(pad, force)

    def _update_pad_led(self, pad, force=False):
        color = 'DefaultButton.Off'
        if self._drum_rack and pad and pad in self._used_pads:
            color = self._empty_value
            dr_pad = self._drum_rack.drum_pads[pad.message_identifier()]
            if dr_pad == self._selected_drum_pad:
                color = self._selected_value
            elif dr_pad.chains:
                if dr_pad.solo:
                    color = self._soloed_value
                elif dr_pad.mute:
                    color = self._muted_value
                else:
                    color = self.get_pad_filled_color(dr_pad.name.upper())
            if force:
                pad.force_next_send()
            pad.set_light(color)


class ColoredDrumRackComponent(DrumRackComponent):
    """ Specialized DrumRackComponent that can read color settings from file
    and use the settings in place of the defaults. The settings in the file
    can be: PAD_EMPTY, PAD_NOT_EMPTY, PAD_SELECTED, PAD_SOLOED, PAD_MUTED.
    Also, pad names (or portions thereof) can be specified so that colors
    can be associated with pad names.
    """

    def __init__(self, color_class, *a, **k):
        self._color_names = color_class.__dict__.keys()
        self._color_class_name = str(color_class).split('.')[(-1)] if color_class else ''
        self._pad_to_color_names = {}
        super(ColoredDrumRackComponent, self).__init__(*a, **k)

    def disconnect(self):
        super(ColoredDrumRackComponent, self).disconnect()
        self._color_names = None
        self._color_class_name = None
        self._pad_to_color_names = None
        return

    def get_pad_filled_color(self, pad_name):
        for k, v in self._pad_to_color_names.iteritems():
            if k in pad_name:
                return v

        return self._filled_value

    def parse_settings(self, settings):
        """ Parses the given dict of settings of color settings. """
        if settings:
            for k, v in settings.iteritems():
                if k == 'PAD_EMPTY':
                    self._empty_value = self._parse_color_value(v, self._empty_value)
                elif k == 'PAD_NOT_EMPTY':
                    self._filled_value = self._parse_color_value(v, self._filled_value)
                elif k == 'PAD_SELECTED':
                    self._selected_value = self._parse_color_value(v, self._selected_value)
                elif k == 'PAD_SOLOED':
                    self._soloed_value = self._parse_color_value(v, self._soloed_value)
                elif k == 'PAD_MUTED':
                    self._muted_value = self._parse_color_value(v, self._muted_value)
                else:
                    self._pad_to_color_names[k.upper()] = self._parse_color_value(v, self._filled_value)

    def _parse_color_value(self, color, default=None):
        if color in self._color_names:
            return '%s.%s' % (self._color_class_name, color)
        return default
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/DrumRackComponent.pyc
