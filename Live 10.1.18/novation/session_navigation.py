# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\session_navigation.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
from .util import skin_scroll_buttons

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        skin_scroll_buttons(self._vertical_banking, b'Session.Navigation', b'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_banking, b'Session.Navigation', b'Session.NavigationPressed')
        skin_scroll_buttons(self._vertical_paginator, b'Session.Navigation', b'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_paginator, b'Session.Navigation', b'Session.NavigationPressed')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/session_navigation.pyc
