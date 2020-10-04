# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialButtonSliderStrategies.py
# Compiled at: 2017-03-07 13:28:53
import Live
from ControlUtils import get_group_buttons_pressed, reset_parameter, can_reset_or_toggle_parameter
from ClipUtils import get_playing_clip, clear_parameter_envelope, can_clear_parameter_envelope
from Utils import floats_equal

def slider_button_value(slider, param, button_id):
    buttons_len = len(slider._buttons)
    param_range = float(param.max - param.min)
    return param_range / (buttons_len - 1) * button_id + param.min


def bipolar_button_value(slider, param, button_id):
    """ Returns the bipolar value (based on distance from center point) to use and
    also checks whether the two buttons (or single button) in the center of the
    slider are pressed, which will center the value. """
    buttons_len = len(slider._buttons)
    half_len = buttons_len / 2
    pressed = get_group_buttons_pressed(slider._buttons)
    if buttons_len % 2 == 0:
        if len(pressed) == 2 and pressed[0] == half_len - 1 and pressed[1] == half_len:
            return 0.0
    elif len(pressed) == 1 and pressed[0] == half_len:
        return 0.0
    param_value = param.max / half_len * (button_id % half_len) + param.min
    if button_id >= half_len:
        if half_len == 4:
            param_value = -(param.max / half_len * ((button_id ^ half_len - 1) % half_len) + param.min)
        else:
            param_value = -param_value
    return param_value


def inc_dec_button_value(slider, param, button_id):
    """ Returns the incremented/decremented value or, if fine tuning, handles
    resetting/toggling parameter values or clearing envelopes and returning None. """
    buttons_len = len(slider._buttons)
    if button_id == buttons_len / 2:
        return param.value + slider._inc_dec_factor
    else:
        if button_id == buttons_len / 2 - 1:
            return param.value + -slider._inc_dec_factor
        if slider._is_fine_tuning and button_id == buttons_len - 1:
            reset_parameter(param)
        elif slider._is_fine_tuning and button_id == 0:
            clip = get_playing_clip(slider.canonical_parent.song())
            if clip:
                if isinstance(param, Live.DeviceParameter.DeviceParameter):
                    clear_parameter_envelope(clip, param)
                else:
                    param.clear_parameter_envelope(clip)
            slider._buttons[button_id].set_light(slider._automat_clear_colors[0])
        return


def on_off_button_value(slider, param, button_id):
    if button_id == len(slider._buttons) - 1:
        return float(not param.value)
    else:
        return


def slider_offsets(param, param_value, midi_value, buttons_len):
    if midi_value:
        return (0, param_value)
    return (-1, -1)


def bipolar_offsets(param, param_value, midi_value, buttons_len):
    half_len = buttons_len / 2
    if buttons_len == 8:
        if param.value == 0.0:
            return (half_len - 1, half_len)
        if param.value > 0.0:
            return (half_len, max(param_value - 1, half_len))
        if param.value < 0.0:
            return (min(param_value, half_len - 1), half_len - 1)
    if param.value == 0.0:
        return (half_len, half_len)
    if param.value > 0.0:
        return (half_len + 1, max(param_value, half_len + 1))
    if param.value < 0.0:
        return (min(param_value, half_len - 1), half_len - 1)


def inc_dec_offsets(param, param_value, midi_value, buttons_len):
    return (
     buttons_len / 2 - 1, buttons_len / 2)


def on_off_offsets(param, param_value, midi_value, buttons_len):
    return (
     buttons_len - 1, buttons_len - 1)


def slider_send_value(slider, param, index, offsets, buttons_len):
    if index in range(offsets[0], offsets[1] + 1):
        return slider._slider_color
    else:
        return


def bipolar_send_value(slider, param, index, offsets, buttons_len):
    if index in range(offsets[0], offsets[1] + 1):
        return slider._bipolar_color
    else:
        return


def inc_dec_send_value(slider, param, index, offsets, buttons_len):
    if index == offsets[0]:
        can_dec = not floats_equal(param.value, param.min)
        return slider._inc_dec_colors[int(can_dec)]
    if index == offsets[1]:
        can_inc = not floats_equal(param.value, param.max)
        return slider._inc_dec_colors[int(can_inc)]
    if slider._is_fine_tuning:
        if index == buttons_len - 1:
            can_reset = can_reset_or_toggle_parameter(param)
            return slider._off_on_colors[can_reset]
        if index == 0:
            can_clear = can_clear_parameter_envelope(param)
            return slider._automat_clear_colors[can_clear]


def on_off_send_value(slider, param, index, offsets, buttons_len):
    if index == buttons_len - 1:
        return slider._off_on_colors[int(param.value == param.max)]
    else:
        return


STRATEGIES = (
 {'button_value': slider_button_value, 'offsets': slider_offsets, 
    'send_value': slider_send_value},
 {'button_value': bipolar_button_value, 'offsets': bipolar_offsets, 
    'send_value': bipolar_send_value},
 {'button_value': inc_dec_button_value, 'offsets': inc_dec_offsets, 
    'send_value': inc_dec_send_value},
 {'button_value': on_off_button_value, 'offsets': on_off_offsets, 
    'send_value': on_off_send_value})
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialButtonSliderStrategies.pyc
