# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\hardware_settings.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from KeyLab_Essential import sysex
from KeyLab_Essential.hardware_settings import HardwareSettingsComponent as HardwareSettingsComponentBase

class HardwareSettingsComponent(HardwareSettingsComponentBase):

    def __init__(self, *a, **k):
        super(HardwareSettingsComponent, self).__init__(*a, **k)
        self._vegas_mode_switch = None
        return

    def set_vegas_mode_switch(self, switch):
        self._vegas_mode_switch = switch

    def set_hardware_live_mode_enabled(self, enable):
        super(HardwareSettingsComponent, self).set_hardware_live_mode_enabled(enable)
        if enable and self._vegas_mode_switch:
            self._vegas_mode_switch.send_value(sysex.OFF_VALUE)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_mkII/hardware_settings.pyc
