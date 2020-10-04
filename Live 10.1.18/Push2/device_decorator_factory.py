# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_decorator_factory.py
# Compiled at: 2020-07-31 16:17:47
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from .auto_filter import AutoFilterDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .device_decoration import SamplerDeviceDecorator, PedalDeviceDecorator, DrumBussDeviceDecorator, UtilityDeviceDecorator
from .delay import DelayDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .operator import OperatorDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {b'OriginalSimpler': SimplerDeviceDecorator, 
       b'Operator': OperatorDeviceDecorator, 
       b'MultiSampler': SamplerDeviceDecorator, 
       b'AutoFilter': AutoFilterDeviceDecorator, 
       b'Eq8': Eq8DeviceDecorator, 
       b'Compressor2': CompressorDeviceDecorator, 
       b'Pedal': PedalDeviceDecorator, 
       b'DrumBuss': DrumBussDeviceDecorator, 
       b'Echo': EchoDeviceDecorator, 
       b'InstrumentVector': WavetableDeviceDecorator, 
       b'StereoGain': UtilityDeviceDecorator, 
       b'Delay': DelayDeviceDecorator}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/device_decorator_factory.pyc
