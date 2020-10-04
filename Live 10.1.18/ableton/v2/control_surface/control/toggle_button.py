# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\toggle_button.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .control import Connectable, control_event, control_color
from .button import ButtonControlBase

class ToggleButtonControl(ButtonControlBase):
    """
    A Control representing a button that can be toggled on and off.

    The class is extending
    :class:`~ableton.v2.control_surface.control.button.ButtonControlBase`
    by adding a :attr:`toggled` event and colors for the two states.

    :meth:`State.connect_property` can be used to connect the Control with a boolean
    property.
    """
    toggled = control_event(b'toggled')

    class State(ButtonControlBase.State, Connectable):
        """
        State-full representation of the Control.
        """
        untoggled_color = control_color(b'DefaultButton.Off')
        toggled_color = control_color(b'DefaultButton.On')
        requires_listenable_connected_property = True

        def __init__(self, untoggled_color=None, toggled_color=None, *a, **k):
            super(ToggleButtonControl.State, self).__init__(*a, **k)
            if untoggled_color is not None:
                self.untoggled_color = untoggled_color
            if toggled_color is not None:
                self.toggled_color = toggled_color
            self._is_toggled = False
            return

        @property
        def is_toggled(self):
            """
            Represents the button's toggled state. If a property is connected to the
            Control, it will not be affected by setting is_toggled.
            """
            return self._is_toggled

        @is_toggled.setter
        def is_toggled(self, toggled):
            if self._is_toggled != toggled:
                self._is_toggled = toggled
                self._send_current_color()

        def connect_property(self, *a):
            """
            Creates a bidirectional binding between a boolean property and the button's
            toggled state.
            """
            super(ToggleButtonControl.State, self).connect_property(*a)
            self.is_toggled = self.connected_property_value

        def on_connected_property_changed(self, value):
            self.is_toggled = value

        def _send_button_color(self):
            self._control_element.set_light(self.toggled_color if self._is_toggled else self.untoggled_color)

        def _on_pressed(self):
            super(ToggleButtonControl.State, self)._on_pressed()
            self._is_toggled = not self._is_toggled
            self._call_listener(b'toggled', self._is_toggled)
            self.connected_property_value = self.is_toggled
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/control/toggle_button.pyc
