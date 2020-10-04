# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\AssignableButtonsConsts.py
# Compiled at: 2017-03-07 13:28:52
from AssignableButtonControl import ButtonFunctionControl, ButtonPropertyControl, ButtonViewToggleControl
from consts import GLOBAL_QUANTIZE_NAMES, RECORD_QUANTIZE_NAMES
from Utils import floats_equal

def _create_bfc_assignment(parent=None, b_type=None, fnc_name=None, flt_type=None):
    """ Creates/returns a ButtonFunctionControl assignment. """
    if b_type is None:
        b_type = ButtonFunctionControl
    return {'type': b_type, 'parent': parent, 'function_name': fnc_name, 'floating_type': flt_type}


def _create_bpc_assignment(parent=None, fnc_name=None, flt_type=None, prop_name=None, f_value=None, is_mty=False, o_transform=None):
    """ Creates/returns a ButtonPropertyControl assignment. """
    bfc = _create_bfc_assignment(parent, ButtonPropertyControl, fnc_name, flt_type)
    bfc['property_name'] = prop_name
    bfc['fixed_value'] = f_value
    bfc['is_momentary'] = is_mty
    bfc['output_transform'] = o_transform
    return bfc


def _create_bvtc_assignment(parent=None, fnc_name=None, flt_type=None, v_name=None, sv_name=None):
    """ Creates/returns a ButtonViewToggleControl assignment. """
    bfc = _create_bfc_assignment(parent, ButtonViewToggleControl, fnc_name, flt_type)
    bfc['view_name'] = v_name
    bfc['second_view_name'] = sv_name
    return bfc


def _create_global_assignment(button_name):
    """ Creates/returns a GlobalButtonsComponent assignment. """
    return {'parent': None, 'type': 'global', 'button': button_name}


def _crossfade_output_transform(value, f_value):
    """ Transforms the output to buttons assigned to the crossfader so that LEDs work
    similar to how a button slider would work. """
    if f_value > 0:
        if value >= f_value or floats_equal(value, f_value, abs_tol=0.1):
            return 1
        return 0
    if f_value < 0:
        if value <= f_value or floats_equal(value, f_value, abs_tol=0.1):
            return 1
        return 0
    if value == 0.0:
        return 1
    return 0


ASSIGNABLES = {'PLAY TGL': _create_bpc_assignment('song', prop_name='is_playing'), 'PLAY': _create_bpc_assignment('song', prop_name='is_playing', f_value=True), 
   'CONTINUE': _create_bpc_assignment('song', prop_name='is_playing', fnc_name='continue_playing'), 
   'STOP': _create_bpc_assignment('song', prop_name='is_playing', f_value=False), 
   'SSN REC': _create_bpc_assignment('song', prop_name='session_record'), 
   'ATM': _create_bpc_assignment('song', prop_name='session_automation_record'), 
   'RE-ENABLE ATM': _create_bpc_assignment('song', fnc_name='re_enable_automation', prop_name='re_enable_automation_enabled'), 
   'REC': _create_bpc_assignment('song', prop_name='record_mode'), 
   'PUNCH IN': _create_bpc_assignment('song', prop_name='punch_in'), 
   'PUNCH OUT': _create_bpc_assignment('song', prop_name='punch_out'), 
   'OVER': _create_bpc_assignment('song', prop_name='arrangement_overdub'), 
   'METRO': _create_bpc_assignment('song', prop_name='metronome'), 
   'LOOP': _create_bpc_assignment('song', prop_name='loop'), 
   'B2A': _create_bpc_assignment('song', prop_name='back_to_arranger'), 
   'NUDGE >': _create_bpc_assignment('song', prop_name='nudge_up', is_mty=True), 
   'NUDGE <': _create_bpc_assignment('song', prop_name='nudge_down', is_mty=True), 
   'CUE >': _create_bpc_assignment('song', fnc_name='jump_to_next_cue', prop_name='can_jump_to_next_cue'), 
   'CUE <': _create_bpc_assignment('song', fnc_name='jump_to_prev_cue', prop_name='can_jump_to_prev_cue'), 
   'FOLLOW': _create_bpc_assignment('song_view', prop_name='follow_song'), 
   'SET CUE': _create_bfc_assignment('song', fnc_name='set_or_delete_cue'), 
   'STOP ALL': _create_bfc_assignment('song', fnc_name='stop_all_clips'), 
   'TAP': _create_bfc_assignment('song', fnc_name='tap_tempo'), 
   'UNDO': _create_bfc_assignment('song', fnc_name='undo'), 
   'REDO': _create_bfc_assignment('song', fnc_name='redo'), 
   'DETAIL VIEW': _create_bvtc_assignment('app_view', v_name='Detail'), 
   'SSN/ARR': _create_bvtc_assignment('app_view', v_name='Arranger'), 
   'DEV/CLIP': _create_bvtc_assignment('app_view', v_name='Detail/Clip', sv_name='Detail/DeviceChain'), 
   'CLIP LOOP': _create_bpc_assignment(prop_name='looping', flt_type='any_clip'), 
   'CLIP MUTE': _create_bpc_assignment(prop_name='muted', flt_type='any_clip'), 
   'CLIP WARP': _create_bpc_assignment(prop_name='warping', flt_type='audio_clip'), 
   'CLIP RAM': _create_bpc_assignment(prop_name='ram_mode', flt_type='audio_clip'), 
   'CLIP PLAY TGL': _create_bpc_assignment(prop_name='clip_playing_status', fnc_name='_play_clip', flt_type='self_clip'), 
   'CLIP PLAY': _create_bpc_assignment(prop_name='clip_playing_status', fnc_name='_fire_clip', flt_type='self_clip'), 
   'CLIP CLR ENV': _create_bpc_assignment(prop_name='has_envelopes', fnc_name='clear_all_envelopes', flt_type='any_clip'), 
   'CLIP DOUBLE': _create_bfc_assignment(fnc_name='double_clip', flt_type='midi_clip'), 
   'CLIP DEL': _create_bpc_assignment(prop_name='has_clip', fnc_name='delete_clip', flt_type='slot'), 
   'CLIP DUPE': _create_bpc_assignment(prop_name='has_clip', fnc_name='duplicate_clip', flt_type='slot'), 
   'SCENE PLAY': _create_bpc_assignment(prop_name='is_triggered', fnc_name='fire', flt_type='scene'), 
   'SCENE PLAY SPC': _create_bpc_assignment(prop_name='is_triggered', fnc_name='fire_as_selected', flt_type='scene'), 
   'TRACK ARM': _create_bpc_assignment(prop_name='arm', flt_type='armable_track'), 
   'TRACK MUTE': _create_bpc_assignment(prop_name='mute', flt_type='not_master_track'), 
   'TRACK SOLO': _create_bpc_assignment(prop_name='solo', flt_type='not_master_track'), 
   'TRACK MON IN': _create_bpc_assignment(prop_name='current_monitoring_state', f_value=0, flt_type='armable_track'), 
   'TRACK MON AUTO': _create_bpc_assignment(prop_name='current_monitoring_state', f_value=1, flt_type='armable_track'), 
   'TRACK MON OFF': _create_bpc_assignment(prop_name='current_monitoring_state', f_value=2, flt_type='armable_track'), 
   'TRACK XFADE A': _create_bpc_assignment(prop_name='crossfade_assign', f_value=0, flt_type='not_master_track_mixer'), 
   'TRACK XFADE OFF': _create_bpc_assignment(prop_name='crossfade_assign', f_value=1, flt_type='not_master_track_mixer'), 
   'TRACK XFADE B': _create_bpc_assignment(prop_name='crossfade_assign', f_value=2, flt_type='not_master_track_mixer'), 
   'TRACK STOP': _create_bpc_assignment(prop_name='track_playing_status', fnc_name='_stop_track', flt_type='self_track'), 
   'TRACK PLAY TGL': _create_bpc_assignment(prop_name='track_playing_status', fnc_name='_play_track', flt_type='self_track'), 
   'TRACK PLAY': _create_bpc_assignment(prop_name='track_playing_status', fnc_name='_fire_track', flt_type='self_track'), 
   'TRACK PLAY SPC': _create_bpc_assignment(prop_name='track_playing_status', fnc_name='_fire_track_as_selected', flt_type='self_track'), 
   'SCROLL >': _create_global_assignment('increase_button'), 
   'SCROLL <': _create_global_assignment('decrease_button'), 
   'GLOBAL Q': _create_global_assignment('global_quantize_button'), 
   'REC Q': _create_global_assignment('record_quantize_button'), 
   'FIXED LEN': _create_global_assignment('fixed_length_button')}
for index, name in enumerate(GLOBAL_QUANTIZE_NAMES):
    ASSIGNABLES['GLOBAL Q %s' % name.upper()] = _create_bpc_assignment('song', prop_name='clip_trigger_quantization', f_value=index)

_rq = list(RECORD_QUANTIZE_NAMES)
_rq.insert(0, 'NONE')
for index, name in enumerate(_rq):
    ASSIGNABLES['REC Q %s' % name.upper()] = _create_bpc_assignment('song', prop_name='midi_recording_quantization', f_value=index)

for index in xrange(-10, 11, 2):
    val = index / 10.0
    d_val = index * 5
    d_name = 'C'
    if d_val != 0:
        d_name = '%sA' % abs(d_val) if d_val < 0 else '%sB' % d_val
    ASSIGNABLES['XFADER %s' % d_name] = _create_bpc_assignment('crossfader', prop_name='value', f_value=val, o_transform=_crossfade_output_transform)

def create_assignment(parent, assign, off_color, on_color):
    """ Creates an AssignableButtonControl based on the given arguments. """
    if assign['type'] == ButtonFunctionControl:
        return ButtonFunctionControl(parent, off_color, on_color, function_name=assign['function_name'], floating_type=assign['floating_type'])
    else:
        if assign['type'] == ButtonPropertyControl:
            return ButtonPropertyControl(parent, off_color, on_color, function_name=assign['function_name'], floating_type=assign['floating_type'], property_name=assign['property_name'], fixed_value=assign['fixed_value'], is_momentary=assign['is_momentary'], output_transform=assign['output_transform'])
        if assign['type'] == ButtonViewToggleControl:
            return ButtonViewToggleControl(parent, off_color, on_color, function_name=assign['function_name'], floating_type=assign['floating_type'], view_name=assign['view_name'], second_view_name=assign['second_view_name'])
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/AssignableButtonsConsts.pyc
