# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SeqPageComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from ClipUtils import apply_loop_settings, create_sequence_clip
from ControlUtils import set_group_button_lights, get_group_buttons_pressed, is_button_pressed
from ModifierMixin import ModifierMixin
from ShowMessageMixin import ShowMessageMixin
from Utils import format_absolute_time
from consts import DEF_SEQ_CLIP_LENGTH, RESOLUTIONS as RES
PAGE_LENGTHS = {32: {k:4.0 for k in RES}, 16: {k:4.0 if k > 0.25 else 2.0 for k in RES}, 8: {RES[0]: 1.0, RES[1]: 1.0, RES[2]: 1.0, RES[3]: 2.0, RES[4]: 2.0, 
       RES[5]: 4.0, RES[6]: 4.0, RES[7]: 4.0}}

class SeqPageComponent(ControlSurfaceComponent, ModifierMixin, ShowMessageMixin):
    """ SeqPageComponent handles selecting the page(s) to step-sequence into as well as
    controlling the clip's loop. """
    __subject_events__ = ('start_time', )

    def __init__(self, num_steps, resolution_comp, handle_modifier_leds=True, targets_comp=None, *a, **k):
        super(SeqPageComponent, self).__init__(handle_modifier_leds=handle_modifier_leds, *a, **k)
        self.is_private = True
        self._num_steps = num_steps
        self._clip = None
        self._track = None
        self._page_length = 0.0
        self._step_input_length = 0.0
        self._num_viewable_pages = 1
        self._full_edit_range = 0.0
        self._current_edit_range = 0.0
        self._editing_single_page = False
        self._last_playing_page = -1
        self._is_following = False
        self._page_buttons = None
        self._num_page_buttons = 0
        self._last_page_button_index = -1
        self.set_clip.subject = targets_comp
        self.set_track.subject = targets_comp
        self._resolution = resolution_comp.resolution
        self._on_resolution_changed.subject = resolution_comp
        self._on_resolution_changed(resolution_comp.resolution)
        return

    def disconnect(self):
        super(SeqPageComponent, self).disconnect()
        self._clip = None
        self._track = None
        self._page_buttons = None
        return

    @property
    def start_time(self):
        """ The time to start sequencing from. """
        return self._current_edit_range[0]

    @subject_slot('target_clip')
    def set_clip(self, clip):
        """ Sets the clip to sequence into. """
        self._editing_single_page = False
        self._is_following = False
        self._last_page_button_index = -1
        self._clip = clip if clip and clip.is_midi_clip else None
        self._on_playing_position_changed.subject = self._clip
        self._on_playing_status_changed.subject = self._clip
        self._on_looping_changed.subject = self._clip
        self._on_loop_start_changed.subject = self._clip
        self._on_loop_end_changed.subject = self._clip
        self.update()
        return

    @subject_slot('target_track')
    def set_track(self, track):
        """ Sets the track associated with the clip. This is needed for creating new
        clips. """
        self._track = track if track and track.has_midi_input else None
        return

    def set_page_buttons(self, buttons):
        """ Sets the buttons to use for selecting pages/adjusting the clip's loop. """
        self._last_page_button_index = -1
        self._page_buttons = list(buttons) if buttons else None
        self._num_page_buttons = len(self._page_buttons) if buttons else 0
        self._on_page_button_value.replace_subjects(buttons or [])
        self._update_page_buttons()
        return

    @subject_slot_group('value')
    def _on_page_button_value(self, value, _):
        if self.is_enabled():
            if not self._clip:
                if value and self._track:
                    create_sequence_clip(self.application(), self._track)
                return
            if value:
                pressed = get_group_buttons_pressed(self._page_buttons)
                start = pressed[0] * self._page_length
                if is_button_pressed(self._delete_button):
                    self._clip.remove_notes(start, 0, self._page_length, 128)
                    self._show_info('Deleted', start, start + self._page_length)
                elif is_button_pressed(self._duplicate_button):
                    if pressed[0] < self._num_page_buttons - 1:
                        self._clip.remove_notes(start + self._page_length, 0, self._page_length, 128)
                        n_to_dupe = self._clip.get_notes(start, 0, self._page_length, 128)
                        target_notes = []
                        for n in n_to_dupe:
                            target_notes.append((n[0], n[1] + self._page_length, n[2],
                             n[3], n[4]))

                        self._clip.set_notes(tuple(target_notes))
                        self._show_info('Duplicated', start, start + self._page_length)
                elif len(pressed) == 2:
                    self._set_page_range(pressed[0], pressed[1])
                    self._last_page_button_index = -1
                else:
                    should_adjust = self._last_page_button_index == pressed[0]
                    self._set_page_range(pressed[0], pressed[0], adjust_clip=should_adjust)
                    self._last_page_button_index = pressed[0]

    def _set_page_range(self, index, end, adjust_clip=True):
        """ Sets the page(s) to sequence into and (optionally) adjusts the clip's
        loop. """
        if self.is_enabled() and self._clip:
            self._editing_single_page = index == end
            start = index * self._page_length
            if adjust_clip:
                c_end = end * self._page_length + self._page_length
                apply_loop_settings(self._clip, (start, c_end), True, True, True)
                self._full_edit_range = (start, c_end)
                self._current_edit_range = (start,
                 min(c_end, self._step_input_length + start))
            else:
                self._current_edit_range = self._get_quantized_range(index)
                if self._current_edit_range[1] > self._clip.loop_end:
                    self._clip.loop_end = self._current_edit_range[1]
            self._notify_start_time_change()
            self._last_playing_page = -1
            self._enable_following()
            self._update_page_buttons()

    def _handle_page_follow(self, start_page):
        """ Handles moving between pages when is_following. """
        q_range = self._get_quantized_range(start_page)
        if q_range[0] != self._current_edit_range[0]:
            self._current_edit_range = q_range
            self._notify_start_time_change()
            self._update_page_buttons()

    def _get_quantized_range(self, start_page):
        """ Quantizes the page range for cases where a resolution allows for viewing
        multiple pages. """
        qntzd_start_pos = start_page / self._num_viewable_pages * self._num_viewable_pages * self._page_length
        return (qntzd_start_pos, qntzd_start_pos + self._step_input_length)

    def _notify_start_time_change(self, show_info=True):
        """ Notifies listeners of start time changes and displays time range in
        status bar. """
        self.notify_start_time(self._current_edit_range[0])
        if self._clip and show_info:
            self._show_info('Page', self._current_edit_range[0], self._current_edit_range[1])

    def _show_info(self, header, start, end):
        self.component_message('%s Range' % header, '%s - %s' % (
         format_absolute_time(self._clip, start),
         format_absolute_time(self._clip, end)))

    def _calculate_ranges_and_lengths(self):
        """ Calculates the length of a page at the current resolution as well as the
        number of viewable pages and edit ranges. """
        if self._num_steps:
            self._page_length = PAGE_LENGTHS[self._num_steps][self._resolution]
            raw_length = self._num_steps * self._resolution
            self._num_viewable_pages = int(raw_length / self._page_length)
            if self._num_viewable_pages < 1:
                self._num_viewable_pages = 1
            if self._num_viewable_pages >= 2 and self._num_viewable_pages % 2 != 0:
                self._num_viewable_pages -= 1
            self._step_input_length = self._num_viewable_pages * self._page_length
            self._full_edit_range = (0.0, DEF_SEQ_CLIP_LENGTH)
            self._current_edit_range = (0.0, self._step_input_length)

    def _enable_following(self):
        """ Enables following if the current range can't be viewed on a single page.
        Disables it otherwise. """
        if self._editing_single_page:
            self._is_following = False
        else:
            seq_range = self._full_edit_range[1] - self._full_edit_range[0]
            self._is_following = seq_range > self._step_input_length

    @subject_slot('resolution')
    def _on_resolution_changed(self, res):
        self._resolution = res
        self._calculate_ranges_and_lengths()
        self._enable_following()
        self._last_playing_page = -1
        self._update_page_buttons()
        self._on_playing_position_changed()
        self._notify_start_time_change(show_info=False)

    @subject_slot('playing_position')
    def _on_playing_position_changed(self):
        if self.is_enabled() and self._page_buttons:
            if self._clip:
                position = int(self._clip.playing_position / self._page_length)
                if position in xrange(self._num_page_buttons) and position != self._last_playing_page:
                    self._clear_last_playing_page_button()
                    if self._is_following:
                        self._handle_page_follow(position)
                    self._page_buttons[position].set_light('Sequence.Page.Playing')
                    self._last_playing_page = position
            else:
                set_group_button_lights(self._page_buttons, 'Sequence.Page.OutOfRange')

    @subject_slot('playing_status')
    def _on_playing_status_changed(self):
        if self._clip and not self._clip.is_playing:
            self._clear_last_playing_page_button()

    @subject_slot('looping')
    def _on_looping_changed(self):
        self._update_page_buttons()

    @subject_slot('loop_start')
    def _on_loop_start_changed(self):
        self._update_page_buttons()

    @subject_slot('loop_end')
    def _on_loop_end_changed(self):
        self._update_page_buttons()

    def update(self):
        super(SeqPageComponent, self).update()
        self._last_playing_page = -1
        self._calculate_ranges_and_lengths()
        self._enable_following()
        self._update_page_buttons()

    def _update_page_buttons(self):
        if self.is_enabled() and self._page_buttons:
            if self._clip:
                for i in xrange(self._num_page_buttons):
                    self._update_page_button(i)

            else:
                set_group_button_lights(self._page_buttons, 'Sequence.Page.OutOfRange')

    def _update_page_button(self, index):
        if self.is_enabled() and self._clip:
            button = self._page_buttons[index]
            if button:
                value = 'Sequence.Page.OutOfRange'
                page = index * self._page_length
                if self._editing_single_page and page >= self._current_edit_range[0] and page < self._current_edit_range[1]:
                    value = 'Sequence.Page.Selected'
                elif page >= self._clip.loop_start and page < self._clip.loop_end:
                    value = 'Sequence.Page.InRange'
                button.set_light(value)

    def _clear_last_playing_page_button(self):
        if self._page_buttons and self._last_playing_page != -1:
            self._update_page_button(self._last_playing_page)
        self._last_playing_page = -1
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SeqPageComponent.pyc
