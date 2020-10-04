# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\parameter_provider.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid, NamedTuple, EventObject
DISCRETE_PARAMETERS_DICT = {b'GlueCompressor': ('Ratio', 'Attack', 'Release', 'Peak Clip In')}

def is_parameter_quantized(parameter, parent_device):
    is_quantized = False
    if liveobj_valid(parameter):
        device_class = getattr(parent_device, b'class_name', None)
        is_quantized = parameter.is_quantized or device_class in DISCRETE_PARAMETERS_DICT and parameter.name in DISCRETE_PARAMETERS_DICT[device_class]
    return is_quantized


class ParameterInfo(NamedTuple):
    parameter = None
    default_encoder_sensitivity = None
    fine_grain_encoder_sensitivity = None

    def __init__(self, name=None, *a, **k):
        super(ParameterInfo, self).__init__(_overriden_name=name, *a, **k)

    @property
    def name(self):
        actual_name = self.parameter.name if liveobj_valid(self.parameter) else b''
        return self._overriden_name or actual_name

    def __eq__(self, other_info):
        return super(ParameterInfo, self).__eq__(other_info) and self.name == other_info.name


class ParameterProvider(EventObject):
    __events__ = ('parameters', )

    @property
    def parameters(self):
        return []
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/parameter_provider.pyc
