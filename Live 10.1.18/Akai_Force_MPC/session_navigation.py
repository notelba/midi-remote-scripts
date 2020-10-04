# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\session_navigation.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        for scroll_component in (
         self._vertical_banking,
         self._horizontal_banking,
         self._vertical_paginator,
         self._horizontal_paginator):
            for button in (
             scroll_component.scroll_up_button,
             scroll_component.scroll_down_button):
                button.color = b'Navigation.Enabled'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/session_navigation.pyc
