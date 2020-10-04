# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\simple_mode_switcher.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const
from pushbase.note_layout_switcher import ModeSwitcherBase

class SimpleModeSwitcher(ModeSwitcherBase):

    def __init__(self, session_modes=None, *a, **k):
        assert session_modes is not None
        super(SimpleModeSwitcher, self).__init__(*a, **k)
        self._session_modes = session_modes
        self._cycle_mode = session_modes.cycle_mode
        self._get_current_alternative_mode = const(session_modes)
        return

    def _unlock_alternative_mode(self, locked_mode):
        super(SimpleModeSwitcher, self)._unlock_alternative_mode(locked_mode)
        self.locked_mode = None
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/simple_mode_switcher.pyc
