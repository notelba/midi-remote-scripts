# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\blinking_button.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import lazy_attribute, task
from ableton.v2.control_surface.control import ButtonControl as ButtonControlBase, control_color
DEFAULT_BLINK_PERIOD = 0.1

class BlinkingButtonControl(ButtonControlBase):

    class State(ButtonControlBase.State):
        blink_on_color = control_color(b'DefaultButton.On')
        blink_off_color = control_color(b'DefaultButton.Off')

        def __init__(self, blink_on_color=b'DefaultButton.On', blink_off_color=b'DefaultButton.Off', blink_period=DEFAULT_BLINK_PERIOD, *a, **k):
            super(BlinkingButtonControl.State, self).__init__(*a, **k)
            self.blink_on_color = blink_on_color
            self.blink_off_color = blink_off_color
            self._blink_period = blink_period

        def start_blinking(self):
            self._blink_task.restart()

        def stop_blinking(self):
            self._blink_task.kill()

        @lazy_attribute
        def _blink_task(self):
            blink_on = partial(self._set_blinking_color, self.blink_on_color)
            blink_off = partial(self._set_blinking_color, self.blink_off_color)
            return self.tasks.add(task.sequence(task.run(blink_on), task.wait(self._blink_period), task.run(blink_off), task.wait(self._blink_period), task.run(blink_on), task.wait(self._blink_period), task.run(blink_off)))

        def _set_blinking_color(self, color):
            if self._control_element:
                self._control_element.set_light(color)

        def _kill_all_tasks(self):
            super(BlinkingButtonControl.State, self)._kill_all_tasks()
            self._blink_task.kill()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/blinking_button.pyc
