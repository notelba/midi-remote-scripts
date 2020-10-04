# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\PropertyControl.py
# Compiled at: 2017-10-19 12:46:57
import Live
ABS_MODES = (
 Live.MidiMap.MapMode.absolute,
 Live.MidiMap.MapMode.absolute_14_bit)
from _Framework.SubjectSlot import SlotManager, Subject, subject_slot
from _Framework.Util import nop
from SpecialButtonSliderElement import SpecialButtonSliderElement
from SpecialEncoderElement import SpecialEncoderElement
from ControlUtils import release_parameters, parameter_value_to_midi_value
from Utils import live_object_is_valid

class PropertyControl(SlotManager, Subject):
    """ PropertyControl allows a SpecialEncoderElement or SpecialButtonSliderElement to
    control a property similar to how a parameter can be controlled with takeover
    handling for controls that need it.  This module also includes variations for
    resetting quantized properties (ResettablePropertyControl) and for specialized
    parameter control (ParameterControl). """
    __subject_events__ = ('name', 'value', 'automation_state', 'state', 'range')

    def __init__(self, prop_name, parent, full_range, abs_range=None, default_value=0.0, rel_thresh=10, rel_step=1.0, value_items=(), quantized=True, display_name=None, display_callback=None, display_value_transform=None, can_enforce_takeover=True, cast_value_to_int=False, add_nops=True, *a, **k):
        super(PropertyControl, self).__init__(*a, **k)
        self._control = None
        self._parent = parent
        self._property_name = prop_name
        self._use_full_range = False
        self._full_range = None
        self._absolute_range = None
        self._absolute_factor = None
        self._enforce_takeover = False
        self._suppress_feedback = False
        self._can_suppress_feedback = True
        self._default_value = default_value
        self._relative_threshold = rel_thresh
        self._relative_step = rel_step
        self._value_items = value_items
        self._is_quantized = bool(quantized)
        self._can_enforce_takeover = bool(can_enforce_takeover)
        self._awaiting_control_value = False
        self._can_set_value_directly = True
        self._display_name = display_name
        self._display_callback = display_callback
        self._display_value_transform = display_value_transform
        if display_value_transform is None:
            self._display_value_transform = lambda x: str(x)
        self._cast_value_to_int = bool(cast_value_to_int)
        self.canonical_parent = None
        if add_nops:
            self.clear_parameter_envelope = nop
            self.begin_gesture = nop
            self.end_gesture = nop
        self.set_range(full_range, abs_range)
        return

    def disconnect(self):
        self._remove_property_listener()
        super(PropertyControl, self).disconnect()
        release_parameters((self._control,))
        self._control = None
        self._parent = None
        self._property_name = None
        self._full_range = None
        self._absolute_range = None
        self._value_items = None
        self._display_callback = None
        self.canonical_parent = None
        return

    def set_control(self, control):
        """ Sets the control to use for controlling this property. """
        self._remove_property_listener()
        self._on_takeover_control_value_changed.subject = None
        self._on_relative_control_value_changed.subject = None
        release_parameters((self._control,))
        self._control = control
        self._can_set_value_directly = True
        self._use_full_range = False
        if control:
            if isinstance(control, SpecialButtonSliderElement):
                self._can_set_value_directly = False
                control.set_property_to_map_to(self if live_object_is_valid(self._parent) else None)
            elif isinstance(control, SpecialEncoderElement):
                control.set_property_to_map_to(self if live_object_is_valid(self._parent) else None)
                self._can_suppress_feedback = control.should_suppress_feedback_for_property_controls()
            if control.message_map_mode() in ABS_MODES:
                self._can_enforce_takeover = self._can_enforce_takeover and control.needs_takeover()
                if self._can_set_value_directly:
                    self._on_takeover_control_value_changed.subject = control
            else:
                self._on_relative_control_value_changed.subject = control
                self._use_full_range = True
            self._add_property_listener()
        return

    def set_parent(self, parent):
        """ Sets the parent of this property. """
        self._remove_property_listener()
        self._parent = parent if live_object_is_valid(parent) else None
        if self._control:
            self._add_property_listener()
        if isinstance(self._control, SpecialButtonSliderElement):
            self._control.set_property_to_map_to(self if self._parent else None)
        elif isinstance(self._control, SpecialEncoderElement):
            self._control.set_property_to_map_to(self if self._parent else None)
        self._update_control()
        return

    def set_property_name(self, name):
        """ Sets the name of this property and updates all. """
        self._remove_property_listener()
        self._property_name = name
        self.set_parent(self._parent)

    def set_range(self, full_range, abs_range=None):
        """ Sets the range of this property. """
        notify = self._full_range != full_range
        self._full_range = full_range
        if abs_range:
            self._absolute_range = abs_range
        else:
            self._absolute_range = full_range
        self._absolute_factor = (self._absolute_range[1] - self._absolute_range[0]) / 127.0
        self._on_property_value_changed()
        if notify:
            self.notify_range()

    def set_default_value(self, value):
        """ Sets the default value of this property. """
        self._default_value = value

    def set_relative_step(self, step):
        """ Sets the relative step factor to use. """
        self._relative_step = step

    def set_property_value(self, current_value, new_value):
        """ Sets the property value and calls the display callback if there is one.
        This is broken out so that it can be overridden. """
        if live_object_is_valid(self._parent) and current_value != new_value:
            setattr(self._parent, self._property_name, new_value)
            if self._display_callback:
                self._display_callback(new_value)

    def get_property_value(self):
        """ Returns the value of the property. This is broken out so that it can be
        overridden. """
        if live_object_is_valid(self._parent):
            return getattr(self._parent, self._property_name)
        else:
            return

    @subject_slot('value')
    def _on_takeover_control_value_changed(self, control_value):
        if live_object_is_valid(self._parent):
            param_value = self.get_property_value()
            scaled_value = self._absolute_factor * control_value
            last_control_value = self._control._last_received_value
            control_diff = control_value - last_control_value
            if self._enforce_takeover:
                if self._awaiting_control_value:
                    self._on_property_value_changed()
                    return
                if control_diff > 0 and last_control_value < 127:
                    if param_value > self._absolute_range[1]:
                        return
                    step_factor = (self._absolute_range[1] - param_value) / float(127 - last_control_value)
                    scaled_value = step_factor + step_factor * control_diff + param_value - self._absolute_range[0]
                elif control_diff < 0 and last_control_value > 0:
                    step_factor = (param_value - self._absolute_range[0]) / float(last_control_value)
                    scaled_value = control_value * step_factor
            scaled_value += self._absolute_range[0]
            if self._is_quantized:
                scaled_value = int(scaled_value)
            new_param_value = max(self._absolute_range[0], min(self._absolute_range[1], scaled_value))
            self._suppress_feedback = self._can_suppress_feedback
            self.set_property_value(param_value, new_param_value)

    @subject_slot('value')
    def _on_relative_control_value_changed(self, value):
        if live_object_is_valid(self._parent):
            param_value = self.get_property_value()
            factor = self._control.get_adjustment_factor(value, self._relative_threshold)
            if factor:
                factor = factor * self._relative_step
                if self._is_quantized:
                    factor = int(factor)
                new_param_value = max(self._full_range[0], min(self._full_range[1], param_value + factor))
                self.set_property_value(param_value, new_param_value)

    def _on_property_value_changed(self):
        if live_object_is_valid(self._parent) and self._control:
            if self._control.message_map_mode() in ABS_MODES:
                last_control_value = self._control._last_received_value
                self._awaiting_control_value = last_control_value == -1
                value = self.get_property_value()
                if self._awaiting_control_value or value < self._absolute_range[0] or value > self._absolute_range[1]:
                    self._enforce_takeover = self._can_enforce_takeover
                else:
                    scaled_value = self._absolute_factor * last_control_value
                    if self._is_quantized:
                        scaled_value = int(scaled_value)
                    if self._can_enforce_takeover:
                        self._enforce_takeover = abs(scaled_value - value) > self._absolute_factor * 2
            self.notify_value()
        self._update_control()

    def update(self):
        if self._control:
            self._control.set_property_to_map_to(self if live_object_is_valid(self._parent) else None)
        return

    def _update_control(self):
        if self._control and not self._suppress_feedback:
            if live_object_is_valid(self._parent):
                prop_value = self.get_property_value()
                if prop_value == self._absolute_range[1]:
                    self._control.send_value(127)
                elif prop_value > self._absolute_range[0]:
                    scaled_value = parameter_value_to_midi_value(prop_value, self._absolute_range[0], self._absolute_range[1])
                    self._control.send_value(scaled_value)
                else:
                    self._control.send_value(0)
            else:
                self._control.send_value(0)
        self._suppress_feedback = False

    def _add_property_listener(self):
        if live_object_is_valid(self._parent):
            add_method = getattr(self._parent, 'add_%s_listener' % self._property_name)
            add_method(self._on_property_value_changed)
            self._on_property_value_changed()

    def _remove_property_listener(self):
        if live_object_is_valid(self._parent):
            remove_method = getattr(self._parent, 'remove_%s_listener' % self._property_name)
            try:
                remove_method(self._on_property_value_changed)
            except:
                pass

    def __str__(self):
        """ Returns the property value as a string. """
        if live_object_is_valid(self._parent):
            return self._display_value_transform(self.get_property_value())
        return ''

    @property
    def name(self):
        return self._display_name or self._property_name

    @property
    def original_name(self):
        return self._display_name or self._property_name

    @property
    def min(self):
        if self._use_full_range:
            return self._full_range[0]
        return self._absolute_range[0]

    @property
    def max(self):
        if self._use_full_range:
            return self._full_range[1]
        return self._absolute_range[1]

    @property
    def is_quantized(self):
        return self._is_quantized

    @property
    def is_enabled(self):
        return True

    @property
    def state(self):
        return 0

    @property
    def automation_state(self):
        return Live.DeviceParameter.AutomationState.none

    @property
    def default_value(self):
        return self._default_value

    @property
    def value_items(self):
        return self._value_items

    def _get_value(self):
        if live_object_is_valid(self._parent):
            if self._cast_value_to_int:
                return int(self.get_property_value())
            return self.get_property_value()
        return 0

    def _set_value(self, value):
        if live_object_is_valid(self._parent):
            self.set_property_value(self.get_property_value(), value)

    value = property(_get_value, _set_value)


class ResettablePropertyControl(PropertyControl):
    """ Specialized version that always return false for is_quantized.  This allows
    quantized properties to be reset to a default value instead of toggled. """

    def set_relative_step(self, _):
        """ Overrides standard to do nothing as this should not be set for quantized
        properties. """
        pass

    @property
    def is_quantized(self):
        return False


class ParameterControl(PropertyControl):
    """ Specialized version that controls a parameter rather than a property. This is
    only useful in cases where an alternate form of parameter control is needed.  """

    def __init__(self, *a, **k):
        super(ParameterControl, self).__init__(add_nops=False, *a, **k)

    def set_property_value(self, current_value, new_value):
        """ Overrides standard to set value of parameter. """
        if live_object_is_valid(self._parent) and current_value != new_value:
            self._parent.value = new_value

    def get_property_value(self):
        """ Overrides standard to get value of parameter. """
        if live_object_is_valid(self._parent):
            return self._parent.value
        else:
            return

    def _add_property_listener(self):
        """ Overrides standard to use subject_slot. """
        if live_object_is_valid(self._parent):
            self._on_parameter_changed.subject = self._parent
            self._on_property_value_changed()

    def _remove_property_listener(self):
        """ Overrides standard to use subject_slot. """
        self._on_parameter_changed.subject = None
        return

    @subject_slot('value')
    def _on_parameter_changed(self):
        self._on_property_value_changed()

    def __str__(self):
        if live_object_is_valid(self._parent):
            return str(self._parent)
        return ''

    @property
    def name(self):
        if live_object_is_valid(self._parent):
            return self._parent.name
        return ''

    @property
    def automation_state(self):
        if live_object_is_valid(self._parent):
            return self._parent.automation_state
        return Live.DeviceParameter.AutomationState.none

    @property
    def default_value(self):
        if live_object_is_valid(self._parent):
            return self._parent.default_value
        return 0.0

    def begin_gesture(self):
        if live_object_is_valid(self._parent):
            self._parent.begin_gesture()

    def end_gesture(self):
        if live_object_is_valid(self._parent):
            self._parent.end_gesture()

    def clear_parameter_envelope(self, clip):
        if live_object_is_valid(self._parent):
            clip.clear_envelope(self._parent)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/PropertyControl.pyc
