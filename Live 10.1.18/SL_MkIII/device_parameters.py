# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\device_parameters.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from ableton.v2.control_surface import InternalParameterBase
from ableton.v2.control_surface.components import DisplayingDeviceParameterComponent
from ableton.v2.control_surface.control import ColorSysexControl, control_list
from .util import convert_parameter_value_to_midi_value

def is_internal_parameter(parameter):
    return isinstance(parameter, InternalParameterBase)


WIDTH = 8

class DeviceParameterComponent(DisplayingDeviceParameterComponent):
    parameter_color_fields = control_list(ColorSysexControl, WIDTH)
    encoder_color_fields = control_list(ColorSysexControl, WIDTH)

    def __init__(self, *a, **k):
        self._parameter_controls = None
        super(DeviceParameterComponent, self).__init__(*a, **k)
        return

    def set_parameter_controls(self, encoders):
        super(DeviceParameterComponent, self).set_parameter_controls(encoders)
        self._parameter_controls = encoders

    def _update_parameter_values(self):
        super(DeviceParameterComponent, self)._update_parameter_values()
        for parameter, control in izip_longest(self.parameters, self._parameter_controls or []):
            if is_internal_parameter(parameter) and control:
                control.send_value(convert_parameter_value_to_midi_value(parameter))

    def _update_parameters(self):
        super(DeviceParameterComponent, self)._update_parameters()
        self._update_color_fields()

    def _update_color_fields(self):
        for color_field_index, parameter_info in izip_longest(xrange(WIDTH), self._parameter_provider.parameters[:WIDTH]):
            parameter = parameter_info.parameter if parameter_info else None
            color = b'Device.On' if parameter else b'DefaultButton.Disabled'
            self.parameter_color_fields[color_field_index].color = color
            self.encoder_color_fields[color_field_index].color = color

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/SL_MkIII/device_parameters.pyc
