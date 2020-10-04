# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\clip_control_component.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import EventObject, clamp, forward_property, listenable_property, listens, liveobj_valid, nop
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, control_list, EncoderControl, StepEncoderControl
from ableton.v2.control_surface.mode import ModesComponent
from ableton.v2.control_surface.elements import DisplayDataSource
ONE_THIRTYSECOND_IN_BEATS = 0.125
ONE_SIXTEENTH_IN_BEATS = 0.25
ONE_YEAR_AT_120BPM_IN_BEATS = 63072000.0
GRID_QUANTIZATION_LIST = [
 Live.Clip.GridQuantization.no_grid,
 Live.Clip.GridQuantization.g_thirtysecond,
 Live.Clip.GridQuantization.g_sixteenth,
 Live.Clip.GridQuantization.g_eighth,
 Live.Clip.GridQuantization.g_quarter,
 Live.Clip.GridQuantization.g_half,
 Live.Clip.GridQuantization.g_bar,
 Live.Clip.GridQuantization.g_2_bars,
 Live.Clip.GridQuantization.g_4_bars,
 Live.Clip.GridQuantization.g_8_bars]
WARP_MODE_NAMES = {Live.Clip.WarpMode.beats: b'Beats', 
   Live.Clip.WarpMode.tones: b'Tones', 
   Live.Clip.WarpMode.texture: b'Texture', 
   Live.Clip.WarpMode.repitch: b'Repitch', 
   Live.Clip.WarpMode.complex: b'Complex', 
   Live.Clip.WarpMode.complex_pro: b'Pro', 
   Live.Clip.WarpMode.rex: b'Rex'}

def convert_beat_time_to_bars_beats_sixteenths((numerator, denominator), beat_time):
    if beat_time is None:
        return b'-'
    else:
        beats_per_bar = one_bar_in_note_values((numerator, denominator), 4.0)
        musical_beats_per_beat = denominator / 4.0
        if beat_time >= 0:
            bars = 1 + int(beat_time / beats_per_bar)
        else:
            bars = int(beat_time / beats_per_bar) if beat_time % beats_per_bar == 0 else int(beat_time / beats_per_bar) - 1
        beats = 1 + int(beat_time % beats_per_bar * musical_beats_per_beat)
        sixteenths = 1 + int(beat_time % (1.0 / musical_beats_per_beat) * 4.0)
        return b'%i.%i.%i' % (bars, beats, sixteenths)


def convert_beat_length_to_bars_beats_sixteenths((numerator, denominator), beat_length):
    if beat_length is None:
        return b'-'
    else:
        beats_per_bar = one_bar_in_note_values((numerator, denominator), 4.0)
        musical_beats_per_beat = denominator / 4.0
        bars = int(beat_length / beats_per_bar)
        beats = int(beat_length % beats_per_bar * musical_beats_per_beat)
        sixteenths = int(beat_length % (1.0 / musical_beats_per_beat) * 4.0)
        return b'%i.%i.%i' % (bars, beats, sixteenths)


def is_new_recording(clip):
    return clip.is_recording and not clip.is_overdubbing


def one_bar_in_note_values((numerator, denominator), note_value=4.0):
    return note_value * numerator / denominator


class LoopSettingsModel(EventObject):
    __events__ = ('looping', 'loop_start', 'loop_end', 'loop_length', 'position', 'start_marker')

    def __init__(self, song, *a, **k):
        super(LoopSettingsModel, self).__init__(*a, **k)
        self.clip = None
        self._song = song
        return

    @listenable_property
    def clip(self):
        return self._clip

    @clip.setter
    def clip(self, clip):
        self._clip = clip
        self._loop_length = self._get_loop_length()
        self._on_looping_changed.subject = clip
        self._on_start_marker_changed.subject = clip
        self._on_loop_start_changed.subject = clip
        self._on_loop_end_changed.subject = clip
        self._on_position_changed.subject = clip
        self.notify_clip()

    loop_start = forward_property(b'clip')(b'loop_start')
    start_marker = forward_property(b'clip')(b'start_marker')
    loop_end = forward_property(b'clip')(b'loop_end')
    looping = forward_property(b'clip')(b'looping')
    position = forward_property(b'clip')(b'position')

    @listens(b'looping')
    def _on_looping_changed(self):
        self.notify_looping()

    @listens(b'start_marker')
    def _on_start_marker_changed(self):
        self.notify_start_marker()

    @listens(b'loop_start')
    def _on_loop_start_changed(self):
        self._update_loop_length()
        self.notify_loop_start()

    @listens(b'loop_end')
    def _on_loop_end_changed(self):
        self._update_loop_length()
        self.notify_loop_end()

    @listens(b'position')
    def _on_position_changed(self):
        self.notify_position()

    @property
    def loop_length(self):
        return self._loop_length

    def _get_loop_length(self):
        if liveobj_valid(self._clip):
            return self.loop_end - self.loop_start
        return 0

    def _update_loop_length(self):
        loop_length = self._get_loop_length()
        if self._loop_length != loop_length:
            self._loop_length = loop_length
            self.notify_loop_length()

    @property
    def can_loop(self):
        return self.clip.is_midi_clip or self.clip.is_audio_clip and self.clip.warping

    def move_start_marker(self, value, fine_grained):
        marker = self.clip.start_marker if self.looping else self.clip.loop_start
        new_value = marker + self._adjusted_offset(value, fine_grained)
        signature = (
         self.clip.signature_numerator, self.clip.signature_denominator)
        measure_in_beats = one_bar_in_note_values(signature)
        measure_in_sixteenths = one_bar_in_note_values(signature, 16.0)
        additional_offset = measure_in_beats / measure_in_sixteenths * (measure_in_sixteenths - 1) if fine_grained else 0.0
        new_value = min(new_value, self.clip.loop_end - measure_in_beats + additional_offset)
        if self.looping:
            if new_value >= self.clip.end_marker:
                self.clip.end_marker = self.clip.loop_end
            self.clip.start_marker = new_value
        else:
            self.clip.loop_start = new_value

    def move_position(self, value, fine_grained):
        if not is_new_recording(self.clip):
            new_value = self.clip.position + self._adjusted_offset(value, fine_grained)
            should_update_start_marker = self.clip.position == self.clip.start_marker
            self.clip.position = new_value
            if should_update_start_marker:
                self.clip.start_marker = new_value
            self.clip.view.show_loop()

    def move_loop_end(self, value, fine_grained):
        if not is_new_recording(self.clip):
            new_end = self.clip.loop_end + self._adjusted_offset(value, fine_grained)
            if new_end > self.loop_start:
                self.clip.loop_end = new_end

    def _adjusted_offset(self, value, fine_grained):
        return value * self._encoder_factor(fine_grained) * one_bar_in_note_values((
         self.clip.signature_numerator, self.clip.signature_denominator))

    def _encoder_factor(self, fine_grained):
        if fine_grained:
            return 1.0 / one_bar_in_note_values((self.clip.signature_numerator, self.clip.signature_denominator), 16.0)
        return 1.0


class LoopSettingsControllerComponent(Component):
    encoders = control_list(StepEncoderControl, control_count=4)
    shift_button = ButtonControl()

    def __init__(self, *a, **k):
        super(LoopSettingsControllerComponent, self).__init__(*a, **k)
        self._encoder_callbacks_looped = [
         self._on_clip_position_value,
         self._on_clip_end_value,
         self._on_clip_start_marker_value,
         self._on_clip_looping_value]
        self._encoder_callbacks_unlooped = [
         self._on_clip_start_marker_value,
         self._on_clip_end_value,
         nop,
         self._on_clip_looping_value]
        self._touched_encoder_callbacks_looped = [
         self._on_clip_position_touched,
         self._on_clip_end_touched,
         self._on_clip_start_marker_touched,
         self._on_clip_looping_touched]
        self._touched_encoder_callbacks_unlooped = [
         self._on_clip_position_touched,
         self._on_clip_end_touched,
         nop,
         self._on_clip_looping_touched]
        self._released_encoder_callbacks_looped = [
         self._on_clip_position_released,
         self._on_clip_end_released,
         self._on_clip_start_marker_released,
         self._on_clip_looping_released]
        self._released_encoder_callbacks_unlooped = [
         self._on_clip_position_released,
         self._on_clip_end_released,
         nop,
         self._on_clip_looping_released]
        self._loop_model = self.register_disconnectable(LoopSettingsModel(self.song))
        self._update_encoder_state()

    def _get_clip(self):
        return self._loop_model.clip

    def _set_clip(self, clip):
        self._loop_model.clip = clip
        self.update()
        self._update_encoder_state()
        self._on_clip_changed()

    clip = property(_get_clip, _set_clip)

    def _on_clip_changed(self):
        pass

    @encoders.value
    def encoders(self, value, encoder):
        callback_set = self._encoder_callbacks_looped if self._loop_model.looping else self._encoder_callbacks_unlooped
        callback_set[encoder.index](value)

    @encoders.touched
    def encoders(self, encoder):
        callback_set = self._touched_encoder_callbacks_looped if self._loop_model.looping else self._touched_encoder_callbacks_unlooped
        callback_set[encoder.index]()

    @encoders.released
    def encoders(self, encoder):
        callback_set = self._released_encoder_callbacks_looped if self._loop_model.looping else self._released_encoder_callbacks_unlooped
        callback_set[encoder.index]()

    def _update_encoder_state(self):
        enable_encoders = liveobj_valid(self.clip)
        for encoder in self.encoders:
            encoder.enabled = enable_encoders

    def _on_clip_position_value(self, value):
        self._loop_model.move_position(value, self.shift_button.is_pressed)

    def _on_clip_end_value(self, value):
        self._loop_model.move_loop_end(value, self.shift_button.is_pressed)

    def _on_clip_start_marker_value(self, value):
        self._loop_model.move_start_marker(value, self.shift_button.is_pressed)

    def _on_clip_looping_value(self, value):
        if self._loop_model.can_loop:
            currently_looping = self._loop_model.looping
            if value >= 0 and not currently_looping or value < 0 and currently_looping:
                self._loop_model.looping = not currently_looping

    def _on_clip_start_marker_touched(self):
        pass

    def _on_clip_end_touched(self):
        pass

    def _on_clip_position_touched(self):
        pass

    def _on_clip_looping_touched(self):
        pass

    def _on_clip_start_marker_released(self):
        pass

    def _on_clip_end_released(self):
        pass

    def _on_clip_position_released(self):
        pass

    def _on_clip_looping_released(self):
        pass


class LoopSettingsComponent(LoopSettingsControllerComponent):
    """
    Component for managing loop settings of a clip
    """

    def __init__(self, *a, **k):
        super(LoopSettingsComponent, self).__init__(*a, **k)
        self._name_sources = [ DisplayDataSource() for _ in xrange(4) ]
        self._value_sources = [ DisplayDataSource() for _ in xrange(4) ]
        self.__on_looping_changed.subject = self._loop_model
        self.__on_start_marker_changed.subject = self._loop_model
        self.__on_loop_start_changed.subject = self._loop_model
        self.__on_loop_end_changed.subject = self._loop_model

    def set_name_display(self, display):
        if display:
            display.set_data_sources(self._name_sources)

    def set_value_display(self, display):
        if display:
            display.set_data_sources(self._value_sources)

    def convert_beat_time_to_bars_beats_sixteenths(self, clip, beat_time):
        return convert_beat_time_to_bars_beats_sixteenths((
         clip.signature_numerator, clip.signature_denominator), beat_time)

    def convert_beat_length_to_bars_beats_sixteenths(self, clip, beat_length):
        return convert_beat_length_to_bars_beats_sixteenths((
         clip.signature_numerator, clip.signature_denominator), beat_length)

    def _on_clip_changed(self):
        self.__on_signature_denominator_changed.subject = self._loop_model.clip
        self.__on_signature_denominator_changed()
        self.__on_signature_numerator_changed.subject = self._loop_model.clip
        self.__on_signature_numerator_changed()

    @listens(b'signature_denominator')
    def __on_signature_denominator_changed(self):
        self.__update_position_sources()

    @listens(b'signature_numerator')
    def __on_signature_numerator_changed(self):
        self.__update_position_sources()

    def __update_position_sources(self):
        self._update_start_marker_source()
        self._update_loop_start_source()
        self._update_loop_end_source()
        self._update_position_source()

    @listens(b'looping')
    def __on_looping_changed(self):
        if self.is_enabled():
            self._update_is_looping_source()
            self._update_loop_end_source()
            self._update_start_marker_source()

    @listens(b'start_marker')
    def __on_start_marker_changed(self):
        self._update_start_marker_source()

    @listens(b'loop_start')
    def __on_loop_start_changed(self):
        self._update_loop_start_source()
        self._update_position_source()
        self._update_loop_end_source()

    @listens(b'loop_end')
    def __on_loop_end_changed(self):
        self._update_position_source()
        self._update_loop_end_source()

    def _update_start_marker_source(self):
        looping = self._loop_model.looping if liveobj_valid(self.clip) else False
        self._value_sources[2].set_display_string(self.convert_beat_time_to_bars_beats_sixteenths(self.clip, self._loop_model.start_marker) if looping else b'')

    def _update_is_looping_source(self):
        looping = self._loop_model.looping if liveobj_valid(self.clip) else False
        self._name_sources[0].set_display_string(b'Position' if looping else b'Start')
        self._name_sources[1].set_display_string(b'Length' if looping else b'End')
        self._name_sources[2].set_display_string(b'Offset' if looping else b'')

    def _update_loop_start_source(self):
        self._value_sources[0].set_display_string(self.convert_beat_time_to_bars_beats_sixteenths(self.clip, self._loop_model.loop_start) if self.clip else b'-')

    def _update_loop_end_source(self):
        if liveobj_valid(self.clip) and not is_new_recording(self.clip):
            looping = self._loop_model.looping
            self._value_sources[1].set_display_string(self.convert_beat_length_to_bars_beats_sixteenths(self.clip, self._loop_model.loop_length) if looping else self.convert_beat_time_to_bars_beats_sixteenths(self.clip, self._loop_model.loop_end))
            self._value_sources[3].set_display_string(b'On' if looping else b'Off')
        else:
            self._value_sources[1].set_display_string(b'-')
            self._value_sources[3].set_display_string(b'-')

    def _update_position_source(self):
        self._value_sources[0].set_display_string(self.convert_beat_time_to_bars_beats_sixteenths(self.clip, self._loop_model.position) if liveobj_valid(self.clip) else b'-')

    def update(self):
        super(LoopSettingsComponent, self).update()
        if self.is_enabled():
            for index, label in enumerate([b'Position', b'Length', b'Offset', b'Loop']):
                self._name_sources[index].set_display_string(label)

            self.__on_loop_start_changed()
            self.__on_loop_end_changed()
            self.__on_looping_changed()
            self.__on_start_marker_changed()


class AudioClipSettingsModel(EventObject):
    __events__ = ('pitch_fine', 'pitch_coarse', 'gain', 'warp_mode', 'warping')

    def __init__(self, *a, **k):
        super(AudioClipSettingsModel, self).__init__(*a, **k)
        self.clip = None
        return

    def _get_clip(self):
        return self._clip

    def _set_clip(self, clip):
        self._clip = clip
        self.__on_pitch_fine_changed.subject = self._clip
        self.__on_pitch_coarse_changed.subject = self._clip
        self.__on_gain_changed.subject = self._clip
        self.__on_warp_mode_changed.subject = self._clip
        self.__on_warping_changed.subject = self._clip

    clip = property(_get_clip, _set_clip)
    pitch_fine = forward_property(b'clip')(b'pitch_fine')
    pitch_coarse = forward_property(b'clip')(b'pitch_coarse')
    gain = forward_property(b'clip')(b'gain')
    warping = forward_property(b'clip')(b'warping')

    def _get_warp_mode(self):
        return self.clip.warp_mode

    def _set_warp_mode(self, value):
        if self.clip.warping:
            available_warp_modes = self.available_warp_modes
            warp_mode_index = available_warp_modes.index(self.clip.warp_mode)
            new_warp_mode_index = clamp(warp_mode_index + value, 0, len(available_warp_modes) - 1)
            self.clip.warp_mode = available_warp_modes[new_warp_mode_index]

    warp_mode = property(_get_warp_mode, _set_warp_mode)

    def set_clip_gain(self, value, fine_grained):
        self.clip.gain = clamp(self.clip.gain + value * self._encoder_factor(fine_grained), 0.0, 1.0)

    def set_clip_pitch_coarse(self, value, fine_grained):
        self.clip.pitch_coarse = int(clamp(self.clip.pitch_coarse + value * self._encoder_factor(fine_grained), -48.0, 48.0))

    def set_clip_pitch_fine(self, value, fine_grained):
        self.clip.pitch_fine = int(self.clip.pitch_fine + value * 100.0 * self._encoder_factor(fine_grained))

    def _encoder_factor(self, fine_grained):
        if fine_grained:
            return 0.1
        return 1.0

    @listens(b'pitch_fine')
    def __on_pitch_fine_changed(self):
        self.notify_pitch_fine()

    @listens(b'pitch_coarse')
    def __on_pitch_coarse_changed(self):
        self.notify_pitch_coarse()

    @listens(b'gain')
    def __on_gain_changed(self):
        self.notify_gain()

    @listens(b'warp_mode')
    def __on_warp_mode_changed(self):
        self.notify_warp_mode()

    @listens(b'warping')
    def __on_warping_changed(self):
        self.notify_warping()

    @property
    def available_warp_modes(self):
        if liveobj_valid(self.clip):
            return list(self.clip.available_warp_modes)
        return []


class AudioClipSettingsControllerComponent(Component):
    """
    Component for managing settings of an audio clip
    """
    warp_mode_encoder = StepEncoderControl()
    transpose_encoder = StepEncoderControl()
    detune_encoder = EncoderControl()
    gain_encoder = EncoderControl()
    shift_button = ButtonControl()

    def __init__(self, *a, **k):
        super(AudioClipSettingsControllerComponent, self).__init__(*a, **k)
        self._audio_clip_model = self.register_disconnectable(AudioClipSettingsModel())

    def _get_clip(self):
        return self._audio_clip_model.clip

    def _set_clip(self, clip):
        self._audio_clip_model.clip = clip
        self._update_encoder_enabled_state()
        self._on_clip_changed()

    clip = property(_get_clip, _set_clip)

    def _update_encoder_enabled_state(self):
        enabled = liveobj_valid(self.clip)
        self.warp_mode_encoder.enabled = self.transpose_encoder.enabled = self.detune_encoder.enabled = self.gain_encoder.enabled = enabled

    @warp_mode_encoder.value
    def warp_mode_encoder(self, value, encoder):
        self._on_clip_warp_mode_value(value)

    def _on_clip_warp_mode_value(self, value):
        self._audio_clip_model.warp_mode = value

    @transpose_encoder.value
    def transpose_encoder(self, value, encoder):
        self._on_transpose_encoder_value(value)

    def _on_transpose_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_coarse(value, self.shift_button.is_pressed)

    @detune_encoder.value
    def detune_encoder(self, value, encoder):
        self._on_detune_encoder_value(value)

    def _on_detune_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_fine(value, self.shift_button.is_pressed)

    @gain_encoder.value
    def gain_encoder(self, value, encoder):
        self._audio_clip_model.set_clip_gain(value, self.shift_button.is_pressed)


class AudioClipSettingsComponent(AudioClipSettingsControllerComponent):

    def __init__(self, *a, **k):
        super(AudioClipSettingsComponent, self).__init__(*a, **k)
        self._name_sources = [ DisplayDataSource() for _ in xrange(4) ]
        self._value_sources = [ DisplayDataSource() for _ in xrange(4) ]
        self.__on_pitch_fine_changed.subject = self._audio_clip_model
        self.__on_pitch_coarse_changed.subject = self._audio_clip_model
        self.__on_gain_changed.subject = self._audio_clip_model
        self.__on_warping_changed.subject = self._audio_clip_model
        self.__on_warp_mode_changed.subject = self._audio_clip_model

    def _on_clip_changed(self):
        self.update()

    def set_name_display(self, display):
        if display:
            display.set_data_sources(self._name_sources)

    def set_value_display(self, display):
        if display:
            display.set_data_sources(self._value_sources)

    @listens(b'warp_mode')
    def __on_warp_mode_changed(self):
        if self.is_enabled():
            self._update_warp_mode_source()

    @listens(b'warping')
    def __on_warping_changed(self):
        if self.is_enabled():
            self._update_warp_mode_source()

    @listens(b'gain')
    def __on_gain_changed(self):
        if self.is_enabled():
            self._update_gain_source()

    @listens(b'pitch_fine')
    def __on_pitch_fine_changed(self):
        if self.is_enabled():
            self._update_pitch_fine_source()

    @listens(b'pitch_coarse')
    def __on_pitch_coarse_changed(self):
        if self.is_enabled():
            self._update_pitch_coarse_source()

    def _update_warp_mode_source(self):
        display_value = b'-'
        if liveobj_valid(self.clip):
            display_value = WARP_MODE_NAMES[self.clip.warp_mode] if liveobj_valid(self.clip) and self.clip.warping else b'Off'
        self._value_sources[0].set_display_string(display_value)

    def _update_gain_source(self):
        value = self.clip.gain_display_string if liveobj_valid(self.clip) else b'-'
        self._value_sources[3].set_display_string(value)

    def _update_pitch_fine_source(self):
        value = str(int(self.clip.pitch_fine)) + b' ct' if liveobj_valid(self.clip) else b'-'
        self._value_sources[2].set_display_string(value)

    def _update_pitch_coarse_source(self):
        value = str(int(self.clip.pitch_coarse)) + b' st' if liveobj_valid(self.clip) else b'-'
        self._value_sources[1].set_display_string(value)

    def update(self):
        super(AudioClipSettingsComponent, self).update()
        if self.is_enabled():
            for index, label in enumerate([b'WarpMode', b'Transpose', b'Detune', b'Gain']):
                self._name_sources[index].set_display_string(label)

            self._update_warp_mode_source()
            self._update_gain_source()
            self._update_pitch_fine_source()
            self._update_pitch_coarse_source()


class ClipNameComponent(Component):
    """
    Component for showing the clip name
    """
    num_label_segments = 4

    def __init__(self, *a, **k):
        super(ClipNameComponent, self).__init__(*a, **k)
        self._clip = None
        self._name_data_sources = [ DisplayDataSource() for _ in xrange(self.num_label_segments) ]
        self._name_data_sources[0].set_display_string(b'Clip Selection:')
        return

    def _get_clip(self):
        return self._clip

    def _set_clip(self, clip):
        self._clip = clip
        self._update_clip_name()
        self._on_name_changed.subject = clip
        self.update()

    clip = property(_get_clip, _set_clip)

    def set_display(self, display):
        if display:
            display.set_num_segments(self.num_label_segments)
            for idx in xrange(self.num_label_segments):
                display.segment(idx).set_data_source(self._name_data_sources[idx])

    @listens(b'name')
    def _on_name_changed(self):
        if self.is_enabled():
            self._update_clip_name()

    def _name_for_clip(self, clip):
        if clip:
            if clip.name:
                return clip.name
            return b'[unnamed]'
        return b'[none]'

    def _update_clip_name(self):
        self._name_data_sources[1].set_display_string(self._name_for_clip(self._clip))

    def update(self):
        super(ClipNameComponent, self).update()
        if self.is_enabled():
            self._update_clip_name()


class ClipControlComponent(ModesComponent):
    """
    Component that modifies clip properties
    """

    def __init__(self, loop_layer=None, audio_layer=None, clip_name_layer=None, *a, **k):
        super(ClipControlComponent, self).__init__(*a, **k)
        self._audio_clip_settings = AudioClipSettingsComponent(parent=self, is_enabled=False, layer=audio_layer)
        self._loop_settings = LoopSettingsComponent(parent=self, is_enabled=False, layer=loop_layer)
        self._clip_name = ClipNameComponent(parent=self, is_enabled=False, layer=clip_name_layer)
        self.add_mode(b'no_clip', (self._clip_name,))
        self.add_mode(b'midi', (self._loop_settings, self._clip_name))
        self.add_mode(b'audio', (self._loop_settings, self._audio_clip_settings, self._clip_name))
        self.selected_mode = b'no_clip'
        self._update_clip()
        self._on_detail_clip_changed.subject = self.song.view
        self._on_selected_scene_changed.subject = self.song.view
        self._on_selected_track_changed.subject = self.song.view

    @listens(b'selected_scene')
    def _on_selected_scene_changed(self):
        self._update_clip()

    @listens(b'selected_track')
    def _on_selected_track_changed(self):
        self._update_clip()

    @listens(b'detail_clip')
    def _on_detail_clip_changed(self):
        self._update_clip()

    def update(self):
        super(ClipControlComponent, self).update()
        if self.is_enabled():
            self._update_clip()

    def _update_mode(self):
        track = self.song.view.selected_track
        new_mode = b'no_clip'
        if track.clip_slots and (track.has_midi_input or track.has_audio_input):
            new_mode = b'midi' if track.has_midi_input else b'audio'
        self.selected_mode = new_mode

    def _update_clip(self):
        self._update_mode()
        clip = self.song.view.detail_clip if self.is_enabled() else None
        audio_clip = clip if liveobj_valid(clip) and clip.is_audio_clip else None
        self._clip_name.clip = clip
        self._loop_settings.clip = clip
        self._audio_clip_settings.clip = audio_clip
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/pushbase/clip_control_component.pyc
