# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\device_component.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import ParameterInfo
from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v2.control_surface.control import ButtonControl
from .parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity

def is_wavetable(device):
    return liveobj_valid(device) and device.class_name == b'InstrumentVector'


class DeviceComponent(DeviceComponentBase):
    shift_button = ButtonControl()

    @shift_button.pressed
    def shift_button(self, button):
        decorated_device = self.device()
        if is_wavetable(decorated_device):
            decorated_device.osc_1_pitch.adjust_finegrain = True
            decorated_device.osc_2_pitch.adjust_finegrain = True

    @shift_button.released
    def shift_button(self, button):
        decorated_device = self.device()
        if is_wavetable(decorated_device):
            decorated_device.osc_1_pitch.adjust_finegrain = False
            decorated_device.osc_2_pitch.adjust_finegrain = False

    def _create_parameter_info(self, parameter, name):
        device_class_name = self.device().class_name
        return ParameterInfo(parameter=parameter, name=name, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter, device_class_name), fine_grain_encoder_sensitivity=fine_grain_parameter_mapping_sensitivity(parameter, device_class_name))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push/device_component.pyc
