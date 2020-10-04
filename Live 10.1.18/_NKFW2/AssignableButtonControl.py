# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\AssignableButtonControl.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class ButtonFunctionControl(ControlSurfaceComponent):
    """ ButtonFunctionControl allows a button to trigger an arbitrary function and
    provides local LED control. """

    def __init__(self, parent, off_color, on_color, function_name=None, floating_type=None, *a, **k):
        super(ButtonFunctionControl, self).__init__(*a, **k)
        self.is_private = True
        self._parent = parent
        self._colors = (off_color, on_color)
        self._function_name = function_name
        self._floating_type = floating_type
        self._button = None
        return

    def disconnect(self):
        super(ButtonFunctionControl, self).disconnect()
        self._parent = None
        self._colors = None
        self._button = None
        return

    def _get_parent(self):
        return self._parent

    def _set_parent(self, parent):
        self._parent = parent
        self._handle_new_parent()

    def _handle_new_parent(self):
        """ Called after the new parent has been set.  This is broken out so that it
        can be overridden. """
        self._update_button()

    parent = property(_get_parent, _set_parent)

    @property
    def floating_type(self):
        """ Returns the floating type (such as clip) of this component. """
        return self._floating_type

    def set_button(self, button):
        """ Sets the button that will trigger the function. """
        self._button = button
        self._on_button_value.subject = button
        self._update_button()

    @subject_slot('value')
    def _on_button_value(self, value):
        if self._parent:
            if value:
                getattr(self._parent, self._function_name)()
            self._button.set_light(self._colors[bool(value)])

    def update(self):
        super(ButtonFunctionControl, self).update()
        self._update_button()

    def _update_button(self):
        if self.is_enabled() and self._button:
            if self._parent:
                self._button.set_light(self._colors[0])
            else:
                self._button.turn_off()


class ButtonPropertyControl(ButtonFunctionControl):
    """ ButtonPropertyControl extends ButtonFunctionControl to allow a button to be used
    for controlling and providing feedback from an arbitrary property. This allows
    for momentary control over the property and can also call a function. """

    def __init__(self, *a, **k):
        self._property_name = k.pop('property_name', None)
        self._fixed_value = k.pop('fixed_value', None)
        self._is_momentary = k.pop('is_momentary', False)
        self._output_transform = k.pop('output_transform', None)
        super(ButtonPropertyControl, self).__init__(*a, **k)
        self._property_slot = None
        self._connect_slot()
        self._button = None
        return

    def disconnect(self):
        super(ButtonPropertyControl, self).disconnect()
        self._property_slot = None
        return

    def _handle_new_parent(self):
        """ Overrides standard to set up slot. """
        self._connect_slot()
        self._update_button()

    def _connect_slot(self):
        """ Registers a slot for the property to control and also unregisters the previous
        slot. """
        self.unregister_disconnectable(self._property_slot)
        if self._parent:
            self._property_slot = self.register_slot(self._parent, self._update_button, self._property_name)

    @subject_slot('value')
    def _on_button_value(self, value):
        if self._parent and value or self._is_momentary:
            if self._function_name is not None and value:
                getattr(self._parent, self._function_name)()
            else:
                if self._fixed_value is not None:
                    p_value = self._fixed_value
                else:
                    p_value = not getattr(self._parent, self._property_name)
                setattr(self._parent, self._property_name, p_value)
        return

    def _update_button(self):
        if self.is_enabled() and self._button:
            if self._parent:
                p_value = getattr(self._parent, self._property_name)
                if self._output_transform is not None:
                    color_index = self._output_transform(p_value, self._fixed_value)
                elif self._fixed_value is not None:
                    color_index = 1 if p_value == self._fixed_value else 0
                else:
                    color_index = 1 if p_value else 0
                self._button.set_light(self._colors[color_index])
            else:
                self._button.turn_off()
        return


class ButtonViewToggleControl(ButtonFunctionControl):
    """ ButtonViewToggleControl extends ButtonFunctionControl to allow a button to used
    for toggling views, which requires special handling due to the way view listeners are
    implemented. """

    def __init__(self, *a, **k):
        self._view_name = k.pop('view_name', None)
        self._second_view_name = k.pop('second_view_name', None)
        super(ButtonViewToggleControl, self).__init__(*a, **k)
        self._parent.add_is_view_visible_listener(self._view_name, self._update_button)
        return

    def disconnect(self):
        lst = self._update_button
        if self._parent.is_view_visible_has_listener(self._view_name, lst):
            self._parent.remove_is_view_visible_listener(self._view_name, lst)
        super(ButtonViewToggleControl, self).disconnect()

    @subject_slot('value')
    def _on_button_value(self, value):
        if value:
            if self._parent.is_view_visible(self._view_name):
                if self._second_view_name is not None:
                    self._parent.show_view(self._second_view_name)
                else:
                    self._parent.hide_view(self._view_name)
            else:
                self._parent.show_view(self._view_name)
        return

    def _update_button(self):
        if self.is_enabled() and self._button:
            color_index = 1 if self._parent.is_view_visible(self._view_name) else 0
            self._button.set_light(self._colors[color_index])
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/AssignableButtonControl.pyc
