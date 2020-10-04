# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\SpecialModesComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ModesComponent import ReenterBehaviour, ModesComponent

class SpecialModesComponent(ModesComponent):

    def on_enabled_changed(self):
        super(SpecialModesComponent, self).on_enabled_changed()
        if not self.is_enabled():
            self._last_selected_mode = None
        return


class SpecialReenterBehaviour(ReenterBehaviour):
    """
    When a mode with this behaviour is reentered, enters on_reenter_mode instead
    """

    def __init__(self, mode_name=None, *a, **k):
        super(ReenterBehaviour, self).__init__(*a, **k)
        self._mode_name = mode_name

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(ReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            if self._mode_name is not None and component.get_mode(self._mode_name):
                component.push_mode(self._mode_name)
                component.pop_unselected_modes()
        return


class CancelingReenterBehaviour(SpecialReenterBehaviour):

    def __init__(self, *a, **k):
        super(CancelingReenterBehaviour, self).__init__(*a, **k)
        self._reenter_mode_active = False

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(CancelingReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            self._reenter_mode_active = True

    def release_immediate(self, component, mode):
        super(CancelingReenterBehaviour, self).release_immediate(component, mode)
        self._return(component, mode)

    def release_delayed(self, component, mode):
        super(CancelingReenterBehaviour, self).release_delayed(component, mode)
        self._return(component, mode)

    def _return(self, component, mode):
        if self._reenter_mode_active:
            component.push_mode(mode)
            component.pop_unselected_modes()
            self._reenter_mode_active = False
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro/SpecialModesComponent.pyc
