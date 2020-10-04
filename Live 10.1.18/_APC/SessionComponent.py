# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_APC\SessionComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SessionComponent import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):
    """ Special SessionComponent for the APC controllers' combination mode """

    def link_with_track_offset(self, track_offset):
        assert track_offset >= 0
        if self._is_linked():
            self._unlink()
        self.set_offsets(track_offset, self.scene_offset())
        self._link()

    def unlink(self):
        if self._is_linked():
            self._unlink()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_APC/SessionComponent.pyc
