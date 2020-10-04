# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV2_LX2_LC2_LD2\LV2_LX2_LC2_LD2.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .FaderfoxScript import FaderfoxScript
from .LV2MixerController import LV2MixerController
from .LV2DeviceController import LV2DeviceController
from .FaderfoxDeviceController import FaderfoxDeviceController
from .LV2TransportController import LV2TransportController
from .consts import *

class LV2_LX2_LC2_LD2(FaderfoxScript):
    """Automap script for LV2 Faderfox controllers"""
    __module__ = __name__
    __name__ = b'LV2_LX2_LC2_LD2 Remote Script'

    def __init__(self, c_instance):
        LV2_LX2_LC2_LD2.realinit(self, c_instance)

    def realinit(self, c_instance):
        self.suffix = b'2'
        FaderfoxScript.realinit(self, c_instance)
        self.mixer_controller = LV2MixerController(self)
        self.device_controller = LV2DeviceController(self)
        self.transport_controller = LV2TransportController(self)
        self.components = [
         self.mixer_controller,
         self.device_controller,
         self.transport_controller]

    def suggest_map_mode(self, cc_no, channel):
        return -1
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/LV2_LX2_LC2_LD2/LV2_LX2_LC2_LD2.pyc
