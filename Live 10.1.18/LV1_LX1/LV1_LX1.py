# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV1_LX1\LV1_LX1.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from LV2_LX2_LC2_LD2.FaderfoxComponent import FaderfoxComponent
from LV2_LX2_LC2_LD2.FaderfoxScript import FaderfoxScript
from LV2_LX2_LC2_LD2.FaderfoxMixerController import FaderfoxMixerController
from LV2_LX2_LC2_LD2.FaderfoxDeviceController import FaderfoxDeviceController
from LV2_LX2_LC2_LD2.FaderfoxTransportController import FaderfoxTransportController

class LV1_LX1(FaderfoxScript):
    """Automap script for LV1 Faderfox controllers"""
    __module__ = __name__
    __name__ = b'LV1_LX1 Remote Script'

    def __init__(self, c_instance):
        LV1_LX1.realinit(self, c_instance)

    def realinit(self, c_instance):
        self.suffix = b'1'
        FaderfoxScript.realinit(self, c_instance)
        self.is_lv1 = True
        self.log(b'lv1 lx1')
        self.mixer_controller = FaderfoxMixerController(self)
        self.device_controller = FaderfoxDeviceController(self)
        self.transport_controller = FaderfoxTransportController(self)
        self.components = [
         self.mixer_controller,
         self.device_controller,
         self.transport_controller]
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/LV1_LX1/LV1_LX1.pyc
