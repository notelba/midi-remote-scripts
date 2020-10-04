# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\notification.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import control_list
from .control import DisplayControl
CLEAR_DELAY = 5

class NotificationComponent(Component):
    display_lines = control_list(DisplayControl, control_count=2)

    def __init__(self, *a, **k):
        super(NotificationComponent, self).__init__(*a, **k)
        self._clear_notification_task = self._tasks.add(task.sequence(task.wait(CLEAR_DELAY), task.run(self._clear_notification)))
        self._clear_notification_task.kill()

    def show_notification(self, upper_line, lower_line):
        self._clear_notification_task.kill()
        self._clear_notification_task.restart()
        self.display_lines[0].message = upper_line
        self.display_lines[1].message = lower_line

    def _clear_notification(self):
        self.display_lines[0].message = b' '
        self.display_lines[1].message = b' '
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_MK3/notification.pyc
