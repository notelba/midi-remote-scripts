# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\control.py
# Compiled at: 2020-06-08 15:00:06
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import Control
DEFAULT_MESSAGE = b'-'

class DisplayControl(Control):

    class State(Control.State):

        def __init__(self, *a, **k):
            super(DisplayControl.State, self).__init__(*a, **k)
            self._message = DEFAULT_MESSAGE

        @property
        def message(self):
            return self._message

        @message.setter
        def message(self, message):
            self._message = DEFAULT_MESSAGE if message is None else message
            self._send_current_message()
            return

        def set_control_element(self, control_element):
            super(DisplayControl.State, self).set_control_element(control_element)
            self._send_current_message()

        def update(self):
            super(DisplayControl.State, self).update()
            self._send_current_message()

        def _send_current_message(self):
            if self._control_element:
                self._control_element.display_message(self._message)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/control.pyc
