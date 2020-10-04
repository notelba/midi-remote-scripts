# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialButtonSliderElement.py
# Compiled at: 2017-09-30 15:26:23
import Live
from _Framework.InputControlElement import MIDI_INVALID_TYPE
from _Framework.SliderElement import SliderElement
from _Framework.SubjectSlot import SlotManager, subject_slot_group, subject_slot
from _Framework.Util import nop
from ParameterSmoother import ParameterSmoother
from ControlUtils import set_group_button_lights, parameter_is_quantized, get_smoothing_speed_for_velocity, parameter_value_to_midi_value
from SpecialButtonSliderStrategies import STRATEGIES
SLIDER = 0
BIPOLAR = 1
INC_DEC = 2
ON_OFF = 3

class SpecialButtonSliderElement(SliderElement, SlotManager):
    """ SpecialButtonSliderElement is a special type of ButtonSliderElement that sets
    up the buttons in different ways and uses different LED colors depending on the type
    of parameter being controlled. It also provides parameter smoothing as well as the
    ability to fine tune (inc/dec), reset parameters and clear envelopes. """
    _last_sent_value = -1
    __subject_events__ = ('parameter_name', 'parameter_value')

    def __init__(self, should_invert_buttons=True, default_smoothing_speed=2, velocity_sensitive=False, slider_color='DefaultButton.On', bipolar_color='DefaultButton.On', inc_dec_colors=('DefaultButton.On', 'DefaultButton.On'), off_on_colors=('DefaultButton.Off', 'DefaultButton.On'), automat_clear_colors=('DefaultButton.Off', 'DefaultButton.On'), **k):
        self._parameter_to_map_to = None
        super(SpecialButtonSliderElement, self).__init__(MIDI_INVALID_TYPE, 0, 0, **k)
        self._smoother = ParameterSmoother(self._tasks, default_smoothing_speed, smoothing_complete_callback=self._on_smoothing_complete)
        self._should_invert_buttons = bool(should_invert_buttons)
        self._is_velocity_sensitive = bool(velocity_sensitive)
        self._needs_takeover = False
        self._is_fine_tuning = False
        self._mapping_type = SLIDER
        self._inc_dec_factor = 1
        self._last_received_value = -1
        self._strategy = STRATEGIES[SLIDER]
        self._buttons = None
        self._slider_color = slider_color
        self._bipolar_color = bipolar_color
        self._inc_dec_colors = inc_dec_colors
        self._off_on_colors = off_on_colors
        self._automat_clear_colors = automat_clear_colors
        self.install_connections = nop
        self._parameter_value_slot = self.register_slot(None, self._on_parameter_changed, 'value')
        return

    def disconnect(self):
        set_group_button_lights(self._buttons, 'DefaultButton.Off')
        super(SpecialButtonSliderElement, self).disconnect()
        self._smoother.disconnect()
        self._parameter_to_map_to = None
        self._parameter_value_slot = None
        self._buttons = None
        self._inc_dec_colors = None
        self._off_on_colors = None
        self._automat_clear_colors = None
        self._strategy = None
        return

    @property
    def parameter_name(self):
        """ (For use with M4L and displays): Returns the name of the parameter or property
        this slider is assigned to. """
        if self._parameter_to_map_to is not None:
            return self._parameter_to_map_to.name
        else:
            return ''

    @property
    def parameter_value(self):
        """ (For use with M4L and displays): Returns the unicode value of the parameter
        or property this slider is assigned to. """
        if self._parameter_to_map_to is not None:
            return unicode(self._parameter_to_map_to)
        else:
            return ''

    @subject_slot('name')
    def _on_parameter_name_changed(self):
        """ Notifies listeners of parameter_name upon changes. """
        self.notify_parameter_name(self.parameter_name)

    @subject_slot('value')
    def _on_property_value_changed(self):
        """ This is only used for property observing, parameters are already observed. """
        self.notify_parameter_value(self.parameter_value)

    def set_buttons(self, buttons):
        """ Sets the buttons to use in this button slider. """
        assert buttons is None or len(buttons) > 0
        self._smoother.stop_smoothing()
        self._last_sent_value = -1
        self._buttons = buttons or []
        if buttons and self._should_invert_buttons:
            self._buttons = list(self._buttons)[::-1]
        self._button_value.replace_subjects(self._buttons)
        self._update_mapping_type()
        return

    def get_button(self, index):
        """ Returns the button at the index in the slider or None if out of range or no
        buttons. """
        if self._buttons and index in xrange(len(self._buttons)):
            return self._buttons[index]
        else:
            return

    def height(self):
        """ Returns the height or number of buttons in the slider or 0 if no buttons. """
        if self._buttons:
            return len(self._buttons)
        return 0

    def enable_fine_tune_and_reset(self, enable):
        """ Enables/disables fine tuning. When enabled the mapping type will be set to
        inc/dec, the highest button in the slider will be set up as a reset/toggle button
        and the lowest button will be set up as a clear envelope button. """
        self._is_fine_tuning = bool(enable)
        self._update_mapping_type()

    def set_slider_color(self, color):
        """ Sets the LED color to use when the slider is set up as a continuous
        slider. """
        self._slider_color = color

    def set_bipolar_color(self, color):
        """ Sets the LED color to use when the slider is set up as a bipolar slider. """
        self._bipolar_color = color

    def set_inc_dec_colors(self, colors):
        """ Sets the tuple of LED colors (can't increment/can increment) to use when the
        slider is set up as inc/dec buttons. """
        assert isinstance(colors, tuple)
        assert len(colors) == 2
        self._inc_dec_colors = colors

    def set_off_on_colors(self, colors):
        """ Sets the tuple of LED colors (off/on) to use when the slider is set up as an
        on/off button. """
        assert isinstance(colors, tuple)
        assert len(colors) == 2
        self._off_on_colors = colors

    def set_automation_clear_colors(self, colors):
        """ Sets the tuple of LED colors (off/on) to use for the lowest button in the
        slider (clear automation) when fine tune is enabled. """
        assert isinstance(colors, tuple)
        assert len(colors) == 2
        self._automat_clear_colors = colors

    def set_smoothing_speed(self, speed):
        """ Sets the smoother object's smoothing speed. """
        self._smoother.set_smoothing_speed(speed)

    def set_property_to_map_to(self, prop):
        """ Sets the property to map to and connects to it.  Also handles setting up
        observers. """
        self.release_parameter()
        self._parameter_to_map_to = prop
        self._smoother.set_parameter(prop)
        self._on_parameter_name_changed.subject = prop
        self._on_property_value_changed.subject = prop
        self._update_mapping_type()

    def connect_to(self, parameter):
        """ Overrides standard so that mapping type can be properly updated on parameter
        assignment.  Also handles setting up observers. """
        self._on_parameter_changed.subject = None
        self._on_parameter_name_changed.subject = None
        SliderElement.connect_to(self, parameter)
        self._smoother.set_parameter(self._parameter_to_map_to)
        self._on_parameter_changed.subject = self._parameter_to_map_to
        self._on_parameter_name_changed.subject = self._parameter_to_map_to
        self._update_mapping_type()
        return

    def release_parameter(self):
        """ Overrides standard to update mapping type on parameter disconnect and clear
        out observers. """
        self._on_parameter_changed.subject = None
        self._on_property_value_changed.subject = None
        SliderElement.release_parameter(self)
        self._smoother.set_parameter(None)
        self._parameter_to_map_to = None
        self._update_mapping_type()
        return

    def clear_send_cache(self):
        """ Extends standard to clear last sent value. """
        super(SpecialButtonSliderElement, self).clear_send_cache()
        self._last_sent_value = -1

    def send_value(self, value, **k):
        """ Overrides standard to interpret parameter values differently and use different
        LED colors depending on the type of parameter being controlled. Also handles
        clearing LEDs if no parameter assigned. """
        assert value is not None
        assert isinstance(value, int)
        assert value in range(128)
        if self._buttons and value != self._last_sent_value:
            buttons_len = len(self._buttons)
            led_color = 'DefaultButton.Off'
            param = self._parameter_to_map_to
            if param:
                param_value = int((param.value - param.min) / (param.max - param.min) * buttons_len)
                offsets = self._strategy['offsets'](param, param_value, value, buttons_len)
                if offsets == (-1, -1):
                    set_group_button_lights(self._buttons, 'DefaultButton.Off')
                else:
                    for index, button in enumerate(self._buttons):
                        led_color = self._strategy['send_value'](self, param, index, offsets, buttons_len)
                        if button:
                            button.set_light(led_color or 'DefaultButton.Off')

            else:
                set_group_button_lights(self._buttons, 'DefaultButton.Off')
            self._last_sent_value = value
        return

    @subject_slot_group('value')
    def _button_value(self, value, sender):
        """ Overrides standard to interpret values from buttons differently depending
        on the parameter being controlled. """
        self.clear_send_cache()
        self._last_sent_value = -1
        if value:
            self._smoother.stop_smoothing()
            if self._is_velocity_sensitive:
                s = get_smoothing_speed_for_velocity(value)
                self._smoother.set_smoothing_speed(s)
            button_id = list(self._buttons).index(sender)
            buttons_len = len(self._buttons)
            midi_value = int(127 * button_id / (buttons_len - 1))
            param = self._parameter_to_map_to
            if param and param.is_enabled:
                param_value = self._strategy['button_value'](self, param, button_id)
                if param_value is not None:
                    self._smoother.set_parameter_value(param_value, self._mapping_type >= INC_DEC)
            self.notify_value(midi_value)
            self._last_received_value = midi_value
        return

    def _on_smoothing_complete(self):
        self._last_sent_value = -1

    def _update_mapping_type(self):
        """ Updates the type of mapping to use based on the type of parameter being
        controlled. """
        self._last_sent_value = -1
        self._mapping_type = SLIDER
        self._smoother.stop_smoothing()
        if self._parameter_to_map_to is not None:
            param = self._parameter_to_map_to
            if self._is_fine_tuning:
                self._mapping_type = INC_DEC
                self._inc_dec_factor = (param.max - param.min) / 127.0
            elif param.max == abs(param.min):
                self._mapping_type = BIPOLAR
            else:
                parent = param.canonical_parent
                if isinstance(parent, Live.Device.Device):
                    parent = parent.class_name
                    if parameter_is_quantized(param):
                        self._mapping_type = INC_DEC
                        if param.max - param.min == 1.0:
                            self._mapping_type = ON_OFF
                        self._inc_dec_factor = 1
            self._strategy = STRATEGIES[self._mapping_type]
            self._on_parameter_changed()
        else:
            set_group_button_lights(self._buttons, 'DefaultButton.Off')
        self.notify_parameter_value(self.parameter_value)
        self.notify_parameter_name(self.parameter_name)
        return

    @subject_slot('value')
    def _on_parameter_changed(self):
        assert self._parameter_to_map_to is not None
        param = self._parameter_to_map_to
        midi_value = parameter_value_to_midi_value(param.value, param.min, param.max)
        self.send_value(midi_value)
        self.notify_parameter_value(self.parameter_value)
        return

    def message_channel(self):
        raise NotImplementedError

    def message_identifier(self):
        raise NotImplementedError

    def message_map_mode(self):
        return Live.MidiMap.MapMode.absolute

    def identifier_bytes(self):
        raise RuntimeWarning
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialButtonSliderElement.pyc
