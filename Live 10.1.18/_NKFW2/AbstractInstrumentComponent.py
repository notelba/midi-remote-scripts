# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\AbstractInstrumentComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group, CallableSubjectSlotGroup
from _Framework.Util import nop
from ModifierMixin import ModifierMixin
from ShowMessageMixin import ShowMessageMixin
from ResettableScrollComponent import ResettableScrollComponent, ResettableScrollable
from ControlUtils import skin_scroll_component, is_button_pressed, get_group_buttons_pressed
from ClipUtils import delete_note_lane, delete_all_notes, mute_note_lane, convert_to_note_name

class AbstractInstrumentComponent(CompoundComponent, ModifierMixin, ShowMessageMixin, ResettableScrollable):
    """ AbstractInstrumentComponent provides the basic plumbing needed for components
    that can play instruments.

    This utilizes several modifiers as well as modifier combinations.
    Delete + pad =     Delete notes associated with pad or range of pads
    Quantize + pad =   Quantize notes associated with pad or range of pads

    Shift is used here if Select is not present
    Select + Delete =  Delete all notes
    Select + Quantize = Quantize all notes """

    def __init__(self, scroll_button_color='DefaultButton.On', handle_modifier_leds=True, target_clip_comp=None, quantize_comp=None, octave_size=12, *a, **k):
        super(AbstractInstrumentComponent, self).__init__(handle_modifier_leds=handle_modifier_leds, press_callback=self._set_enabled_state_of_used_pads, *a, **k)
        self._on_target_clip_changed.subject = target_clip_comp
        self._quantize_component = quantize_comp
        self._octave_size = octave_size
        self._octave_offset = 0
        self._clip = None
        self._erase_start_time = None
        self._used_pads = []
        self._unused_pads = []
        self._unused_pad_listener = self.register_slot_manager(CallableSubjectSlotGroup(event='value', listener=nop, function=nop))
        self._scroller = self.register_component(ResettableScrollComponent(self))
        skin_scroll_component(self._scroller, color=scroll_button_color)
        return

    def disconnect(self):
        super(AbstractInstrumentComponent, self).disconnect()
        self._quantize_component = None
        self._clip = None
        self._erase_start_time = None
        self._used_pads = None
        self._unused_pads = None
        self._unused_pad_listener = None
        return

    def set_clip(self, clip):
        """ Sets the clip to use. """
        self._clip = clip if clip and clip.is_midi_clip else None
        return

    def can_scroll_up(self):
        """ Whether or not scrolling up is possible. """
        raise NotImplementedError

    def can_scroll_down(self):
        """ Whether or not scrolling down is possible. """
        raise NotImplementedError

    def _can_scroll_octave(self, _):
        """ Whether or not scrolling is possible. To be overridden. """
        return True

    def reset(self):
        """ Resets the scroll position. """
        raise NotImplementedError

    def should_enable_scroller(self):
        """ Whether or not the scroller should be enabled. """
        return True

    def increment_scroll_position(self, factor):
        """ Handles actually performing the scroll by the given factor.
        This is a standard implementation that can be overridden. """
        is_decrease = factor < 0
        if self._can_scroll_octave(is_decrease):
            if is_decrease:
                self._octave_offset -= self._octave_size
            else:
                self._octave_offset += self._octave_size
            self.update()

    @subject_slot_group('value')
    def on_used_pad_value(self, value, button):
        """ Handles deleting or quantizing note lanes if certain modifiers are pressed.
        This is a standard implementation that can be overridden. """
        if is_button_pressed(self._delete_button):
            self.handle_note_delete(value != 0, button.message_identifier())
        elif is_button_pressed(self._quantize_button) and value:
            self.handle_note_quantize()

    def handle_note_delete(self, is_pressed, btn_id):
        """ Handles deleting a single note or range of notes or erasing a portion of the
        note lane. """
        if self._clip:
            n_range = self._get_note_range()
            if len(n_range) < 2:
                if self._clip.is_playing and self.song().is_playing:
                    self._handle_note_erase(is_pressed, btn_id)
                elif is_pressed:
                    delete_note_lane(self._clip, n_range[0])
                    self.component_message('Note Deleted', convert_to_note_name(n_range[0]))
            elif is_pressed:
                self._clip.remove_notes(-100000000.0, n_range[0], 999999999.0, n_range[1])
                self.component_message('Notes Deleted', '%s - %s' % (
                 convert_to_note_name(n_range[0]),
                 convert_to_note_name(n_range[2] - 1)))

    def _handle_note_erase(self, is_pressed, btn_id):
        """ Handles erasing a portion of a note lane. """
        if is_pressed:
            self._erase_start_time = self._clip.playing_position
            mute_note_lane(self._clip, btn_id, True)
            self.component_message('Erasing Note', convert_to_note_name(btn_id))
        else:
            if self._clip.playing_position < self._erase_start_time:
                end_range = self._clip.loop_end - self._erase_start_time
                self._clip.remove_notes(self._erase_start_time, btn_id, end_range, 1)
                self._clip.remove_notes(0.0, btn_id, self._clip.playing_position, 1)
            else:
                t_range = self._clip.playing_position - self._erase_start_time
                self._clip.remove_notes(self._erase_start_time, btn_id, t_range, 1)
            mute_note_lane(self._clip, btn_id, False)

    def handle_note_quantize(self):
        """ Handles quantizing a single note or range of notes. """
        if self._clip and self._quantize_component:
            n_range = self._get_note_range()
            if len(n_range) == 1:
                self._quantize_component.quantize_pitch(self._clip, n_range[0])
            else:
                for i in xrange(n_range[0], n_range[2]):
                    self._quantize_component.quantize_pitch(self._clip, i)

    def _get_note_range(self):
        """ Returns the range of used pads that are currently pressed. """
        pressed = get_group_buttons_pressed(self._used_pads)
        if pressed:
            start_note = self._used_pads[pressed[0]].message_identifier()
            if len(pressed) == 1:
                return (start_note,)
            end_note = self._used_pads[pressed[1]].message_identifier()
            if end_note == start_note:
                return (start_note,)
            if end_note < start_note:
                old_end = end_note
                end_note = start_note
                start_note = old_end
        else:
            return ()
        return (
         start_note, end_note - start_note + 1, end_note + 1)

    def select_pressed(self):
        """ Returns whether the select button (if present) is pressed. If it's not
        present, returns the pressed state of the shift button. """
        if self._select_button:
            return is_button_pressed(self._select_button)
        return is_button_pressed(self._shift_button)

    def handle_unall_functions(self):
        """ Handles deleting/quantizing all notes if certain modifiers are pressed.  This
        is a standard implementation that can be overridden. """
        if self._clip and self.select_pressed():
            if is_button_pressed(self._delete_button):
                delete_all_notes(self._clip)
                return True
            if is_button_pressed(self._quantize_button) and self._quantize_component:
                self._quantize_component.quantize_clip(self._clip)
                return True
        return False

    def handle_unused_pads(self):
        """ Handles setting up/removing listener for unused pads. """
        self._unused_pad_listener.replace_subjects(self._unused_pads or [])

    def set_scroll_down_button(self, button):
        """ Sets the button to use for scrolling down (octaves, etc). """
        self._scroller.set_scroll_down_button(button)

    def set_scroll_up_button(self, button):
        """ Sets the button to use for scrolling up (octaves, etc). """
        self._scroller.set_scroll_up_button(button)

    def scroll_up(self):
        self.increment_scroll_position(1)

    def scroll_down(self):
        self.increment_scroll_position(-1)

    def update(self):
        super(AbstractInstrumentComponent, self).update()
        self.update_modifier_leds()
        self._scroller.set_enabled(self.should_enable_scroller())
        self._scroller.update()

    def _set_enabled_state_of_used_pads(self, state, _):
        if state and self.handle_unall_functions():
            return
        if self._used_pads:
            for pad in self._used_pads:
                pad.set_enabled(state, True)

        self.on_used_pad_value.replace_subjects(self._used_pads if state else [])

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, clip):
        self.set_clip(clip)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/AbstractInstrumentComponent.pyc
