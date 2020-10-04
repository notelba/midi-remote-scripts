# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ResettableScrollComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ScrollComponent import ScrollComponent, Scrollable
from ControlUtils import kill_scroll_tasks, skin_scroll_component

class ResettableScrollable(Scrollable):
    """ Extends standard to include reset method that can be implemented. """

    def reset(self):
        raise NotImplementedError


class ResettableObjectPropertyScrollable(ResettableScrollable):
    """ ResettableObjectPropertyScrollable is a ResettableScrollable
    meant to be used for scrolling between values of a property of an
    object. This will not allow scrolling if the object doesn't exist.
    The scroller object still needs to be disabled however. """

    def __init__(self, prop_name, v_min, v_max, default_value, factor=0.01, *a, **k):
        self._prop_name = prop_name
        self._min = v_min
        self._max = v_max
        self._default_value = default_value
        self._factor = factor
        self._object = None
        super(ResettableObjectPropertyScrollable, self).__init__(*a, **k)
        return

    def disconnect(self):
        self._prop_name = None
        self._object = None
        return

    def set_object(self, obj):
        """ Sets the object associated with this property. """
        self._object = obj

    def set_property_name(self, name):
        """ Sets the name of the property to control. """
        self._prop_name = name

    def set_min_and_max_values(self, v_min, v_max):
        """ Sets the minimum and maximum values of this property. """
        self._min = v_min
        self._max = v_max

    def set_default_value(self, value):
        """ Sets the default value of this property. """
        self._default_value = value

    def set_adjustment_factor(self, factor):
        """ Sets the adjustment factory to use for this property. """
        self._factor = factor

    def can_scroll_up(self):
        return self._object is not None and getattr(self._object, self._prop_name) < self._max

    def can_scroll_down(self):
        return self._object is not None and getattr(self._object, self._prop_name) > self._min

    def reset(self):
        if self._object:
            setattr(self._object, self._prop_name, self._default_value)

    def scroll_up(self):
        if self._object:
            self._increment_scroll_position(1)

    def scroll_down(self):
        if self._object:
            self._increment_scroll_position(-1)

    def _increment_scroll_position(self, factor):
        inc = factor * self._factor
        setattr(self._object, self._prop_name, max(self._min, min(self._max, getattr(self._object, self._prop_name) + inc)))


class ResettableScrollComponent(ScrollComponent):
    """ Extends standard to call reset on the scrollable when both scroll buttons
    are pressed.

    Note that this this doesn't handle disabling scroll buttons so this entire component
    should be disabled when scrolling isn't possible. """

    def __init__(self, *a, **k):
        self._did_reset = False
        self._state_colors = None
        super(ResettableScrollComponent, self).__init__(*a, **k)
        return

    def disconnect(self):
        super(ResettableScrollComponent, self).disconnect()
        self._state_colors = None
        return

    def set_scroll_up_button(self, button):
        if not self._state_colors:
            self._set_state_colors()
        kill_scroll_tasks((self,))
        super(ResettableScrollComponent, self).set_scroll_up_button(button)
        self._update_scroll_buttons()

    def set_scroll_down_button(self, button):
        if not self._state_colors:
            self._set_state_colors()
        kill_scroll_tasks((self,))
        super(ResettableScrollComponent, self).set_scroll_down_button(button)
        self._update_scroll_buttons()

    def set_color(self, color):
        """ Sets the color to use when the scroll buttons aren't pressed. """
        if not self._state_colors:
            self._set_state_colors()
        self._state_colors[1] = color
        self._update_scroll_buttons()

    def _set_state_colors(self):
        self._state_colors = [
         self.scroll_up_button._disabled_color,
         self.scroll_up_button._color]

    def _on_scroll_pressed(self, button, scroll_step, scroll_task):
        self._did_reset = self._should_reset()
        if self._did_reset:
            self._scroll_task_up.kill()
            self._scroll_task_down.kill()
            self.scrollable.reset()
            self._update_scroll_buttons()
        else:
            super(ResettableScrollComponent, self)._on_scroll_pressed(button, scroll_step, scroll_task)

    def _on_scroll_released(self, scroll_task):
        scroll_task.kill()
        if not self._did_reset:
            self._ensure_scroll_one_direction()

    def _should_reset(self):
        return self.scroll_up_button.is_pressed and self.scroll_down_button.is_pressed

    def _update_scroll_buttons(self):
        if self.is_enabled() and self._state_colors:
            self.scroll_up_button.color = self._state_colors[self.can_scroll_up()]
            self.scroll_down_button.color = self._state_colors[self.can_scroll_down()]


class ScrolledProperty(ResettableScrollComponent):
    """ Simple object that combines a ResettableScrollComponent and
    ResettableObjectPropertyScrollable to allow for ease of use, particularly in
    CompoundComponents. """

    def __init__(self, led_value, prop_name, v_min, v_max, default_value, factor=0.01):
        prop = ResettableObjectPropertyScrollable(prop_name, v_min, v_max, default_value, factor=factor)
        super(ScrolledProperty, self).__init__(prop)
        skin_scroll_component(self, color=led_value)

    def set_object(self, obj):
        """ Sets the scrollable's object. """
        self.scrollable.set_object(obj)

    def set_property_name(self, name):
        """ Sets the name of the scrollable's property. """
        self.scrollable.set_property_name(name)

    def set_min_and_max_values(self, v_min, v_max):
        """ Sets the min and max values of the scrollable's property. """
        self.scrollable.set_min_and_max_values(v_min, v_max)

    def set_default_value(self, value):
        """ Sets the default value of the scrollable's property. """
        self.scrollable.set_default_value(value)

    def set_adjustment_factor(self, factor):
        """ Sets the adjustment factor of the scrollable's property. """
        self.scrollable.set_adjustment_factor(factor)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ResettableScrollComponent.pyc
