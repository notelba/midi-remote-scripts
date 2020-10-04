# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\simpler.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import depends, find_if, listenable_property, listens, liveobj_valid
from ableton.v2.control_surface import EnumWrappingParameter, NotifyingList, SimplerDeviceDecorator as SimplerDeviceDecoratorBase, get_parameter_by_name
from pushbase.message_box_component import Messenger
from .device_component import DeviceComponentWithTrackColorViewData, extend_with_envelope_features_for_parameter, make_vector
from .device_decoration import DeviceSwitchOption, SimplerPositions, WaveformNavigationParameter
from .device_options import DeviceTriggerOption, DeviceOnOffOption
from .real_time_channel import RealTimeDataComponent
from .visualisation_settings import VisualisationGuides
RESET_SLICING_NOTIFICATION = b'Slicing has been reset'
MAX_NUMBER_SLICES = 64

def center_point(start, end):
    return int((end - start) / 2.0) + start


def insert_new_slice(simpler):
    sample = simpler.sample
    view = simpler.view
    slices = list(sample.slices) + [sample.end_marker]
    selected_slice = view.selected_slice
    if selected_slice in slices:
        slice_index = slices.index(selected_slice)
        new_slice_point = center_point(selected_slice, slices[(slice_index + 1)])
        if new_slice_point not in slices:
            sample.insert_slice(new_slice_point)
            view.selected_slice = new_slice_point


class EnvelopeType(int):
    pass


EnvelopeType.volume_env = EnvelopeType(0)
EnvelopeType.filter_env = EnvelopeType(1)
EnvelopeType.pitch_env = EnvelopeType(2)

class SimplerDeviceDecorator(SimplerDeviceDecoratorBase, Messenger):
    waveform_real_time_channel_id = b''
    playhead_real_time_channel_id = b''

    @depends(song=None)
    def __init__(self, song=None, *a, **k):
        self._song = song
        self._envelope_types_provider = NotifyingList(available_values=[
         b'Volume', b'Filter', b'Pitch'], default_value=EnvelopeType.volume_env)
        super(SimplerDeviceDecorator, self).__init__(*a, **k)
        self.setup_options()
        self.register_disconnectables(self.options)
        self.__on_parameters_changed.subject = self._live_object
        self.__on_signature_numerator_changed.subject = song
        self.__on_can_warp_as_changed.subject = self._live_object
        self.__on_can_warp_half_changed.subject = self._live_object
        self.__on_can_warp_double_changed.subject = self._live_object
        self.__on_start_marker_changed.subject = self._live_object.sample
        self.__on_end_marker_changed.subject = self._live_object.sample
        self.__on_selected_slice_changed.subject = self._live_object.view
        self.__on_envelope_type_changed.subject = self.envelope

    def setup_parameters(self):
        super(SimplerDeviceDecorator, self).setup_parameters()
        self.positions = self.register_disconnectable(SimplerPositions(self))
        self.zoom = WaveformNavigationParameter(name=b'Zoom', parent=self, simpler=self)
        self.zoom.focus_region_of_interest(b'start_end_marker', self.get_parameter_by_name(b'Start'))
        self.zoom.add_waveform_navigation_listener(self.notify_waveform_navigation)
        self.envelope = EnumWrappingParameter(name=b'Env. Type', parent=self, values_host=self._envelope_types_provider, index_property_host=self._envelope_types_provider, values_property=b'available_values', index_property=b'index', value_type=EnvelopeType)
        self._additional_parameters.extend([self.zoom, self.envelope])

    def setup_options(self):

        def get_simpler_flag(name):
            return liveobj_valid(self._live_object) and getattr(self._live_object, name)

        def call_simpler_function(name, *a):
            if liveobj_valid(self._live_object):
                return getattr(self._live_object, name)(*a)

        def sample_available():
            return liveobj_valid(self._live_object) and liveobj_valid(self._live_object.sample)

        def call_sample_function(name, *a):
            if sample_available():
                return getattr(self._live_object.sample, name)(*a)

        def reset_slices():
            call_sample_function(b'reset_slices')
            self.show_notification(RESET_SLICING_NOTIFICATION)

        def split_slice_available():
            if sample_available():
                slices = self._live_object.sample.slices
                return len(slices) != MAX_NUMBER_SLICES or slices[(-1)] != self._live_object.view.selected_slice
            return False

        self.crop_option = DeviceTriggerOption(name=b'Crop', callback=partial(call_simpler_function, b'crop'))
        self.reverse_option = DeviceTriggerOption(name=b'Reverse', callback=partial(call_simpler_function, b'reverse'))
        self.one_shot_sustain_mode_option = DeviceSwitchOption(name=b'Trigger Mode', parameter=get_parameter_by_name(self, b'Trigger Mode'))
        self.retrigger_option = DeviceOnOffOption(name=b'Retrigger', property_host=self._live_object, value_property_name=b'retrigger')
        self.warp_as_x_bars_option = DeviceTriggerOption(name=b'Warp as X Bars', default_label=self.get_warp_as_option_label(), callback=lambda : call_simpler_function(b'warp_as', call_simpler_function(b'guess_playback_length')), is_active=lambda : get_simpler_flag(b'can_warp_as'))
        self.warp_half_option = DeviceTriggerOption(name=b':2', callback=partial(call_simpler_function, b'warp_half'), is_active=lambda : get_simpler_flag(b'can_warp_half'))
        self.warp_double_option = DeviceTriggerOption(name=b'x2', callback=partial(call_simpler_function, b'warp_double'), is_active=lambda : get_simpler_flag(b'can_warp_double'))
        self.lfo_sync_option = DeviceSwitchOption(name=b'LFO Sync Type', parameter=get_parameter_by_name(self, b'L Sync'))
        self.loop_option = DeviceOnOffOption(name=b'Loop', property_host=get_parameter_by_name(self, b'S Loop On'))
        self.filter_slope_option = DeviceSwitchOption(name=b'Filter Slope', parameter=get_parameter_by_name(self, b'Filter Slope'))
        self.clear_slices_action = DeviceTriggerOption(name=b'Clear Slices', default_label=b'Clear Slices', callback=lambda : call_sample_function(b'clear_slices'), is_active=lambda : sample_available() and len(self._live_object.sample.slices) > 1)
        self.reset_slices_action = DeviceTriggerOption(name=b'Reset Slices', default_label=b'Reset Slices', callback=reset_slices, is_active=lambda : sample_available())
        self.split_slice_action = DeviceTriggerOption(name=b'Split Slice', default_label=b'Split Slice', callback=lambda : insert_new_slice(self._live_object), is_active=split_slice_available)

    def get_parameter_by_name(self, name):
        return find_if(lambda p: p.name == name, self.parameters)

    @property
    def options(self):
        return (
         self.crop_option,
         self.reverse_option,
         self.one_shot_sustain_mode_option,
         self.retrigger_option,
         self.warp_as_x_bars_option,
         self.warp_half_option,
         self.warp_double_option,
         self.lfo_sync_option,
         self.loop_option,
         self.filter_slope_option,
         self.clear_slices_action,
         self.reset_slices_action,
         self.split_slice_action)

    @listenable_property
    def waveform_navigation(self):
        return self.zoom.waveform_navigation

    @property
    def available_resolutions(self):
        return ('1 Bar', '½', '¼', '⅛', '\ue001', '\ue002', 'Transients')

    @property
    def available_slicing_beat_divisions(self):
        return ('\ue001', '\ue001T', '⅛', '⅛T', '¼', '¼T', '½', '½T', '1 Bar', '2 Bars',
                '4 Bars')

    @listens(b'parameters')
    def __on_parameters_changed(self):
        self.lfo_sync_option.set_parameter(get_parameter_by_name(self, b'L Sync'))
        self.filter_slope_option.set_parameter(get_parameter_by_name(self, b'Filter Slope'))

    def _reconnect_sample_listeners(self):
        super(SimplerDeviceDecorator, self)._reconnect_sample_listeners()
        self._reconnect_to_markers()
        self._update_warp_as_label()
        self.positions.post_sample_changed()
        self.zoom.post_sample_changed()
        self.zoom.focus_region_of_interest(b'start_end_marker', self.get_parameter_by_name(b'Start'))

    def _reconnect_to_markers(self):
        self.__on_start_marker_changed.subject = self._live_object.sample
        self.__on_end_marker_changed.subject = self._live_object.sample

    def _update_warp_as_label(self):
        self.warp_as_x_bars_option.default_label = self.get_warp_as_option_label()

    @listens(b'start_marker')
    def __on_start_marker_changed(self):
        self._update_warp_as_label()

    @listens(b'end_marker')
    def __on_end_marker_changed(self):
        self._update_warp_as_label()

    @listens(b'signature_numerator')
    def __on_signature_numerator_changed(self):
        self._update_warp_as_label()

    @listens(b'can_warp_as')
    def __on_can_warp_as_changed(self):
        self.warp_as_x_bars_option.notify_active()

    @listens(b'can_warp_half')
    def __on_can_warp_half_changed(self):
        self.warp_half_option.notify_active()

    @listens(b'can_warp_double')
    def __on_can_warp_double_changed(self):
        self.warp_double_option.notify_active()

    @listens(b'selected_slice')
    def __on_selected_slice_changed(self):
        self.split_slice_action.notify_active()

    def _on_sample_changed(self):
        super(SimplerDeviceDecorator, self)._on_sample_changed()
        self.clear_slices_action.notify_active()
        self.reset_slices_action.notify_active()
        self.split_slice_action.notify_active()

    def _on_slices_changed(self):
        super(SimplerDeviceDecorator, self)._on_slices_changed()
        self.clear_slices_action.notify_active()

    def get_warp_as_option_label(self):
        try:
            bars = int(self._live_object.guess_playback_length() / self._song.signature_numerator)
            return b'Warp as %d Bar%s' % (bars, b's' if bars > 1 else b'')
        except RuntimeError:
            return b'Warp as X Bars'

    @listenable_property
    def envelope_type_index(self):
        return self._envelope_types_provider.index

    @listens(b'value')
    def __on_envelope_type_changed(self):
        self.notify_envelope_type_index()


class SimplerDeviceComponent(DeviceComponentWithTrackColorViewData):
    ZOOM_SENSITIVE_PARAMETERS = ('S Start', 'S Length', 'Start', 'End', 'Nudge')
    PARAMETERS_RELATIVE_TO_ACTIVE_AREA = ('S Start', 'S Length')
    ENVELOPE_PREFIXES = [
     b'Ve', b'Fe', b'Pe', b'']

    def __init__(self, *a, **k):
        super(SimplerDeviceComponent, self).__init__(*a, **k)
        self._playhead_real_time_data = RealTimeDataComponent(parent=self, channel_type=b'playhead')
        self._waveform_real_time_data = RealTimeDataComponent(parent=self, channel_type=b'waveform')
        self.__on_playhead_channel_changed.subject = self._playhead_real_time_data
        self.__on_waveform_channel_changed.subject = self._waveform_real_time_data

    def _set_device_for_subcomponents(self, device):
        super(SimplerDeviceComponent, self)._set_device_for_subcomponents(device)
        self._playhead_real_time_data.set_data(device)
        self._waveform_real_time_data.set_data(device)

    def _set_decorated_device_for_subcomponents(self, decorated_device):
        super(SimplerDeviceComponent, self)._set_decorated_device_for_subcomponents(decorated_device)
        self.__on_sample_or_file_path_changed.subject = decorated_device
        self.__on_waveform_visible_region_changed.subject = decorated_device
        if liveobj_valid(decorated_device):
            decorated_device.zoom.reset_focus_and_animation()

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            self._decorated_device.zoom.touch_object(parameter)
        self._update_visualisation_view_data(self._visualisation_data())

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            self._decorated_device.zoom.release_object(parameter)
        self._update_visualisation_view_data(self._visualisation_data())

    def parameters_changed(self):
        self._update_visualisation_view_data(self._visualisation_data())

    def _is_parameter_available(self, parameter):
        name = parameter.name if liveobj_valid(parameter) else b''
        return not self._in_multisample_mode() or name not in self.ZOOM_SENSITIVE_PARAMETERS + ('Zoom', )

    def _adjust_parameter_sensitivity(self, parameter, sensitivity):
        device = self._decorated_device
        if liveobj_valid(device) and liveobj_valid(device.sample):
            if parameter.name in self.ZOOM_SENSITIVE_PARAMETERS and device.waveform_navigation is not None:
                sensitivity *= device.waveform_navigation.visible_proportion
            if parameter.name in self.PARAMETERS_RELATIVE_TO_ACTIVE_AREA:
                active_area_quotient = device.sample.length / float(device.sample.end_marker - device.sample.start_marker + 1)
                sensitivity *= active_area_quotient
        return sensitivity

    @listens(b'channel_id')
    def __on_playhead_channel_changed(self):
        self._update_real_time_channel(b'playhead')

    @listens(b'channel_id')
    def __on_waveform_channel_changed(self):
        self._update_real_time_channel(b'waveform')

    @listens(b'sample.file_path')
    def __on_sample_or_file_path_changed(self):
        self._waveform_real_time_data.invalidate()

    @listens(b'waveform_navigation.visible_region')
    def __on_waveform_visible_region_changed(self, *a):
        self._update_parameter_sensitivities()

    def _update_parameter_sensitivities(self):
        changed_parameters = False
        for index, info in enumerate(self._provided_parameters):
            if info.name in self.ZOOM_SENSITIVE_PARAMETERS:
                self._provided_parameters[index] = self._create_parameter_info(info.parameter, info.name)
                changed_parameters = True

        if changed_parameters:
            self.notify_parameters()

    def _in_multisample_mode(self):
        return liveobj_valid(self._decorated_device) and self._decorated_device.multi_sample_mode

    def _update_real_time_channel(self, channel_name):
        if liveobj_valid(self._decorated_device):
            rt_data = getattr(self, b'_%s_real_time_data' % channel_name)
            setattr(self._decorated_device, channel_name + b'_real_time_channel_id', rt_data.channel_id)

    @property
    def wants_waveform_shown(self):
        return getattr(self._bank, b'wants_waveform_shown', True)

    def disconnect(self):
        super(SimplerDeviceComponent, self).disconnect()
        self._playhead_real_time_data.set_data(None)
        self._waveform_real_time_data.set_data(None)
        return

    def _set_bank_index(self, bank):
        super(SimplerDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._visualisation_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    def _set_decorated_device(self, decorated_device):
        super(SimplerDeviceComponent, self)._set_decorated_device(decorated_device)
        self.__on_selected_envelope_type_changed.subject = decorated_device

    @property
    def selected_envelope_type(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.envelope_type_index
        return 0

    @listens(b'envelope_type_index')
    def __on_selected_envelope_type_changed(self):
        self._update_visualisation_view_data(self._visualisation_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    @property
    def _envelope_visible(self):
        return self._bank != None and self._bank.index == 2

    @property
    def _filter_visible(self):
        return self._bank != None and self._bank.index == 4

    @property
    def _visualisation_visible(self):
        return self._filter_visible or self._envelope_visible

    @property
    def _shrink_parameters(self):
        if self._envelope_visible:
            left_button = self.envelope_left_button
            right_button = left_button + 3
            return [ index >= left_button and index <= right_button for index in range(8) ]
        else:
            if self._filter_visible:
                return [ index >= 1 and index <= 3 for index in range(8) ]
            return [
             False] * 8

    def _initial_visualisation_view_data(self):
        view_data = super(SimplerDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._visualisation_data())
        return view_data

    @property
    def envelope_left_button(self):
        if self.selected_envelope_type == 0:
            return 1
        return 2

    def _visualisation_data(self):
        data = self._envelope_visualisation_data()
        data.update(self._filter_visualisation_data())
        return data

    def _envelope_visualisation_data(self):
        left_button = self.envelope_left_button
        right_button = left_button + 3
        shown_features = set([
         b'AttackLine',
         b'DecayLine',
         b'SustainLine',
         b'ReleaseLine',
         b'FadeInLine',
         b'FadeOutLine'])
        for parameter in self.parameters:
            extend_with_envelope_features_for_parameter(shown_features, parameter, self.ENVELOPE_PREFIXES)

        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed
                             ]
        focused_features = set()
        for parameter in touched_parameters:
            extend_with_envelope_features_for_parameter(focused_features, parameter, self.ENVELOPE_PREFIXES)

        return {b'EnvelopeVisible': self._envelope_visible, 
           b'EnvelopeName': [
                           b'Volume', b'Filter', b'Pitch'][self.selected_envelope_type], 
           b'EnvelopeLeft': VisualisationGuides.light_left_x(left_button), 
           b'EnvelopeRight': VisualisationGuides.light_right_x(right_button), 
           b'EnvelopeShow': make_vector(shown_features), 
           b'EnvelopeFocus': make_vector(focused_features)}

    def _filter_visualisation_data(self):
        left_column = 1
        right_column = 3
        return {b'FilterVisible': self._filter_visible, 
           b'FilterLeft': VisualisationGuides.light_left_x(left_column), 
           b'FilterRight': VisualisationGuides.light_right_x(right_column), 
           b'FilterFocus': any([ button.is_pressed for index, button in enumerate(self.parameter_touch_buttons) if index >= left_column and index <= right_column
                         ])}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/simpler.pyc
