# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_APC\DeviceBankButtonElement.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ComboElement import ComboElement

class DeviceBankButtonElement(ComboElement):
    """
    ComboElement that will change the channel, while the control is grabbed
    """

    def on_nested_control_element_received(self, control):
        super(DeviceBankButtonElement, self).on_nested_control_element_received(control)
        if control == self.wrapped_control:
            self.wrapped_control.set_channel(1)

    def on_nested_control_element_lost(self, control):
        super(DeviceBankButtonElement, self).on_nested_control_element_lost(control)
        if control == self.wrapped_control:
            self.wrapped_control.set_channel(0)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_APC/DeviceBankButtonElement.pyc
