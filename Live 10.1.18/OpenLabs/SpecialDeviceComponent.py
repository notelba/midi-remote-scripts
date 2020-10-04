# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\OpenLabs\SpecialDeviceComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.DeviceComponent import DeviceComponent

class SpecialDeviceComponent(DeviceComponent):

    def __init__(self):
        DeviceComponent.__init__(self)

    def _device_parameters_to_map(self):
        assert self.is_enabled()
        assert self._device != None
        assert self._parameter_controls != None
        return self._device.parameters[1:]
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/OpenLabs/SpecialDeviceComponent.pyc
