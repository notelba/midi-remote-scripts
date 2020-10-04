# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\simple_device_navigation.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection

class SimpleDeviceNavigationComponent(Component):
    """
    Device navigation component for the case where
    we only need to go to the next or previous device
    on a track.
    """
    next_button = ButtonControl(color=b'Device.Navigation', pressed_color=b'Device.NavigationPressed')
    prev_button = ButtonControl(color=b'Device.Navigation', pressed_color=b'Device.NavigationPressed')

    @next_button.pressed
    def next_button(self, value):
        self._scroll_device_chain(NavDirection.right)

    @prev_button.pressed
    def prev_button(self, value):
        self._scroll_device_chain(NavDirection.left)

    def _scroll_device_chain(self, direction):
        view = self.application.view
        if not view.is_view_visible(b'Detail') or not view.is_view_visible(b'Detail/DeviceChain'):
            view.show_view(b'Detail')
            view.show_view(b'Detail/DeviceChain')
        else:
            view.scroll_view(direction, b'Detail/DeviceChain', False)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/simple_device_navigation.pyc
