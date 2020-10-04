# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\session_recording.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase
from ableton.v2.control_surface.control import ToggleButtonControl

class SessionRecordingComponent(SessionRecordingComponentBase):
    mpc_automation_toggle = ToggleButtonControl(toggled_color=b'Automation.On', untoggled_color=b'Automation.Off')

    def _on_session_automation_record_changed(self):
        super(SessionRecordingComponent, self)._on_session_automation_record_changed()
        self.mpc_automation_toggle.is_toggled = self.song.session_automation_record

    @mpc_automation_toggle.toggled
    def mpc_automation_toggle(self, is_toggled, _):
        self.song.session_automation_record = is_toggled
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/session_recording.pyc
