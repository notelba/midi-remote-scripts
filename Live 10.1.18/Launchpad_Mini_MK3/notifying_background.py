# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Mini_MK3\notifying_background.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.control_surface.components import BackgroundComponent

class NotifyingBackgroundComponent(BackgroundComponent):
    __events__ = ('value', )

    def register_slot(self, control, *a):
        super(BackgroundComponent, self).register_slot(control, partial(self.__on_control_value, control), b'value')

    def __on_control_value(self, control, value):
        self.notify_value(control, value)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Mini_MK3/notifying_background.pyc
