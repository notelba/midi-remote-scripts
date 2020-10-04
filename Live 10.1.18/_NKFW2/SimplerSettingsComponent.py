# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SimplerSettingsComponent.py
# Compiled at: 2017-03-07 13:28:53
import Live
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from _Framework.Control import ButtonControl
from _Framework.ScrollComponent import ScrollComponent, Scrollable
from SpecialControl import SpecialButtonControl
from PageSelector import PagedProperty
from ResettableScrollComponent import ScrolledProperty
from ShowMessageMixin import ShowMessageMixin
from ControlUtils import skin_scroll_component, reset_button, assign_button_to_note
from consts import SIMPLER_START_NOTE
NUM_PLAYBACK_MODES = 3
NUM_SLICING_MODES = 3
NUM_STYLES = 4
MIN_MARKER_DISTANCE = 150
SLICE_ADJUSTMENT_FACTOR = 500
START_THRESHOLD = 2
SLICE_STYLE_NAMES = ('Transients', 'Beats', 'Regions', 'Manual')
SPECIAL_SLICE_STYLES = (0, 3)
MULTI_SCROLL_FACTORS = ({'prop': 'slicing_sensitivity', 'min': 0.0, 'max': 0.998, 'def': 1.0, 'factor': 0.01}, {'prop': 'slicing_beat_division', 'min': 0, 'max': 10, 'def': 4, 'factor': 1}, {'prop': 'slicing_region_count', 'min': 2, 'max': 64, 'def': 8, 'factor': 1},
 None)

class SimplerNudgeComponent(ScrollComponent, Scrollable):
    """ ScrollComponent that handles slice nudging. """

    def __init__(self):
        self._simpler = None
        self._selected_slice = None
        super(SimplerNudgeComponent, self).__init__(scrollable=self)
        skin_scroll_component(self, color='Simpler.NudgeEnabled')
        return

    def disconnect(self):
        super(SimplerNudgeComponent, self).disconnect()
        self._simpler = None
        self._selected_slice = None
        return

    def set_object(self, obj):
        """ Sets the Simpler instance to control. """
        self._selected_slice = None
        self._simpler = obj
        return

    def set_selected_slice(self, sel_slice):
        """ Sets the slice to control. """
        self._selected_slice = sel_slice
        self.update()

    def can_scroll_up(self):
        return self._selected_slice is not None

    def can_scroll_down(self):
        return self._selected_slice is not None

    def scroll_up(self):
        self._handle_nudge(-1)

    def scroll_down(self):
        self._handle_nudge(1)

    def _handle_nudge(self, factor):
        if self._selected_slice is not None:
            current_time = self._simpler.view.selected_slice
            if current_time >= 0:
                adjust_factor = int(round(self._simpler.sample.length / SLICE_ADJUSTMENT_FACTOR))
                new_time = current_time - adjust_factor * factor
                if new_time >= 0:
                    if self._should_adjust_start_marker(current_time):
                        self._simpler.sample.start_marker = min(new_time, self._simpler.sample.length - MIN_MARKER_DISTANCE)
                    else:
                        result = self._simpler.sample.move_slice(current_time, new_time)
                        try:
                            self._simpler.view.selected_slice = result
                        except RuntimeError:
                            pass

        return

    def _should_adjust_start_marker(self, time):
        return abs(time - self._simpler.sample.start_marker) < START_THRESHOLD


class SimplerSettingsComponent(CompoundComponent, ShowMessageMixin):
    """ SimplerSettingsComponent provides controls for Simpler's
    settings. """
    warp_inc_dict = dict(color='Simpler.WarpIncrementEnabled', pressed_color='Simpler.WarpIncrementPressed')
    warp_half_button = ButtonControl(**warp_inc_dict)
    warp_double_button = ButtonControl(**warp_inc_dict)
    warp_as_button = ButtonControl(color='Simpler.WarpAsEnabled', pressed_color='Simpler.WarpAsPressed')
    reverse_button = ButtonControl(color='Simpler.ReverseEnabled', pressed_color='Simpler.ReversePressed')
    convert_button = ButtonControl(color='Simpler.ConvertEnabled')
    trigger_mode_button = SpecialButtonControl(color='Simpler.TriggerModeOff', on_color='Simpler.TriggerModeOn')
    pad_slicing_button = SpecialButtonControl(color='Simpler.PadSlicingOff', on_color='Simpler.PadSlicingOn')
    remove_slice_button = ButtonControl(color='Simpler.RemoveSliceEnabled', pressed_color='Simpler.RemoveSlicePressed')
    reset_slices_button = ButtonControl(color='Simpler.ResetSlicesEnabled', pressed_color='Simpler.ResetSlicesPressed')
    clear_slices_button = ButtonControl(color='Simpler.ClearSlicesEnabled', pressed_color='Simpler.ClearSlicesPressed')

    def __init__(self, channel, name='Simpler_Settings_Control', targets_comp=None, *a, **k):
        super(SimplerSettingsComponent, self).__init__(name=name, *a, **k)
        self._channel = channel
        self._simpler = None
        self._clip = None
        self._trigger_mode_parameter = None
        self._on_target_simpler_changed.subject = targets_comp
        self._on_target_clip_changed.subject = targets_comp
        self._selected_slice_button = None
        self._playback_modes = self.register_component(PagedProperty('playback_mode', NUM_PLAYBACK_MODES, page_button_led_values=('DefaultButton.Off',
                                                                                                                                  'Simpler.PlaybackMode.NotSelected',
                                                                                                                                  'Simpler.PlaybackMode.Selected'), page_nav_led_values=('DefaultButton.Off',
                                                                                                                                                                                         'Simpler.PlaybackMode.ToggleEnabled')))
        self._slicing_modes = self.register_component(PagedProperty('slicing_playback_mode', NUM_SLICING_MODES, page_button_led_values=('DefaultButton.Off',
                                                                                                                                        'Simpler.SlicingMode.NotSelected',
                                                                                                                                        'Simpler.SlicingMode.Selected'), page_nav_led_values=('DefaultButton.Off',
                                                                                                                                                                                              'Simpler.SlicingMode.ToggleEnabled')))
        self._slicing_styles = self.register_component(PagedProperty('slicing_style', NUM_STYLES, page_button_led_values=('DefaultButton.Off',
                                                                                                                          'Simpler.SlicingStyle.NotSelected',
                                                                                                                          'Simpler.SlicingStyle.Selected'), page_nav_led_values=('DefaultButton.Off',
                                                                                                                                                                                 'Simpler.SlicingStyle.ToggleEnabled')))
        self._nudge_component = self.register_component(SimplerNudgeComponent())
        msf = MULTI_SCROLL_FACTORS[0]
        self._multi_scroll = self.register_component(ScrolledProperty('Simpler.MultiEnabled', msf['prop'], msf['min'], msf['max'], msf['def']))
        self._start_scroll = self.register_component(ScrolledProperty('Simpler.StartEnabled', 'start_marker', 0, MIN_MARKER_DISTANCE, 0))
        self._end_scroll = self.register_component(ScrolledProperty('Simpler.EndEnabled', 'end_marker', 0, MIN_MARKER_DISTANCE, MIN_MARKER_DISTANCE))
        return

    def disconnect(self):
        super(SimplerSettingsComponent, self).disconnect()
        self._simpler = None
        self._clip = None
        self._playback_modes = None
        self._slicing_modes = None
        self._slicing_styles = None
        self._multi_scroll = None
        self._start_scroll = None
        self._end_scroll = None
        self._nudge_component = None
        self._trigger_mode_parameter = None
        self._selected_slice_button = None
        return

    def set_simpler(self, simpler):
        """ Sets the Simpler instance to control. """
        self._simpler = simpler
        self._on_sample_changed.subject = simpler or None
        self._on_playback_mode_changed.subject = simpler or None
        self._on_slicing_playback_mode_changed.subject = simpler or None
        self._on_can_warp_half_changed.subject = simpler or None
        self._on_can_warp_double_changed.subject = simpler or None
        self._on_can_warp_as_changed.subject = simpler or None
        self._on_pad_slicing_changed.subject = simpler or None
        self._on_selected_slice_changed.subject = simpler.view if simpler else None
        self._playback_modes.set_object(simpler or None)
        self._slicing_modes.set_object(simpler or None)
        self._nudge_component.set_object(simpler or None)
        self._trigger_mode_parameter = self._get_trigger_mode_parameter()
        self._on_trigger_mode_changed.subject = self._trigger_mode_parameter
        self._on_sample_changed()
        return

    def set_clip(self, clip):
        """ Sets the clip to use. """
        self._clip = clip if clip and clip.is_audio_clip else None
        self._update_convert_button()
        return

    def set_playback_mode_buttons(self, buttons):
        """ Sets the group of 3 buttons to use for playback mode selection. """
        self._playback_modes.set_page_buttons(buttons)

    def set_playback_mode_toggle_button(self, button):
        """ Sets the button to use for toggling through playback modes. """
        self._playback_modes.set_next_page_button(button)

    def set_slicing_mode_buttons(self, buttons):
        """ Sets the group of 3 buttons to use for slicing playback mode selection. """
        self._slicing_modes.set_page_buttons(buttons)

    def set_slicing_mode_toggle_button(self, button):
        """ Sets the button to use for toggling through slicing playback modes. """
        self._slicing_modes.set_next_page_button(button)

    def set_slicing_style_buttons(self, buttons):
        """ Sets the group of 4 buttons to use for slicing style selection. """
        self._slicing_styles.set_page_buttons(buttons)

    def set_slicing_style_toggle_button(self, button):
        """ Sets the button to use for toggling through slicing styles. """
        self._slicing_styles.set_next_page_button(button)

    def set_multi_decrease_button(self, button):
        """ Sets the button to use for decreasing style-based attributes. """
        self._multi_scroll.set_scroll_down_button(button)

    def set_multi_increase_button(self, button):
        """ Sets the button to use for inccreasing sstyle-based attributes. """
        self._multi_scroll.set_scroll_up_button(button)

    def set_start_decrease_button(self, button):
        """ Sets the button to use for decreasing the start marker. """
        self._start_scroll.set_scroll_down_button(button)

    def set_start_increase_button(self, button):
        """ Sets the button to use for increasing the start marker. """
        self._start_scroll.set_scroll_up_button(button)

    def set_end_decrease_button(self, button):
        """ Sets the button to use for decreasing the end marker. """
        self._end_scroll.set_scroll_down_button(button)

    def set_end_increase_button(self, button):
        """ Sets the button to use for increasing the start marker. """
        self._end_scroll.set_scroll_up_button(button)

    def set_nudge_decrease_button(self, button):
        """ Sets the button to use for nudging backwards. """
        self._nudge_component.set_scroll_down_button(button)

    def set_nudge_increase_button(self, button):
        """ Sets the button to use for nudging forwards. """
        self._nudge_component.set_scroll_up_button(button)

    def set_selected_slice_button(self, button):
        """ Sets the button to use for playing the selected slice. """
        button_to_reset = button if button else self._selected_slice_button
        reset_button(button_to_reset)
        self._selected_slice_button = button
        self._update_selected_slice_button()

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, clip):
        self.set_clip(clip)

    @subject_slot('target_simpler')
    def _on_target_simpler_changed(self, simpler):
        self.set_simpler(simpler)

    @subject_slot('sample')
    def _on_sample_changed(self):
        sample = None
        if self._simpler and self._simpler.sample:
            sample = self._simpler.sample
        self._on_slicing_style_changed.subject = sample
        self._on_start_changed.subject = sample
        self._on_end_changed.subject = sample
        self._slicing_styles.set_object(sample)
        self._multi_scroll.set_object(sample)
        self._start_scroll.set_object(sample)
        self._end_scroll.set_object(sample)
        self._update_marker_control_factors()
        self.update()
        return

    @warp_half_button.pressed
    def warp_half_button(self, _):
        if self._has_sample():
            self._simpler.warp_half()

    @warp_double_button.pressed
    def warp_double_button(self, _):
        if self._has_sample():
            self._simpler.warp_double()

    @warp_as_button.pressed
    def warp_as_button(self, _):
        if self._has_sample():
            if not self._simpler.sample.warping:
                self._simpler.sample.warping = True
            self._simpler.warp_as(self._simpler.guess_playback_length())

    @reverse_button.pressed
    def reverse_button(self, _):
        if self._has_sample():
            self._simpler.reverse()

    @convert_button.pressed
    def convert_button(self, _):
        if self._clip:
            Live.Conversions.create_midi_track_with_simpler(self.song(), self._clip)

    @trigger_mode_button.pressed
    def trigger_mode_button(self, _):
        if self._simpler and self._trigger_mode_parameter:
            self._trigger_mode_parameter.value = not self._trigger_mode_parameter.value

    @pad_slicing_button.pressed
    def pad_slicing_button(self, _):
        if self._simpler:
            self._simpler.pad_slicing = not self._simpler.pad_slicing

    @remove_slice_button.pressed
    def remove_slice_button(self, _):
        if self._is_special_slice_style():
            s_slice = self._simpler.view.selected_slice
            if s_slice is not None:
                self._simpler.sample.remove_slice(s_slice)
        return

    @reset_slices_button.pressed
    def reset_slices_button(self, _):
        if self._is_special_slice_style():
            self._simpler.sample.reset_slices()

    @clear_slices_button.pressed
    def clear_slices_button(self, _):
        if self._is_special_slice_style():
            self._simpler.sample.clear_slices()

    @subject_slot('playback_mode')
    def _on_playback_mode_changed(self):
        self._playback_modes.update()

    @subject_slot('slicing_playback_mode')
    def _on_slicing_playback_mode_changed(self):
        self._slicing_modes.update()

    @subject_slot('slicing_style')
    def _on_slicing_style_changed(self):
        self._slicing_styles.update()
        self._update_special_slicing_controls()
        self._update_multi_scroll_factors()
        if self._has_sample():
            style = self._simpler.sample.slicing_style
            self.component_message('Slicing Style', SLICE_STYLE_NAMES[style])

    @subject_slot('can_warp_half')
    def _on_can_warp_half_changed(self):
        self._update_warp_half_button()

    @subject_slot('can_warp_double')
    def _on_can_warp_double_changed(self):
        self._update_warp_double_button()

    @subject_slot('can_warp_as')
    def _on_can_warp_as_changed(self):
        self._update_warp_as_button()

    @subject_slot('value')
    def _on_trigger_mode_changed(self):
        self._update_trigger_mode_button()

    @subject_slot('pad_slicing')
    def _on_pad_slicing_changed(self):
        self._update_pad_slicing_button()
        if self._simpler:
            self.component_message('Pad Slicing', 'On' if self._simpler.pad_slicing else 'Off')

    @subject_slot('start_marker')
    def _on_start_changed(self):
        self._update_marker_control_factors()

    @subject_slot('end_marker')
    def _on_end_changed(self):
        self._update_marker_control_factors()

    @subject_slot('selected_slice')
    def _on_selected_slice_changed(self):
        sel_slice = None
        if self._has_sample():
            sel_slice = self._simpler.view.selected_slice
        self._nudge_component.set_selected_slice(sel_slice)
        self._update_selected_slice_button()
        return

    def _has_sample(self):
        return self._simpler is not None and self._simpler.sample is not None

    def _is_special_slice_style(self):
        return self._has_sample() and self._simpler.sample.slicing_style in SPECIAL_SLICE_STYLES

    def _get_trigger_mode_parameter(self):
        if self._simpler:
            for p in self._simpler.parameters:
                if p.name == 'Trigger Mode':
                    return p

        return

    def _update_marker_control_factors(self):
        start = 0
        end = MIN_MARKER_DISTANCE
        length = MIN_MARKER_DISTANCE
        adjust_factor = MIN_MARKER_DISTANCE
        if self._has_sample():
            sample = self._simpler.sample
            start = sample.start_marker
            end = sample.end_marker
            length = sample.length
            adjust_factor = int(round(length / MIN_MARKER_DISTANCE))
        self._start_scroll.set_min_and_max_values(0, end - MIN_MARKER_DISTANCE)
        self._start_scroll.set_adjustment_factor(adjust_factor)
        self._end_scroll.set_min_and_max_values(start + MIN_MARKER_DISTANCE, length - 1)
        self._end_scroll.set_default_value(length - 1)
        self._end_scroll.set_adjustment_factor(adjust_factor)
        self._start_scroll.update()
        self._end_scroll.update()

    def _update_multi_scroll_factors(self):
        if self._has_sample():
            msf = MULTI_SCROLL_FACTORS[self._simpler.sample.slicing_style]
            if msf:
                self._multi_scroll.set_property_name(msf['prop'])
                self._multi_scroll.set_min_and_max_values(msf['min'], msf['max'])
                self._multi_scroll.set_default_value(msf['def'])
                self._multi_scroll.set_adjustment_factor(msf['factor'])
                self._multi_scroll.set_object(self._simpler.sample)
            else:
                self._multi_scroll.set_object(None)
            self._multi_scroll.update()
        return

    def _update_selected_slice_button(self):
        if self._selected_slice_button:
            if self._has_sample() and self._simpler.view.selected_slice in self._simpler.sample.slices:
                idx = self._simpler.sample.slices.index(self._simpler.view.selected_slice)
                assign_button_to_note(self._selected_slice_button, idx + SIMPLER_START_NOTE, channel=self._channel, color='Simpler.SlicePad')
            else:
                reset_button(self._selected_slice_button)

    def update(self):
        super(SimplerSettingsComponent, self).update()
        for component in self._sub_components:
            component.update()

        self._update_warp_half_button()
        self._update_warp_double_button()
        self._update_warp_as_button()
        self._update_reverse_button()
        self._update_convert_button()
        self._update_trigger_mode_button()
        self._update_special_slicing_controls()
        self._update_multi_scroll_factors()
        self._on_selected_slice_changed()

    def _update_special_slicing_controls(self):
        self._update_pad_slicing_button()
        if self.is_enabled():
            enable = self._is_special_slice_style()
            self.remove_slice_button.enabled = enable
            self.reset_slices_button.enabled = enable
            self.clear_slices_button.enabled = enable
            if enable:
                self._on_selected_slice_changed()
            else:
                self._nudge_component.set_selected_slice(None)
        return

    def _update_warp_half_button(self):
        if self.is_enabled():
            self.warp_half_button.enabled = self._simpler and self._simpler.can_warp_half

    def _update_warp_double_button(self):
        if self.is_enabled():
            self.warp_double_button.enabled = self._simpler and self._simpler.can_warp_double

    def _update_warp_as_button(self):
        if self.is_enabled():
            self.warp_as_button.enabled = self._simpler and self._simpler.can_warp_as

    def _update_reverse_button(self):
        if self.is_enabled():
            self.reverse_button.enabled = self._has_sample()

    def _update_convert_button(self):
        if self.is_enabled():
            self.convert_button.enabled = self._clip is not None
        return

    def _update_trigger_mode_button(self):
        if self.is_enabled():
            self.trigger_mode_button.enabled = self._simpler is not None
            if self._simpler and self._trigger_mode_parameter:
                self.trigger_mode_button.is_on = self._trigger_mode_parameter.value > 0
        return

    def _update_pad_slicing_button(self):
        if self.is_enabled():
            is_special = self._is_special_slice_style()
            self.pad_slicing_button.enabled = is_special
            if is_special:
                self.pad_slicing_button.is_on = self._simpler.pad_slicing
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SimplerSettingsComponent.pyc
