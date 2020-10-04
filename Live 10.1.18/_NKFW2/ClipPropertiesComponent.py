# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipPropertiesComponent.py
# Compiled at: 2017-04-24 12:52:35
from functools import partial
from _Framework.SubjectSlot import subject_slot
from ClipComponent import ClipComponent
from PropertyControl import PropertyControl, ResettablePropertyControl
from Utils import live_object_is_valid, calculate_bar_length, calculate_beat_length, format_absolute_time
from consts import PARAM_REL_STEP, WARP_MODE_NAMES
MAX_END = 999999999

class MarkerProperty(ResettablePropertyControl):
    """ MarkerProperty specializes ResettablePropertyControl to control a clip's start,
    end and loop markers with different levels of quantization. """
    marker_factor = 1

    def __init__(self, *a, **k):
        super(MarkerProperty, self).__init__(*a, **k)
        self._enabled = True
        self._should_zoom = False
        self._time_base_is_one = True
        self._display_value_transform = self._standard_value_transform
        if self._property_name == 'loop_end':
            self._display_value_transform = self._length_value_transform

    def set_zoom_on_edit(self, should_zoom):
        """ Sets whether to zoom in the clip when a marker is edited. """
        self._should_zoom = should_zoom

    def set_range(self, full_range, abs_range=None, suppress_feedback=False):
        """ Extends standard to set alternate range when a marker can't be controlled.
        This makes it so encoder LEDs aren't turned off when a marker can't be controlled.
        This also can override feedback suppression for proper LED feedback on marker
        positions. """
        self._enabled = full_range[0] != full_range[1]
        if not self._enabled:
            full_range = (
             full_range[0] - 1, full_range[0])
        self._suppress_feedback = suppress_feedback
        super(MarkerProperty, self).set_range(full_range, abs_range=abs_range)

    def set_property_value(self, current_value, new_value):
        """ Overrides standard to utilize different levels of quantization for controlling
        markers. """
        if self._enabled:
            current_value *= self.marker_factor
            new_value *= self.marker_factor
            if live_object_is_valid(self._parent) and current_value != new_value:
                new_param_value = max(self._absolute_range[0] * self.marker_factor, min(self._absolute_range[1] * self.marker_factor, new_value))
                setattr(self._parent, self._property_name, new_param_value)
                if self._should_zoom:
                    self._parent.view.show_loop()
                    self._parent.view.show_loop()

    def get_property_value(self):
        """ Overrides standard to return properly quantized value. """
        if live_object_is_valid(self._parent):
            return int(getattr(self._parent, self._property_name) / self.marker_factor)
        else:
            return

    @property
    def is_quantized(self):
        """ Overrides standard as end property is not resettable like other marker
        properties. """
        return self._display_name == 'End'

    def _standard_value_transform(self, _):
        return format_absolute_time(self._parent, getattr(self._parent, self._property_name))

    def _length_value_transform(self, _):
        return format_absolute_time(self._parent, self._parent.loop_end - self._parent.loop_start, base_is_one=False)


class AudioClipProperty(ResettablePropertyControl):
    """ AudioClipProperty specializes ResettablePropertyControl for use with properties
    of an audio clip. """

    def set_parent(self, parent):
        """ Extends standard to only set the parent if it's an audio clip. """
        super(AudioClipProperty, self).set_parent(parent if parent and parent.is_audio_clip else None)
        return


class WarpProperty(PropertyControl):
    """ WarpProperty specializes PropertyControl to control a clip's warp mode. """

    def set_parent(self, parent):
        """ Extends standard to only set parent if it's an audio clip and to set the
        property's range based on the available warp modes. """
        if parent and parent.is_audio_clip and parent.warping:
            self.set_range((0, len(parent.available_warp_modes) - 1))
            super(WarpProperty, self).set_parent(parent)
        else:
            super(WarpProperty, self).set_parent(None)
        return

    def set_property_value(self, current_value, new_value):
        """ Overrides standard to set the warp mode based on the available warp modes. """
        if self._parent.warping and current_value != new_value:
            modes = list(self._parent.available_warp_modes)
            self._parent.warp_mode = modes[new_value]

    def get_property_value(self):
        """ Overrides standard to return the index of the current warp mode. """
        if self._parent:
            modes = list(self._parent.available_warp_modes)
            return modes.index(self._parent.warp_mode)
        return 0

    @property
    def value_items(self):
        """ Overrides standard as not all WARP_MODE_NAMES will be available, so need
        to build a list of what's available for the clip. """
        if self._parent:
            return [ WARP_MODE_NAMES[x] for x in self._parent.available_warp_modes ]
        return ()


class ClipPropertiesComponent(ClipComponent):
    """ ClipPropertiesControl specializes ClipComponent to allow encoders to control the
    properties of clips. """

    def __init__(self, name='Clip_Property_Control', *a, **k):
        super(ClipPropertiesComponent, self).__init__(name=name, *a, **k)
        self._wrapper_dict = {'start': MarkerProperty('start_marker', None, (0, 127), display_name='Start'), 
           'end': MarkerProperty('end_marker', None, (1, MAX_END), display_name='End'), 
           'position': MarkerProperty('position', None, (0, 127), display_name='Position', can_enforce_takeover=False), 
           'length': MarkerProperty('loop_end', None, (0, 127), display_name='Length', display_value_transform=self._display_length, can_enforce_takeover=False), 
           'transpose': AudioClipProperty('pitch_coarse', None, (-48, 48), rel_thresh=1, default_value=0, display_name='Transpose', display_value_transform=lambda x: '%i st' % x), 
           'detune': AudioClipProperty('pitch_fine', None, (-49, 49), rel_thresh=1, display_name='Detune', display_value_transform=lambda x: '%i ct' % x), 
           'gain': AudioClipProperty('gain', None, (0, 1.0), default_value=0.40000000596, rel_thresh=0, rel_step=PARAM_REL_STEP, quantized=False, display_name='Gain', display_value_transform=self._display_gain), 
           'warp_mode': WarpProperty('warp_mode', None, (0, 1), display_name='Warp Mode', display_value_transform=self._display_warp_mode)}
        self._wrapper_dict['position'].set_zoom_on_edit(self._zoom_loop_on_edit)
        self._wrapper_dict['length'].set_zoom_on_edit(self._zoom_loop_on_edit)
        return

    def disconnect(self):
        for w in self._wrapper_dict.values():
            w.disconnect()

        super(ClipPropertiesComponent, self).disconnect()

    def __getattr__(self, name):
        """ Overrides standard to handle setters for PropertyControls. """
        if len(name) > 4 and name[:4] == 'set_':
            return partial(self._set_control, name[4:].replace('_control', ''))

    def _set_control(self, name, control):
        self._wrapper_dict[name].set_control(control)

    def set_shift_button(self, button):
        """ Extends standard to set up listener for use with setting the quantization to
        use for adjusting markers. """
        super(ClipPropertiesComponent, self).set_shift_button(button)
        self._on_shift_button_value.subject = button

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        self._update_marker_factor(by_bar=value == 0)

    def on_clip_changed(self):
        """ Sets property parents and adds listeners. """
        for w in self._wrapper_dict.values():
            w.set_parent(self._clip)

        self._on_end_marker_changed.subject = None
        self._on_position_changed.subject = None
        self._on_start_marker_changed.subject = self._clip
        self._on_loop_end_changed.subject = self._clip
        self._on_time_signature_denominator_changed.subject = self._clip
        self._on_time_signature_numerator_changed.subject = self._clip
        self._on_warping_changed.subject = self._clip if self._clip and self._clip.is_audio_clip else None
        self._update_marker_factor()
        return

    @subject_slot('looping')
    def _on_looping_status_changed(self):
        if self.is_enabled() and self._clip:
            self._update_start_property(update_prop_name=True)
            self._update_end_property(update_prop_name=True)
            self._update_position_property(update_parent=True)
            self._update_length_property(update_parent=True)
            loop_clip = self._clip if self._clip and self._clip.looping else None
            self._on_end_marker_changed.subject = loop_clip
            self._on_position_changed.subject = loop_clip
        super(ClipPropertiesComponent, self)._on_looping_status_changed()
        return

    @subject_slot('loop_end')
    def _on_loop_end_changed(self):
        if self.is_enabled() and self._clip:
            self._update_start_property()
            if self._clip.looping:
                suppress = not self._wrapper_dict['length']._suppress_feedback
                self._update_position_property(suppress_feedback=suppress)

    @subject_slot('position')
    def _on_position_changed(self):
        if self.is_enabled() and self._clip:
            self._update_length_property()

    @subject_slot('start_marker')
    def _on_start_marker_changed(self):
        if self.is_enabled() and self._clip:
            self._update_end_property()

    @subject_slot('end_marker')
    def _on_end_marker_changed(self):
        if self.is_enabled() and self._clip:
            self._update_start_property()
            self._update_position_property()
            self._update_length_property()

    @subject_slot('signature_numerator')
    def _on_time_signature_numerator_changed(self):
        self._update_marker_factor()

    @subject_slot('signature_denominator')
    def _on_time_signature_denominator_changed(self):
        self._update_marker_factor()

    @subject_slot('warping')
    def _on_warping_changed(self):
        self._wrapper_dict['warp_mode'].set_parent(self._clip)

    def _update_marker_factor(self, by_bar=True):
        if self._clip:
            MarkerProperty.marker_factor = calculate_bar_length(self._clip) if by_bar else calculate_beat_length(self._clip)
            self._update_start_property()
            self._update_end_property()
            if self._clip.looping:
                self._update_position_property()
                self._update_length_property()

    def _update_start_property(self, update_prop_name=False):
        clip_end = self._clip.loop_end
        if self._clip.looping:
            clip_end = min(self._clip.loop_end, self._clip.end_marker)
        end = clip_end / MarkerProperty.marker_factor - 1
        self._wrapper_dict['start'].set_range((0, end))
        if update_prop_name:
            self._wrapper_dict['start'].set_property_name('start_marker' if self._clip.looping else 'loop_start')

    def _update_end_property(self, update_prop_name=False):
        start = self._wrapper_dict['start'].get_property_value() + 1
        self._wrapper_dict['end'].set_range((start, MAX_END))
        if update_prop_name:
            self._wrapper_dict['end'].set_property_name('end_marker' if self._clip.looping else 'loop_end')

    def _update_position_property(self, update_parent=False, suppress_feedback=False):
        loop_len = self._clip.loop_end - self._clip.loop_start
        factor = MarkerProperty.marker_factor
        end = self._clip.end_marker / factor - loop_len / factor
        self._wrapper_dict['position'].set_range((0, end), suppress_feedback=suppress_feedback)
        if update_parent:
            self._wrapper_dict['position'].set_parent(self._clip if self._clip.looping else None)
        return

    def _update_length_property(self, update_parent=False):
        if self._clip.looping:
            start = self._wrapper_dict['position'].get_property_value() + 1
            end = self._clip.end_marker / MarkerProperty.marker_factor
            self._wrapper_dict['length'].set_range((start, end))
            self._wrapper_dict['length'].set_default_value(self._clip.end_marker)
        if update_parent:
            self._wrapper_dict['length'].set_parent(self._clip if self._clip.looping else None)
        return

    def update(self):
        super(ClipPropertiesComponent, self).update()
        if self.is_enabled():
            for w in self._wrapper_dict.values():
                w.update()

    def _display_gain(self, _):
        if self._clip and self._clip.is_audio_clip:
            return self._clip.gain_display_string
        return ''

    def _display_warp_mode(self, _):
        if self._clip and self._clip.is_audio_clip:
            return WARP_MODE_NAMES[self._clip.warp_mode]
        return ''
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipPropertiesComponent.pyc
