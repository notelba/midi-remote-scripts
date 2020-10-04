# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\LomTypes.py
# Compiled at: 2020-07-31 16:17:47
from __future__ import absolute_import, print_function, unicode_literals
import ast
from collections import namedtuple
import json, types, Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ControlElement import ControlElement
from _Framework.Util import is_iterable

class MFLPropertyFormats:
    Default, JSON = range(2)


_MFLProperty = namedtuple(b'MFLProperty', b'name format to_json from_json min_epii_version')

def MFLProperty(name, format=MFLPropertyFormats.Default, to_json=None, from_json=None, min_epii_version=(-1, -1)):
    return _MFLProperty(name, format, to_json, from_json, min_epii_version)


def data_dict_to_json(property_name, data_dict):
    return json.dumps({property_name: data_dict})


def json_to_data_dict(property_name, json_dict):
    data_dict = ast.literal_eval(json_dict)
    return data_dict.get(property_name, data_dict)


def verify_routings_available_for_object(obj, prop_name):
    if isinstance(obj, Live.Track.Track):
        error_format = b"'%s' not available on %s"
        song = obj.canonical_parent
        if obj == song.master_track:
            raise RuntimeError(error_format % (prop_name, b'master track'))
        elif b'input' in prop_name:
            if obj.is_foldable:
                raise RuntimeError(error_format % (prop_name, b'group tracks'))
            elif obj in song.return_tracks:
                raise RuntimeError(error_format % (prop_name, b'return tracks'))


def routing_object_to_dict(routing_type):
    return {b'display_name': routing_type.display_name, b'identifier': hash(routing_type)}


def available_routing_objects_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, tuple([ routing_object_to_dict(t) for t in property_value ]))


def available_routing_input_types_to_json(obj):
    return available_routing_objects_to_json(obj, b'available_input_routing_types')


def available_routing_output_types_to_json(obj):
    return available_routing_objects_to_json(obj, b'available_output_routing_types')


def available_routing_input_channels_to_json(obj):
    return available_routing_objects_to_json(obj, b'available_input_routing_channels')


def available_routing_output_channels_to_json(obj):
    return available_routing_objects_to_json(obj, b'available_output_routing_channels')


def available_routing_types_to_json(device):
    return available_routing_objects_to_json(device, b'available_routing_types')


def available_routing_channels_to_json(device):
    return available_routing_objects_to_json(device, b'available_routing_channels')


def routing_object_to_json(obj, property_name):
    verify_routings_available_for_object(obj, property_name)
    property_value = getattr(obj, property_name)
    return data_dict_to_json(property_name, routing_object_to_dict(property_value))


def routing_input_type_to_json(obj):
    return routing_object_to_json(obj, b'input_routing_type')


def routing_output_type_to_json(obj):
    return routing_object_to_json(obj, b'output_routing_type')


def routing_input_channel_to_json(obj):
    return routing_object_to_json(obj, b'input_routing_channel')


def routing_output_channel_to_json(obj):
    return routing_object_to_json(obj, b'output_routing_channel')


def routing_type_to_json(device):
    return routing_object_to_json(device, b'routing_type')


def routing_channel_to_json(device):
    return routing_object_to_json(device, b'routing_channel')


def json_to_routing_object(obj, property_name, json_dict):
    verify_routings_available_for_object(obj, property_name)
    objects = getattr(obj, b'available_%ss' % property_name, [])
    identifier = json_to_data_dict(property_name, json_dict)[b'identifier']
    for routing_object in objects:
        if hash(routing_object) == identifier:
            return routing_object

    return


def json_to_input_routing_type(obj, json_dict):
    return json_to_routing_object(obj, b'input_routing_type', json_dict)


def json_to_output_routing_type(obj, json_dict):
    return json_to_routing_object(obj, b'output_routing_type', json_dict)


def json_to_input_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, b'input_routing_channel', json_dict)


def json_to_output_routing_channel(obj, json_dict):
    return json_to_routing_object(obj, b'output_routing_channel', json_dict)


def json_to_routing_type(device, json_dict):
    return json_to_routing_object(device, b'routing_type', json_dict)


def json_to_routing_channel(device, json_dict):
    return json_to_routing_object(device, b'routing_channel', json_dict)


_DEVICE_BASE_PROPS = [
 MFLProperty(b'canonical_parent'),
 MFLProperty(b'parameters'),
 MFLProperty(b'view'),
 MFLProperty(b'can_have_chains'),
 MFLProperty(b'can_have_drum_pads'),
 MFLProperty(b'class_display_name'),
 MFLProperty(b'class_name'),
 MFLProperty(b'is_active'),
 MFLProperty(b'name'),
 MFLProperty(b'type'),
 MFLProperty(b'store_chosen_bank')]
_DEVICE_VIEW_BASE_PROPS = [
 MFLProperty(b'canonical_parent'), MFLProperty(b'is_collapsed')]
_CHAIN_BASE_PROPS = [
 MFLProperty(b'canonical_parent'),
 MFLProperty(b'devices'),
 MFLProperty(b'mixer_device'),
 MFLProperty(b'color'),
 MFLProperty(b'color_index'),
 MFLProperty(b'is_auto_colored'),
 MFLProperty(b'has_audio_input'),
 MFLProperty(b'has_audio_output'),
 MFLProperty(b'has_midi_input'),
 MFLProperty(b'has_midi_output'),
 MFLProperty(b'mute'),
 MFLProperty(b'muted_via_solo'),
 MFLProperty(b'name'),
 MFLProperty(b'solo'),
 MFLProperty(b'delete_device')]
EXPOSED_TYPE_PROPERTIES = {Live.Application.Application: (
                                MFLProperty(b'view'),
                                MFLProperty(b'current_dialog_button_count'),
                                MFLProperty(b'current_dialog_message'),
                                MFLProperty(b'open_dialog_count'),
                                MFLProperty(b'get_bugfix_version'),
                                MFLProperty(b'get_document'),
                                MFLProperty(b'get_major_version'),
                                MFLProperty(b'get_minor_version'),
                                MFLProperty(b'press_current_dialog_button'),
                                MFLProperty(b'control_surfaces')), 
   Live.Application.Application.View: (
                                     MFLProperty(b'canonical_parent'),
                                     MFLProperty(b'browse_mode'),
                                     MFLProperty(b'focused_document_view'),
                                     MFLProperty(b'available_main_views'),
                                     MFLProperty(b'focus_view'),
                                     MFLProperty(b'hide_view'),
                                     MFLProperty(b'is_view_visible'),
                                     MFLProperty(b'scroll_view'),
                                     MFLProperty(b'show_view'),
                                     MFLProperty(b'toggle_browse'),
                                     MFLProperty(b'zoom_view')), 
   Live.Chain.Chain: tuple(_CHAIN_BASE_PROPS), 
   Live.ChainMixerDevice.ChainMixerDevice: (
                                          MFLProperty(b'canonical_parent'),
                                          MFLProperty(b'chain_activator'),
                                          MFLProperty(b'panning'),
                                          MFLProperty(b'sends'),
                                          MFLProperty(b'volume')), 
   Live.Clip.Clip: (
                  MFLProperty(b'canonical_parent'),
                  MFLProperty(b'view'),
                  MFLProperty(b'available_warp_modes'),
                  MFLProperty(b'color'),
                  MFLProperty(b'color_index'),
                  MFLProperty(b'crop'),
                  MFLProperty(b'end_marker'),
                  MFLProperty(b'end_time'),
                  MFLProperty(b'gain'),
                  MFLProperty(b'gain_display_string'),
                  MFLProperty(b'file_path'),
                  MFLProperty(b'has_envelopes'),
                  MFLProperty(b'is_arrangement_clip'),
                  MFLProperty(b'is_audio_clip'),
                  MFLProperty(b'is_midi_clip'),
                  MFLProperty(b'is_overdubbing'),
                  MFLProperty(b'is_playing'),
                  MFLProperty(b'is_recording'),
                  MFLProperty(b'is_triggered'),
                  MFLProperty(b'length'),
                  MFLProperty(b'loop_end'),
                  MFLProperty(b'loop_start'),
                  MFLProperty(b'looping'),
                  MFLProperty(b'muted'),
                  MFLProperty(b'name'),
                  MFLProperty(b'pitch_coarse'),
                  MFLProperty(b'pitch_fine'),
                  MFLProperty(b'playing_position'),
                  MFLProperty(b'position'),
                  MFLProperty(b'ram_mode'),
                  MFLProperty(b'signature_denominator'),
                  MFLProperty(b'signature_numerator'),
                  MFLProperty(b'start_marker'),
                  MFLProperty(b'start_time'),
                  MFLProperty(b'warp_mode'),
                  MFLProperty(b'warping'),
                  MFLProperty(b'will_record_on_start'),
                  MFLProperty(b'clear_all_envelopes'),
                  MFLProperty(b'clear_envelope'),
                  MFLProperty(b'deselect_all_notes'),
                  MFLProperty(b'duplicate_loop'),
                  MFLProperty(b'duplicate_region'),
                  MFLProperty(b'fire'),
                  MFLProperty(b'get_notes'),
                  MFLProperty(b'get_selected_notes'),
                  MFLProperty(b'move_playing_pos'),
                  MFLProperty(b'quantize'),
                  MFLProperty(b'quantize_pitch'),
                  MFLProperty(b'remove_notes'),
                  MFLProperty(b'replace_selected_notes'),
                  MFLProperty(b'scrub'),
                  MFLProperty(b'select_all_notes'),
                  MFLProperty(b'set_fire_button_state'),
                  MFLProperty(b'set_notes'),
                  MFLProperty(b'stop'),
                  MFLProperty(b'stop_scrub')), 
   Live.Clip.Clip.View: (
                       MFLProperty(b'canonical_parent'),
                       MFLProperty(b'grid_is_triplet'),
                       MFLProperty(b'grid_quantization'),
                       MFLProperty(b'hide_envelope'),
                       MFLProperty(b'select_envelope_parameter'),
                       MFLProperty(b'show_envelope'),
                       MFLProperty(b'show_loop')), 
   Live.ClipSlot.ClipSlot: (
                          MFLProperty(b'canonical_parent'),
                          MFLProperty(b'clip'),
                          MFLProperty(b'color'),
                          MFLProperty(b'color_index'),
                          MFLProperty(b'controls_other_clips'),
                          MFLProperty(b'has_clip'),
                          MFLProperty(b'has_stop_button'),
                          MFLProperty(b'is_group_slot'),
                          MFLProperty(b'is_playing'),
                          MFLProperty(b'is_recording'),
                          MFLProperty(b'is_triggered'),
                          MFLProperty(b'playing_status'),
                          MFLProperty(b'will_record_on_start'),
                          MFLProperty(b'create_clip'),
                          MFLProperty(b'delete_clip'),
                          MFLProperty(b'duplicate_clip_to'),
                          MFLProperty(b'fire'),
                          MFLProperty(b'set_fire_button_state'),
                          MFLProperty(b'stop')), 
   Live.CompressorDevice.CompressorDevice: tuple(_DEVICE_BASE_PROPS + [
                                          MFLProperty(b'available_input_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_input_channels_to_json, min_epii_version=(4,
                                                                                                                                                     3)),
                                          MFLProperty(b'available_input_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_input_types_to_json, min_epii_version=(4,
                                                                                                                                               3)),
                                          MFLProperty(b'input_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_input_channel_to_json, min_epii_version=(4,
                                                                                                                               3)),
                                          MFLProperty(b'input_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_input_channel_to_json, min_epii_version=(4,
                                                                                                                            3))]), 
   Live.Device.Device: tuple(_DEVICE_BASE_PROPS), 
   Live.Device.Device.View: tuple(_DEVICE_VIEW_BASE_PROPS), 
   Live.DeviceParameter.DeviceParameter: (
                                        MFLProperty(b'canonical_parent'),
                                        MFLProperty(b'automation_state'),
                                        MFLProperty(b'default_value'),
                                        MFLProperty(b'is_enabled'),
                                        MFLProperty(b'is_quantized'),
                                        MFLProperty(b'max'),
                                        MFLProperty(b'min'),
                                        MFLProperty(b'name'),
                                        MFLProperty(b'original_name'),
                                        MFLProperty(b'state'),
                                        MFLProperty(b'value'),
                                        MFLProperty(b'value_items'),
                                        MFLProperty(b're_enable_automation'),
                                        MFLProperty(b'str_for_value'),
                                        MFLProperty(b'__str__')), 
   Live.DeviceIO.DeviceIO: (
                          MFLProperty(b'available_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_channels_to_json, min_epii_version=(4,
                                                                                                                                         4)),
                          MFLProperty(b'available_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_types_to_json, min_epii_version=(4,
                                                                                                                                   4)),
                          MFLProperty(b'routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_channel_to_json, from_json=json_to_routing_channel, min_epii_version=(4,
                                                                                                                                                      4)),
                          MFLProperty(b'routing_type', format=MFLPropertyFormats.JSON, to_json=routing_type_to_json, from_json=json_to_routing_type, min_epii_version=(4,
                                                                                                                                             4)),
                          MFLProperty(b'default_external_routing_channel_is_none')), 
   Live.DrumChain.DrumChain: tuple(_CHAIN_BASE_PROPS + [MFLProperty(b'out_note'), MFLProperty(b'choke_group')]), 
   Live.DrumPad.DrumPad: (
                        MFLProperty(b'canonical_parent'),
                        MFLProperty(b'chains'),
                        MFLProperty(b'mute'),
                        MFLProperty(b'name'),
                        MFLProperty(b'note'),
                        MFLProperty(b'solo'),
                        MFLProperty(b'delete_all_chains')), 
   Live.Eq8Device.Eq8Device: tuple(_DEVICE_BASE_PROPS + [
                            MFLProperty(b'global_mode'),
                            MFLProperty(b'edit_mode'),
                            MFLProperty(b'oversample')]), 
   Live.Eq8Device.Eq8Device.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty(b'selected_band')]), 
   Live.MaxDevice.MaxDevice: tuple(_DEVICE_BASE_PROPS + [
                            MFLProperty(b'get_bank_count'),
                            MFLProperty(b'get_bank_name'),
                            MFLProperty(b'get_bank_parameters'),
                            MFLProperty(b'audio_outputs'),
                            MFLProperty(b'audio_inputs')]), 
   Live.MixerDevice.MixerDevice: (
                                MFLProperty(b'canonical_parent'),
                                MFLProperty(b'sends'),
                                MFLProperty(b'cue_volume'),
                                MFLProperty(b'crossfader'),
                                MFLProperty(b'left_split_stereo'),
                                MFLProperty(b'panning'),
                                MFLProperty(b'panning_mode'),
                                MFLProperty(b'right_split_stereo'),
                                MFLProperty(b'song_tempo'),
                                MFLProperty(b'track_activator'),
                                MFLProperty(b'volume'),
                                MFLProperty(b'crossfade_assign')), 
   Live.PluginDevice.PluginDevice: tuple(_DEVICE_BASE_PROPS + [
                                  MFLProperty(b'presets'), MFLProperty(b'selected_preset_index')]), 
   Live.RackDevice.RackDevice: tuple(_DEVICE_BASE_PROPS + [
                              MFLProperty(b'chains'),
                              MFLProperty(b'can_show_chains'),
                              MFLProperty(b'drum_pads'),
                              MFLProperty(b'is_showing_chains'),
                              MFLProperty(b'return_chains'),
                              MFLProperty(b'visible_drum_pads'),
                              MFLProperty(b'has_macro_mappings'),
                              MFLProperty(b'has_drum_pads'),
                              MFLProperty(b'copy_pad')]), 
   Live.RackDevice.RackDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [
                                   MFLProperty(b'selected_chain'),
                                   MFLProperty(b'selected_drum_pad'),
                                   MFLProperty(b'drum_pads_scroll_position'),
                                   MFLProperty(b'is_showing_chain_devices')]), 
   Live.Sample.Sample: (
                      MFLProperty(b'canonical_parent'),
                      MFLProperty(b'beats_granulation_resolution'),
                      MFLProperty(b'beats_transient_envelope'),
                      MFLProperty(b'beats_transient_loop_mode'),
                      MFLProperty(b'complex_pro_envelope'),
                      MFLProperty(b'complex_pro_formants'),
                      MFLProperty(b'end_marker'),
                      MFLProperty(b'file_path'),
                      MFLProperty(b'gain'),
                      MFLProperty(b'length'),
                      MFLProperty(b'slicing_sensitivity'),
                      MFLProperty(b'start_marker'),
                      MFLProperty(b'texture_flux'),
                      MFLProperty(b'texture_grain_size'),
                      MFLProperty(b'tones_grain_size'),
                      MFLProperty(b'warp_mode'),
                      MFLProperty(b'warping'),
                      MFLProperty(b'slicing_style'),
                      MFLProperty(b'slicing_beat_division'),
                      MFLProperty(b'slicing_region_count'),
                      MFLProperty(b'gain_display_string'),
                      MFLProperty(b'insert_slice'),
                      MFLProperty(b'move_slice'),
                      MFLProperty(b'remove_slice'),
                      MFLProperty(b'clear_slices'),
                      MFLProperty(b'reset_slices')), 
   Live.Scene.Scene: (
                    MFLProperty(b'canonical_parent'),
                    MFLProperty(b'clip_slots'),
                    MFLProperty(b'color'),
                    MFLProperty(b'color_index'),
                    MFLProperty(b'is_empty'),
                    MFLProperty(b'is_triggered'),
                    MFLProperty(b'name'),
                    MFLProperty(b'tempo'),
                    MFLProperty(b'fire'),
                    MFLProperty(b'fire_as_selected'),
                    MFLProperty(b'set_fire_button_state')), 
   Live.SimplerDevice.SimplerDevice: tuple(_DEVICE_BASE_PROPS + [
                                    MFLProperty(b'sample'),
                                    MFLProperty(b'can_warp_as'),
                                    MFLProperty(b'can_warp_double'),
                                    MFLProperty(b'can_warp_half'),
                                    MFLProperty(b'multi_sample_mode'),
                                    MFLProperty(b'pad_slicing'),
                                    MFLProperty(b'playback_mode'),
                                    MFLProperty(b'playing_position'),
                                    MFLProperty(b'playing_position_enabled'),
                                    MFLProperty(b'retrigger'),
                                    MFLProperty(b'slicing_playback_mode'),
                                    MFLProperty(b'voices'),
                                    MFLProperty(b'crop'),
                                    MFLProperty(b'guess_playback_length'),
                                    MFLProperty(b'reverse'),
                                    MFLProperty(b'warp_as'),
                                    MFLProperty(b'warp_double'),
                                    MFLProperty(b'warp_half')]), 
   Live.SimplerDevice.SimplerDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty(b'selected_slice')]), 
   Live.Song.Song: (
                  MFLProperty(b'cue_points'),
                  MFLProperty(b'return_tracks'),
                  MFLProperty(b'scenes'),
                  MFLProperty(b'tracks'),
                  MFLProperty(b'visible_tracks'),
                  MFLProperty(b'master_track'),
                  MFLProperty(b'view'),
                  MFLProperty(b'appointed_device'),
                  MFLProperty(b'arrangement_overdub'),
                  MFLProperty(b'back_to_arranger'),
                  MFLProperty(b'can_jump_to_next_cue'),
                  MFLProperty(b'can_jump_to_prev_cue'),
                  MFLProperty(b'can_redo'),
                  MFLProperty(b'can_undo'),
                  MFLProperty(b'clip_trigger_quantization'),
                  MFLProperty(b'count_in_duration'),
                  MFLProperty(b'current_song_time'),
                  MFLProperty(b'exclusive_arm'),
                  MFLProperty(b'exclusive_solo'),
                  MFLProperty(b'groove_amount'),
                  MFLProperty(b'is_counting_in'),
                  MFLProperty(b'is_playing'),
                  MFLProperty(b'last_event_time'),
                  MFLProperty(b'loop'),
                  MFLProperty(b'loop_length'),
                  MFLProperty(b'loop_start'),
                  MFLProperty(b'metronome'),
                  MFLProperty(b'midi_recording_quantization'),
                  MFLProperty(b'nudge_down'),
                  MFLProperty(b'nudge_up'),
                  MFLProperty(b'overdub'),
                  MFLProperty(b'punch_in'),
                  MFLProperty(b'punch_out'),
                  MFLProperty(b're_enable_automation_enabled'),
                  MFLProperty(b'record_mode'),
                  MFLProperty(b'root_note'),
                  MFLProperty(b'scale_name'),
                  MFLProperty(b'scale_intervals'),
                  MFLProperty(b'select_on_launch'),
                  MFLProperty(b'session_automation_record'),
                  MFLProperty(b'session_record'),
                  MFLProperty(b'session_record_status'),
                  MFLProperty(b'signature_denominator'),
                  MFLProperty(b'signature_numerator'),
                  MFLProperty(b'song_length'),
                  MFLProperty(b'swing_amount'),
                  MFLProperty(b'tempo'),
                  MFLProperty(b'capture_and_insert_scene'),
                  MFLProperty(b'capture_midi'),
                  MFLProperty(b'can_capture_midi'),
                  MFLProperty(b'continue_playing'),
                  MFLProperty(b'create_audio_track'),
                  MFLProperty(b'create_midi_track'),
                  MFLProperty(b'create_return_track'),
                  MFLProperty(b'create_scene'),
                  MFLProperty(b'delete_scene'),
                  MFLProperty(b'delete_track'),
                  MFLProperty(b'delete_return_track'),
                  MFLProperty(b'duplicate_scene'),
                  MFLProperty(b'duplicate_track'),
                  MFLProperty(b'find_device_position'),
                  MFLProperty(b'force_link_beat_time'),
                  MFLProperty(b'get_beats_loop_length'),
                  MFLProperty(b'get_beats_loop_start'),
                  MFLProperty(b'get_current_beats_song_time'),
                  MFLProperty(b'get_current_smpte_song_time'),
                  MFLProperty(b'is_cue_point_selected'),
                  MFLProperty(b'jump_by'),
                  MFLProperty(b'jump_to_next_cue'),
                  MFLProperty(b'jump_to_prev_cue'),
                  MFLProperty(b'move_device'),
                  MFLProperty(b'play_selection'),
                  MFLProperty(b're_enable_automation'),
                  MFLProperty(b'redo'),
                  MFLProperty(b'scrub_by'),
                  MFLProperty(b'set_or_delete_cue'),
                  MFLProperty(b'start_playing'),
                  MFLProperty(b'stop_all_clips'),
                  MFLProperty(b'stop_playing'),
                  MFLProperty(b'tap_tempo'),
                  MFLProperty(b'trigger_session_record'),
                  MFLProperty(b'undo')), 
   Live.Song.Song.View: (
                       MFLProperty(b'canonical_parent'),
                       MFLProperty(b'detail_clip'),
                       MFLProperty(b'highlighted_clip_slot'),
                       MFLProperty(b'selected_chain'),
                       MFLProperty(b'selected_parameter'),
                       MFLProperty(b'selected_scene'),
                       MFLProperty(b'selected_track'),
                       MFLProperty(b'draw_mode'),
                       MFLProperty(b'follow_song'),
                       MFLProperty(b'select_device')), 
   Live.Song.CuePoint: (
                      MFLProperty(b'canonical_parent'),
                      MFLProperty(b'name'),
                      MFLProperty(b'time'),
                      MFLProperty(b'jump')), 
   Live.Track.Track: (
                    MFLProperty(b'clip_slots'),
                    MFLProperty(b'devices'),
                    MFLProperty(b'canonical_parent'),
                    MFLProperty(b'mixer_device'),
                    MFLProperty(b'view'),
                    MFLProperty(b'arm'),
                    MFLProperty(b'available_input_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_input_channels_to_json, min_epii_version=(4,
                                                                                                                                                     3)),
                    MFLProperty(b'available_input_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_input_types_to_json, min_epii_version=(4,
                                                                                                                                               3)),
                    MFLProperty(b'available_output_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_output_channels_to_json, min_epii_version=(4,
                                                                                                                                                       3)),
                    MFLProperty(b'available_output_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_output_types_to_json, min_epii_version=(4,
                                                                                                                                                 3)),
                    MFLProperty(b'can_be_armed'),
                    MFLProperty(b'can_be_frozen'),
                    MFLProperty(b'can_show_chains'),
                    MFLProperty(b'color'),
                    MFLProperty(b'color_index'),
                    MFLProperty(b'current_input_routing'),
                    MFLProperty(b'current_input_sub_routing'),
                    MFLProperty(b'current_monitoring_state'),
                    MFLProperty(b'current_output_routing'),
                    MFLProperty(b'current_output_sub_routing'),
                    MFLProperty(b'fired_slot_index'),
                    MFLProperty(b'fold_state'),
                    MFLProperty(b'group_track'),
                    MFLProperty(b'has_audio_input'),
                    MFLProperty(b'has_audio_output'),
                    MFLProperty(b'has_midi_input'),
                    MFLProperty(b'has_midi_output'),
                    MFLProperty(b'implicit_arm'),
                    MFLProperty(b'input_meter_left'),
                    MFLProperty(b'input_meter_level'),
                    MFLProperty(b'input_meter_right'),
                    MFLProperty(b'input_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_input_channel_to_json, from_json=json_to_input_routing_channel, min_epii_version=(4,
                                                                                                                                                                        3)),
                    MFLProperty(b'input_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_input_type_to_json, from_json=json_to_input_routing_type, min_epii_version=(4,
                                                                                                                                                               3)),
                    MFLProperty(b'input_routings'),
                    MFLProperty(b'input_sub_routings'),
                    MFLProperty(b'is_foldable'),
                    MFLProperty(b'is_frozen'),
                    MFLProperty(b'is_grouped'),
                    MFLProperty(b'is_part_of_selection'),
                    MFLProperty(b'is_showing_chains'),
                    MFLProperty(b'is_visible'),
                    MFLProperty(b'mute'),
                    MFLProperty(b'muted_via_solo'),
                    MFLProperty(b'name'),
                    MFLProperty(b'output_meter_left'),
                    MFLProperty(b'output_meter_level'),
                    MFLProperty(b'output_meter_right'),
                    MFLProperty(b'output_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_output_channel_to_json, from_json=json_to_output_routing_channel, min_epii_version=(4,
                                                                                                                                                                           3)),
                    MFLProperty(b'output_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_output_type_to_json, from_json=json_to_output_routing_type, min_epii_version=(4,
                                                                                                                                                                  3)),
                    MFLProperty(b'output_routings'),
                    MFLProperty(b'output_sub_routings'),
                    MFLProperty(b'playing_slot_index'),
                    MFLProperty(b'solo'),
                    MFLProperty(b'delete_clip'),
                    MFLProperty(b'delete_device'),
                    MFLProperty(b'duplicate_clip_slot'),
                    MFLProperty(b'duplicate_clip_to_arrangement'),
                    MFLProperty(b'jump_in_running_session_clip'),
                    MFLProperty(b'stop_all_clips')), 
   Live.Track.Track.View: (
                         MFLProperty(b'canonical_parent'),
                         MFLProperty(b'selected_device'),
                         MFLProperty(b'device_insert_mode'),
                         MFLProperty(b'is_collapsed'),
                         MFLProperty(b'select_instrument')), 
   Live.WavetableDevice.WavetableDevice: tuple(_DEVICE_BASE_PROPS + [
                                        MFLProperty(b'add_parameter_to_modulation_matrix'),
                                        MFLProperty(b'filter_routing'),
                                        MFLProperty(b'get_modulation_target_parameter_name'),
                                        MFLProperty(b'get_modulation_value'),
                                        MFLProperty(b'is_parameter_modulatable'),
                                        MFLProperty(b'mono_poly'),
                                        MFLProperty(b'oscillator_1_effect_mode'),
                                        MFLProperty(b'oscillator_2_effect_mode'),
                                        MFLProperty(b'oscillator_1_wavetable_category'),
                                        MFLProperty(b'oscillator_2_wavetable_category'),
                                        MFLProperty(b'oscillator_1_wavetable_index'),
                                        MFLProperty(b'oscillator_2_wavetable_index'),
                                        MFLProperty(b'oscillator_1_wavetables'),
                                        MFLProperty(b'oscillator_2_wavetables'),
                                        MFLProperty(b'oscillator_wavetable_categories'),
                                        MFLProperty(b'poly_voices'),
                                        MFLProperty(b'set_modulation_value'),
                                        MFLProperty(b'unison_mode'),
                                        MFLProperty(b'unison_voice_count'),
                                        MFLProperty(b'visible_modulation_target_names')])}
HIDDEN_TYPE_PROPERTIES = {Live.Sample.Sample: ('slices', )}
EXTRA_CS_FUNCTIONS = ('get_control_names', 'get_control', 'grab_control', 'release_control',
                      'send_midi', 'send_receive_sysex', 'grab_midi', 'release_midi')
ENUM_TYPES = (
 Live.Song.Quantization,
 Live.Song.RecordingQuantization,
 Live.Song.CaptureMode,
 Live.Clip.GridQuantization,
 Live.DeviceParameter.AutomationState,
 Live.Sample.SlicingStyle,
 Live.Sample.SlicingBeatDivision)
TUPLE_TYPES = {b'tracks': Live.Track.Track, 
   b'visible_tracks': Live.Track.Track, 
   b'return_tracks': Live.Track.Track, 
   b'clip_slots': Live.ClipSlot.ClipSlot, 
   b'scenes': Live.Scene.Scene, 
   b'parameters': Live.DeviceParameter.DeviceParameter, 
   b'sends': Live.DeviceParameter.DeviceParameter, 
   b'devices': Live.Device.Device, 
   b'cue_points': Live.Song.CuePoint, 
   b'chains': Live.Chain.Chain, 
   b'return_chains': Live.Chain.Chain, 
   b'drum_pads': Live.DrumPad.DrumPad, 
   b'visible_drum_pads': Live.DrumPad.DrumPad, 
   b'control_surfaces': ControlSurface, 
   b'components': ControlSurfaceComponent, 
   b'controls': ControlElement, 
   b'audio_outputs': Live.DeviceIO.DeviceIO, 
   b'audio_inputs': Live.DeviceIO.DeviceIO}
PROPERTY_TYPES = {b'master_track': Live.Track.Track, 
   b'selected_track': Live.Track.Track, 
   b'selected_scene': Live.Scene.Scene, 
   b'volume': Live.DeviceParameter.DeviceParameter, 
   b'panning': Live.DeviceParameter.DeviceParameter, 
   b'crossfader': Live.DeviceParameter.DeviceParameter, 
   b'song_tempo': Live.DeviceParameter.DeviceParameter, 
   b'cue_volume': Live.DeviceParameter.DeviceParameter, 
   b'track_activator': Live.DeviceParameter.DeviceParameter, 
   b'chain_activator': Live.DeviceParameter.DeviceParameter, 
   b'clip': Live.Clip.Clip, 
   b'detail_clip': Live.Clip.Clip, 
   b'highlighted_clip_slot': Live.ClipSlot.ClipSlot, 
   b'selected_device': Live.Device.Device, 
   b'selected_parameter': Live.DeviceParameter.DeviceParameter, 
   b'selected_chain': Live.Chain.Chain, 
   b'selected_drum_pad': Live.DrumPad.DrumPad, 
   b'sample': Live.Sample.Sample, 
   b'mixer_device': (
                   Live.MixerDevice.MixerDevice,
                   Live.ChainMixerDevice.ChainMixerDevice), 
   b'view': (
           Live.Application.Application.View,
           Live.Song.Song.View,
           Live.Track.Track.View,
           Live.Device.Device.View,
           Live.RackDevice.RackDevice.View,
           Live.Clip.Clip.View), 
   b'left_split_stereo': Live.DeviceParameter.DeviceParameter, 
   b'right_split_stereo': Live.DeviceParameter.DeviceParameter, 
   b'group_track': Live.Track.Track}
LIVE_APP = b'live_app'
LIVE_SET = b'live_set'
CONTROL_SURFACES = b'control_surfaces'
THIS_DEVICE = b'this_device'
ROOT_KEYS = (
 THIS_DEVICE, CONTROL_SURFACES, LIVE_APP, LIVE_SET)

class LomAttributeError(AttributeError):
    pass


class LomObjectError(AttributeError):
    pass


class LomNoteOperationWarning(Exception):
    pass


class LomNoteOperationError(AttributeError):
    pass


def get_exposed_lom_types():
    return EXPOSED_TYPE_PROPERTIES.keys()


def get_exposed_properties_for_type(lom_type, epii_version):
    return [ prop for prop in EXPOSED_TYPE_PROPERTIES.get(lom_type, []) if epii_version >= prop.min_epii_version
           ]


def get_exposed_property_names_for_type(lom_type, epii_version):
    return [ prop.name for prop in get_exposed_properties_for_type(lom_type, epii_version) ]


def is_property_exposed_for_type(property_name, lom_type, epii_version):
    return property_name in get_exposed_property_names_for_type(lom_type, epii_version)


def get_exposed_property_info(lom_type, property_name, epii_version):
    properties = get_exposed_properties_for_type(lom_type, epii_version)
    prop = filter(lambda p: p.name == property_name, properties)
    if not prop:
        return None
    else:
        return prop[0]


def is_class(class_object):
    return isinstance(class_object, types.ClassType) or hasattr(class_object, b'__bases__')


def get_control_surfaces():
    result = []
    cs_list_key = b'control_surfaces'
    if isinstance(__builtins__, dict):
        if cs_list_key in __builtins__.keys():
            result = __builtins__[cs_list_key]
    elif hasattr(__builtins__, cs_list_key):
        result = getattr(__builtins__, cs_list_key)
    return tuple(result)


def get_root_prop(external_device, prop_key):
    root_properties = {LIVE_APP: Live.Application.get_application, 
       LIVE_SET: lambda : Live.Application.get_application().get_document(), 
       CONTROL_SURFACES: get_control_surfaces}
    assert prop_key in ROOT_KEYS
    if prop_key == THIS_DEVICE:
        return external_device
    return root_properties[prop_key]()


def cs_base_classes():
    from _Framework.ControlSurface import ControlSurface
    from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
    from _Framework.ControlElement import ControlElement
    from ableton.v2.control_surface import ControlElement as ControlElement2
    from ableton.v2.control_surface import ControlSurface as ControlSurface2
    from ableton.v2.control_surface import Component as ControlSurfaceComponent2
    return (
     ControlSurface,
     ControlSurfaceComponent,
     ControlElement,
     ControlSurface2,
     ControlSurfaceComponent2,
     ControlElement2)


def is_control_surface(lom_object):
    from _Framework.ControlSurface import ControlSurface
    from ableton.v2.control_surface import ControlSurface as ControlSurface2
    return isinstance(lom_object, (ControlSurface, ControlSurface2))


def is_lom_object(lom_object, lom_classes):
    return isinstance(lom_object, tuple(lom_classes) + (type(None),)) or isinstance(lom_object, cs_base_classes()) or isinstance(lom_object, Live.Base.Vector)


def is_cplusplus_lom_object(lom_object):
    return isinstance(lom_object, Live.LomObject.LomObject)


def is_object_iterable(obj):
    return not isinstance(obj, basestring) and is_iterable(obj) and not isinstance(obj, cs_base_classes())


def is_property_hidden(lom_object, property_name):
    return property_name in HIDDEN_TYPE_PROPERTIES.get(type(lom_object), [])


def verify_object_property(lom_object, property_name, epii_version):
    raise_error = False
    if isinstance(lom_object, cs_base_classes()):
        if not hasattr(lom_object, property_name):
            raise_error = True
    elif not is_property_exposed_for_type(property_name, type(lom_object), epii_version):
        raise_error = True
    if raise_error:
        raise LomAttributeError(b"'%s' object has no attribute '%s'" % (
         lom_object.__class__.__name__, property_name))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_MxDCore/LomTypes.pyc
