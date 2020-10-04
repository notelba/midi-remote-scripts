# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\hardware_settings.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from . import sysex

class HardwareSettingsComponent(Component):
    __events__ = ('daw_preset', )

    def __init__(self, *a, **k):
        super(HardwareSettingsComponent, self).__init__(*a, **k)
        self._hardware_live_mode_switch = None
        self._memory_preset_switch = None
        self._memory_preset_select_mode_switch = None
        self._selected_preset = None
        return

    def set_hardware_live_mode_switch(self, switch):
        self._hardware_live_mode_switch = switch

    def set_memory_preset_switch(self, switch):
        self._memory_preset_switch = switch
        self._on_memory_preset_changed.subject = switch

    def set_memory_preset_select_mode_switch(self, switch):
        self._memory_preset_select_mode_switch = switch
        self._on_memory_preset_select_mode_enabled.subject = switch

    def set_hardware_live_mode_enabled(self, enable):
        if self._hardware_live_mode_switch and self.is_enabled():
            self._hardware_live_mode_switch.send_value(sysex.ON_VALUE if enable else sysex.OFF_VALUE)

    def select_memory_preset(self, preset_index):
        if self._memory_preset_switch and self.is_enabled():
            self._memory_preset_switch.send_value(preset_index)
            self._selected_preset = preset_index

    @listens(b'value')
    def _on_memory_preset_changed(self, preset_info):
        self._selected_preset = preset_info[0]

    @listens(b'value')
    def _on_memory_preset_select_mode_enabled(self, enabled_info):
        enabled = enabled_info[0]
        self.notify_daw_preset(not enabled and self._selected_preset == sysex.DAW_MEMORY_PRESET_INDEX)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_Essential/hardware_settings.pyc
