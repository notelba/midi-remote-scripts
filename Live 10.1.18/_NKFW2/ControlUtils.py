# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ControlUtils.py
# Compiled at: 2018-01-15 18:16:49
import Live
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ScrollComponent import ScrollComponent
from Utils import live_object_is_valid, parse_int, floats_equal
UNLISTED_QUANTIZED_PARAMETERS = {'MidiArpeggiator': ('Synced Rate', 'Ret. Interval', 'Repeats', 'Transp. Steps'), 
   'MidiNoteLength': ('Synced Length', ), 
   'MidiScale': ('Base', ), 
   'BeatRepeat': ('Interval', 'Offset', 'Grid', 'Variation', 'Gate', 'Pitch'), 
   'UltraAnalog': ('OSC1 Octave', 'OSC2 Octave'), 
   'StringStudio': ('Octave', ), 
   'GlueCompressor': ('Ratio', 'Attack', 'Release', 'Peak Clip In')}

def set_group_button_lights(buttons, skin_value):
    """ Sets all of the LED of all the given buttons to the given skin value. """
    assert buttons is None or isinstance(buttons, list) or isinstance(buttons, ButtonMatrixElement)
    assert isinstance(skin_value, str)
    if buttons:
        for button in buttons:
            if button:
                button.set_light(skin_value)

    return


def set_group_button_light(buttons, index, skin_value):
    """ Sets a button LED within a group (list) to the given skin value. This is only
    useful in cases where the index needs to be verified to be within the length of the
    group. """
    if not (buttons is None or isinstance(buttons, list)):
        raise AssertionError
        assert isinstance(index, int)
        assert isinstance(skin_value, str)
        if buttons and index in xrange(len(buttons)):
            button = buttons[index]
            if button:
                button.set_light(skin_value)
    return


def reset_button(button):
    """ Resets the given button back to its default MIDI message and enables it. """
    if button:
        button.use_default_message()
        button.set_light('DefaultButton.Off')
        button.set_enabled(True)


def reset_group_buttons(buttons):
    """ Reverts the given list or matrix of buttons back to their default MIDI messages
    and enables them. """
    assert buttons is None or isinstance(buttons, list) or isinstance(buttons, ButtonMatrixElement)
    if buttons:
        for button in buttons:
            if button:
                button.use_default_message()
                button.set_light('DefaultButton.Off')
                button.set_enabled(True)

    return


def assign_button_to_note(button, note, channel=None, color=None, force_next=True):
    """ Assigns the given button to the given note. Can optionally set the button's
    channel and LED color. """
    if force_next:
        button.force_next_send()
    button.set_identifier(note)
    if channel is not None:
        button.set_channel(channel)
    button.set_enabled(False)
    if color is not None:
        button.set_light(color)
    return


def get_group_buttons_pressed(buttons):
    """ Returns the lowest and highest indexes within the given group (list) that are
    currently pressed as a list. """
    assert buttons is None or isinstance(buttons, list)
    pressed = []
    if buttons:
        for index, button in enumerate(buttons):
            if button and button.is_pressed():
                if len(pressed) == 2:
                    pressed[1] = index
                else:
                    pressed.append(index)

    return pressed


def is_button_pressed(button):
    """ Returns whether the given button is present and is pressed. """
    return button is not None and button.is_pressed()


def get_smoothing_speed_for_velocity(velocity):
    """ Returns the smoothing speed to use with velocity-sensitive buttons. """
    if velocity:
        speed = 128 - velocity
        if speed >= 4:
            speed /= 4
        return speed


def translate_control_channels(controls, channel):
    """ Translates the channels of the given controls to the given channel. """
    assert controls is None or isinstance(controls, list) or isinstance(controls, ButtonMatrixElement)
    if controls:
        for control in controls:
            if control:
                control.set_channel(channel)

    return


def format_control_name(control):
    """ Returns a friendly name for the given control. """
    if control:
        if '_' in control.name:
            n_split = control.name.split('_')
            for i, n in enumerate(n_split):
                if n.isdigit():
                    n_split[i] = str(parse_int(n, 0) + 1)

            f_name = (' ').join(n_split)
            f_name = f_name.replace('Buttons', 'Button').replace('Encoders', 'Encoder').replace('Knobs', 'Knob').replace('Faders', 'Fader').replace('Sliders', 'Slider')
            return f_name
        return control.name
    return ''


def skin_scroll_component(component, color='Enabled', pressed_color='Navigation.Pressed', disabled_color='Navigation.Disabled'):
    """ Skins the buttons of the given scroll component with the given skin values, which
    can be a dict. """
    assert isinstance(component, ScrollComponent)
    component.scroll_up_button._color = color
    component.scroll_up_button._disabled_color = disabled_color
    component.scroll_up_button._pressed_color = pressed_color
    component.scroll_down_button._color = color
    component.scroll_down_button._disabled_color = disabled_color
    component.scroll_down_button._pressed_color = pressed_color
    component._update_scroll_buttons()


def kill_scroll_tasks(scroll_components):
    """ Kill all of the scroll tasks in the given list/tuple of ScrollComponents. """
    assert isinstance(scroll_components, (list, tuple))
    for sc in scroll_components:
        assert isinstance(sc, ScrollComponent)
        sc._scroll_task_up.kill()
        sc._scroll_task_down.kill()


def release_parameters(controls):
    """ Releases the parameters the given controls are attached to. """
    if controls is not None:
        for control in controls:
            if control is not None:
                control.release_parameter()
                control._parameter_to_map_to = None

    return


def can_reset_or_toggle_parameter(param):
    """ Returns whether or not the parameter value can be reset or toggled. """
    if param is not None:
        return param.is_enabled and (parameter_is_quantized(param) or not floats_equal(param.value, param.default_value))
    else:
        return False


def reset_parameter(param):
    """ Resets or toggles parameter value depending on whether or not it's quantized. """
    if param and param.is_enabled:
        if parameter_is_quantized(param):
            if param.value + 1 > param.max:
                param.value = param.min
            else:
                param.value = param.value + 1
        else:
            param.value = param.default_value


def get_parameter_value_to_set(param, value):
    """ Returns either the value that was passed or the parameter's min/max value if
    the passed value is out of range. """
    assert param is not None and isinstance(value, float)
    if value > param.max:
        value = param.max
    elif value < param.min:
        value = param.min
    return value


def parameter_value_to_midi_value(p_value, p_min, p_max):
    """ Returns a valid MIDI value for the given parameter value/range. """
    if p_min > p_max or p_value < p_min:
        return 0
    p_range = p_max - p_min
    return abs(min(127, int(float(p_value - p_min) / p_range * 128.0)))


def parameter_is_quantized(param):
    """ Returns whether or not the given parameter is quantized. This is needed
    for cases where parameters are quantized, but are not listed that way. """
    if live_object_is_valid(param):
        if param.is_quantized:
            return True
        parent = param.canonical_parent
        if isinstance(parent, Live.Device.Device):
            parent = parent.class_name
            return parent in UNLISTED_QUANTIZED_PARAMETERS and param.name in UNLISTED_QUANTIZED_PARAMETERS[parent]
    return False
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ControlUtils.pyc
