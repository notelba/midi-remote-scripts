# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\SpecialDeviceComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.DeviceComponent import DeviceComponent
from .consts import FADER_TYPE_STANDARD, DEVICE_MAP_CHANNEL

class SpecialDeviceComponent(DeviceComponent):

    def set_parameter_controls(self, controls):
        if controls:
            for control in controls:
                control.set_channel(DEVICE_MAP_CHANNEL)
                control.set_light_and_type(b'Device.On', FADER_TYPE_STANDARD)

        super(SpecialDeviceComponent, self).set_parameter_controls(controls)

    def _update_parameter_controls(self):
        if self._parameter_controls is not None:
            for control in self._parameter_controls:
                control.update()

        return

    def update(self):
        super(SpecialDeviceComponent, self).update()
        if self.is_enabled():
            self._update_parameter_controls()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro/SpecialDeviceComponent.pyc
