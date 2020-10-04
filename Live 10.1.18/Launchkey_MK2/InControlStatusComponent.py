# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\InControlStatusComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SubjectSlot import subject_slot
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class InControlStatusComponent(ControlSurfaceComponent):

    def __init__(self, set_is_in_control_on, *a, **k):
        super(InControlStatusComponent, self).__init__(*a, **k)
        self._set_is_in_control_on = set_is_in_control_on

    def set_in_control_status_button(self, button):
        self._on_in_control_value.subject = button

    @subject_slot(b'value')
    def _on_in_control_value(self, value):
        self._set_is_in_control_on(value >= 8)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_MK2/InControlStatusComponent.pyc
