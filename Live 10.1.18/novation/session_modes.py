# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\session_modes.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import lazy_attribute, task
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.mode import ModesComponent

class QuickDoubleClickButton(ButtonControl):

    class State(ButtonControl.State):

        @lazy_attribute
        def _double_click_task(self):
            return self.tasks.add(task.wait(0.3))


class SessionModesComponent(ModesComponent):
    cycle_mode_button = QuickDoubleClickButton()
    mode_button_color_control = ButtonControl()

    def __init__(self, *a, **k):
        super(SessionModesComponent, self).__init__(*a, **k)
        self._last_selected_main_mode = b'launch'

    def revert_to_main_mode(self):
        self.selected_mode = self._last_selected_main_mode

    @cycle_mode_button.pressed
    def cycle_mode_button(self, _):
        if self._last_selected_main_mode and self.selected_mode == b'overview':
            self.selected_mode = self._last_selected_main_mode
        elif len(self._mode_list) > 2:
            self.selected_mode = b'mixer' if self.selected_mode == b'launch' else b'launch'

    @cycle_mode_button.double_clicked
    def cycle_mode_button(self, _):
        self.selected_mode = b'overview'

    def _do_enter_mode(self, name):
        super(SessionModesComponent, self)._do_enter_mode(name)
        if self.selected_mode != b'overview':
            self._last_selected_main_mode = self.selected_mode

    def _update_cycle_mode_button(self, selected):
        if selected == b'overview':
            self.mode_button_color_control.color = b'Mode.Session.Overview'
        else:
            self.mode_button_color_control.color = b'Mode.Session.Mixer' if selected == b'mixer' else b'Mode.Session.Launch'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/session_modes.pyc
