# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launch_Control\DeviceNavigationComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class DeviceNavigationComponent(ControlSurfaceComponent):
    _next_button = None
    _previous_button = None

    def set_next_device_button(self, button):
        self._next_button = button
        self._update_button_states()
        self._on_next_device.subject = button

    def set_previous_device_button(self, button):
        self._previous_button = button
        self._update_button_states()
        self._on_previous_device.subject = button

    @subject_slot(b'value')
    def _on_next_device(self, value):
        if value:
            self._scroll_device_view(Live.Application.Application.View.NavDirection.right)

    @subject_slot(b'value')
    def _on_previous_device(self, value):
        if value:
            self._scroll_device_view(Live.Application.Application.View.NavDirection.left)

    def _scroll_device_view(self, direction):
        self.application().view.show_view(b'Detail')
        self.application().view.show_view(b'Detail/DeviceChain')
        self.application().view.scroll_view(direction, b'Detail/DeviceChain', False)

    def _update_button_states(self):
        if self._next_button:
            self._next_button.turn_on()
        if self._previous_button:
            self._previous_button.turn_on()

    def update(self):
        super(DeviceNavigationComponent, self).update()
        if self.is_enabled():
            self._update_button_states()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launch_Control/DeviceNavigationComponent.pyc
