# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\simpler_decoration.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from math import ceil, floor
import Live
from ..base import clamp, liveobj_valid, listenable_property, listens, sign, EventObject
from ..base.collection import IndexedDict
from .decoration import LiveObjectDecorator
from .internal_parameter import EnumWrappingParameter, RelativeInternalParameter, to_percentage_display, WrappingParameter
BoolWrappingParameter = partial(WrappingParameter, to_property_value=lambda integer, _simpler: bool(integer), from_property_value=lambda boolean, _simpler: int(boolean), value_items=[
 b'Off', b'On'], display_value_conversion=lambda val: b'On' if val else b'Off')

def from_user_range(minv, maxv):
    return lambda v, s: (v - minv) / float(maxv - minv)


def to_user_range(minv, maxv):
    return lambda v, s: clamp(v * (maxv - minv) + minv, minv, maxv)


def to_user_range_quantized(minv, maxv):
    user_range_transform = to_user_range(minv, maxv)
    return lambda v, s: int(round(user_range_transform(v, s)))


def from_sample_count(value, sample):
    return float(value) / sample.length


def to_sample_count(prev_value_getter, value, sample):
    truncation_func = ceil if sign(value - prev_value_getter()) > 0 else floor
    return clamp(int(truncation_func(value * sample.length)), 0, sample.length - 1)


SimplerWarpModes = IndexedDict((
 (
  Live.Clip.WarpMode.beats, b'Beats'),
 (
  Live.Clip.WarpMode.tones, b'Tones'),
 (
  Live.Clip.WarpMode.texture, b'Texture'),
 (
  Live.Clip.WarpMode.repitch, b'Re-Pitch'),
 (
  Live.Clip.WarpMode.complex, b'Complex'),
 (
  Live.Clip.WarpMode.complex_pro, b'Pro')))

class SimplerDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, *a, **k):
        super(SimplerDeviceDecorator, self).__init__(*a, **k)
        self._sample_based_parameters = []
        self._additional_parameters = []
        self.setup_parameters()
        self.register_disconnectables(self._decorated_parameters())
        self.__on_playback_mode_changed.subject = self._live_object
        self.__on_sample_changed.subject = self._live_object
        self.__on_slices_changed.subject = self._live_object.sample

    def setup_parameters(self):
        self.start = WrappingParameter(name=b'Start', parent=self, property_host=self._live_object.sample, source_property=b'start_marker', from_property_value=from_sample_count, to_property_value=partial(to_sample_count, lambda : self.start.linear_value))
        self.end = WrappingParameter(name=b'End', parent=self, property_host=self._live_object.sample, source_property=b'end_marker', from_property_value=from_sample_count, to_property_value=partial(to_sample_count, lambda : self.end.linear_value))
        self.sensitivity = WrappingParameter(name=b'Sensitivity', parent=self, property_host=self._live_object.sample, source_property=b'slicing_sensitivity', display_value_conversion=to_percentage_display)
        self.mode = EnumWrappingParameter(name=b'Mode', parent=self, values_host=self, index_property_host=self, values_property=b'available_playback_modes', index_property=b'playback_mode')
        self.slicing_playback_mode_param = EnumWrappingParameter(name=b'Playback', parent=self, values_host=self, index_property_host=self, values_property=b'available_slicing_playback_modes', index_property=b'slicing_playback_mode')
        self.pad_slicing_param = BoolWrappingParameter(name=b'Pad Slicing', parent=self, property_host=self._live_object, source_property=b'pad_slicing')
        self.nudge = RelativeInternalParameter(name=b'Nudge', parent=self)
        self.multi_sample_mode_param = BoolWrappingParameter(name=b'Multi Sample', parent=self, property_host=self._live_object, source_property=b'multi_sample_mode')
        self.warp = BoolWrappingParameter(name=b'Warp', parent=self, property_host=self._live_object.sample, source_property=b'warping')
        self.warp_mode_param = EnumWrappingParameter(name=b'Warp Mode', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=b'available_warp_modes', index_property=b'warp_mode', to_index_conversion=lambda i: Live.Clip.WarpMode(SimplerWarpModes.key_by_index(i)), from_index_conversion=lambda i: SimplerWarpModes.index_by_key(i))
        self.voices_param = EnumWrappingParameter(name=b'Voices', parent=self, values_host=self, index_property_host=self, values_property=b'available_voice_numbers', index_property=b'voices', to_index_conversion=lambda i: self.available_voice_numbers[i], from_index_conversion=lambda i: self.available_voice_numbers.index(i))
        self.granulation_resolution = EnumWrappingParameter(name=b'Preserve', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=b'available_resolutions', index_property=b'beats_granulation_resolution')
        self.transient_loop_mode = EnumWrappingParameter(name=b'Loop Mode', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=b'available_transient_loop_modes', index_property=b'beats_transient_loop_mode')
        self.transient_envelope = WrappingParameter(name=b'Envelope', parent=self, property_host=self._live_object.sample, source_property=b'beats_transient_envelope', from_property_value=from_user_range(0.0, 100.0), to_property_value=to_user_range(0.0, 100.0))
        self.tones_grain_size_param = WrappingParameter(name=b'Grain Size Tones', parent=self, property_host=self._live_object.sample, source_property=b'tones_grain_size', from_property_value=from_user_range(12.0, 100.0), to_property_value=to_user_range(12.0, 100.0))
        self.texture_grain_size_param = WrappingParameter(name=b'Grain Size Texture', parent=self, property_host=self._live_object.sample, source_property=b'texture_grain_size', from_property_value=from_user_range(2.0, 263.0), to_property_value=to_user_range(2.0, 263.0))
        self.flux = WrappingParameter(name=b'Flux', parent=self, property_host=self._live_object.sample, source_property=b'texture_flux', from_property_value=from_user_range(0.0, 100.0), to_property_value=to_user_range(0.0, 100.0))
        self.formants = WrappingParameter(name=b'Formants', parent=self, property_host=self._live_object.sample, source_property=b'complex_pro_formants', from_property_value=from_user_range(0.0, 100.0), to_property_value=to_user_range(0.0, 100.0))
        self.complex_pro_envelope_param = WrappingParameter(name=b'Envelope Complex Pro', parent=self, property_host=self._live_object.sample, source_property=b'complex_pro_envelope', from_property_value=from_user_range(8.0, 256.0), to_property_value=to_user_range(8.0, 256.0))
        self.gain_param = WrappingParameter(name=b'Gain', parent=self, property_host=self._live_object.sample, source_property=b'gain', display_value_conversion=lambda _: self._live_object.sample.gain_display_string() if liveobj_valid(self._live_object) and liveobj_valid(self._live_object.sample) else b'')
        self.slicing_style_param = EnumWrappingParameter(name=b'Slice by', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=b'available_slice_styles', index_property=b'slicing_style')
        self.slicing_beat_division_param = EnumWrappingParameter(name=b'Division', parent=self, values_host=self, index_property_host=self._live_object.sample, values_property=b'available_slicing_beat_divisions', index_property=b'slicing_beat_division')
        self.slicing_region_count_param = WrappingParameter(name=b'Regions', parent=self, property_host=self._live_object.sample, source_property=b'slicing_region_count', from_property_value=from_user_range(2, 64), to_property_value=to_user_range_quantized(2, 64))
        self._sample_based_parameters.extend([
         self.start,
         self.end,
         self.sensitivity,
         self.warp,
         self.transient_envelope,
         self.tones_grain_size_param,
         self.texture_grain_size_param,
         self.flux,
         self.formants,
         self.complex_pro_envelope_param,
         self.gain_param,
         self.slicing_region_count_param,
         self.warp_mode_param,
         self.granulation_resolution,
         self.transient_loop_mode,
         self.slicing_style_param,
         self.slicing_beat_division_param])
        self._additional_parameters.extend([
         self.mode,
         self.slicing_playback_mode_param,
         self.pad_slicing_param,
         self.nudge,
         self.multi_sample_mode_param,
         self.voices_param])

    def _decorated_parameters(self):
        return tuple(self._sample_based_parameters) + tuple(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._decorated_parameters()

    @property
    def available_playback_modes(self):
        return [
         b'Classic', b'One-Shot', b'Slicing']

    @property
    def available_slicing_playback_modes(self):
        return [
         b'Mono', b'Poly', b'Thru']

    @property
    def available_voice_numbers(self):
        return list(Live.SimplerDevice.get_available_voice_numbers())

    @property
    def available_warp_modes(self):
        return SimplerWarpModes.values()

    @property
    def available_resolutions(self):
        return ('1 Bar', '1/2', '1/4', '1/8', '1/16', '1/32', 'Transients')

    @property
    def available_slice_styles(self):
        return ('Transient', 'Beat', 'Region', 'Manual')

    @property
    def available_slicing_beat_divisions(self):
        return ('1/16', '1/16T', '1/8', '1/8T', '1/4', '1/4T', '1/2', '1/2T', '1 Bar',
                '2 Bars', '4 Bars')

    @property
    def available_transient_loop_modes(self):
        return ('Off', 'Forward', 'Alternate')

    @listenable_property
    def current_playback_mode(self):
        return self._live_object.playback_mode

    @listenable_property
    def slices(self):
        if liveobj_valid(self._live_object) and liveobj_valid(self._live_object.sample):
            return self._live_object.sample.slices
        return []

    @listens(b'sample')
    def __on_sample_changed(self):
        self._on_sample_changed()

    def _on_sample_changed(self):
        self._reconnect_sample_listeners()

    def _reconnect_sample_listeners(self):
        for param in self._sample_based_parameters:
            param.set_property_host(self._live_object.sample)

        self._reconnect_to_slices()

    def _reconnect_to_slices(self):
        self.__on_slices_changed.subject = self._live_object.sample
        self.notify_slices()

    @listens(b'slices')
    def __on_slices_changed(self):
        self._on_slices_changed()

    def _on_slices_changed(self):
        self.notify_slices()

    @listens(b'playback_mode')
    def __on_playback_mode_changed(self):
        self.notify_current_playback_mode()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/simpler_decoration.pyc
