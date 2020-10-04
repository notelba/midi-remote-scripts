# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\sysex.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .control import Control, control_color

class ColorSysexControl(Control):

    class State(Control.State):
        color = control_color(b'DefaultButton.Disabled')

        def __init__(self, color=None, *a, **k):
            super(ColorSysexControl.State, self).__init__(*a, **k)
            if color is not None:
                self.color = color
            return

        def set_control_element(self, control_element):
            super(ColorSysexControl.State, self).set_control_element(control_element)
            self._send_current_color()

        def update(self):
            super(ColorSysexControl.State, self).update()
            self._send_current_color()

        def _send_current_color(self):
            if self._control_element:
                self._control_element.set_light(self.color)

    def __init__(self, *a, **k):
        super(ColorSysexControl, self).__init__(extra_args=a, extra_kws=k)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/control/sysex.pyc
