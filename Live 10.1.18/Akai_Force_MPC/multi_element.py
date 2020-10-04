# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\multi_element.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import MultiElement as MultiElementBase

class MultiElement(MultiElementBase):

    def __init__(self, *a, **k):
        super(MultiElement, self).__init__(*a, **k)
        self._parameter_to_map_to = None
        return

    @property
    def touch_element(self):
        for control in self.owned_control_elements():
            if hasattr(control, b'touch_element'):
                return control.touch_element

        return

    def connect_to(self, parameter):
        self._parameter_to_map_to = parameter
        for control in self.owned_control_elements():
            control.connect_to(parameter)

    def release_parameter(self):
        self._parameter_to_map_to = None
        for control in self.owned_control_elements():
            control.release_parameter()

        return

    def mapped_parameter(self):
        return self._parameter_to_map_to
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/multi_element.pyc
