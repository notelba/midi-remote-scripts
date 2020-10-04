# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\DeviceNavComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class DeviceNavComponent(ControlSurfaceComponent):
    """ Component that can navigate the selection of devices """

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._left_button = None
        self._right_button = None
        return

    def disconnect(self):
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
            self._left_button = None
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
            self._right_button = None
        return

    def set_device_nav_buttons(self, left_button, right_button):
        identify_sender = True
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
        self._left_button = left_button
        if self._left_button != None:
            self._left_button.add_value_listener(self._nav_value, identify_sender)
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
        self._right_button = right_button
        if self._right_button != None:
            self._right_button.add_value_listener(self._nav_value, identify_sender)
        self.update()
        return

    def on_enabled_changed(self):
        self.update()

    def _nav_value(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                modifier_pressed = True
                if not self.application().view.is_view_visible(b'Detail') or not self.application().view.is_view_visible(b'Detail/DeviceChain'):
                    self.application().view.show_view(b'Detail')
                    self.application().view.show_view(b'Detail/DeviceChain')
                else:
                    direction = Live.Application.Application.View.NavDirection.left
                    if sender == self._right_button:
                        direction = Live.Application.Application.View.NavDirection.right
                    self.application().view.scroll_view(direction, b'Detail/DeviceChain', not modifier_pressed)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_AIR_25_49_61/DeviceNavComponent.pyc
