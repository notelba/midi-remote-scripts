# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\velocity_levels_element.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ...base import EventObject, listenable_property
from .proxy_element import ProxyElement

class NullVelocityLevels(EventObject):
    enabled = False
    target_note = -1
    target_channel = -1
    source_channel = -1
    notes = []

    @property
    def levels(self):
        return []

    @listenable_property
    def last_played_level(self):
        return -1.0


class VelocityLevelsElement(ProxyElement):

    def __init__(self, velocity_levels=None, *a, **k):
        super(VelocityLevelsElement, self).__init__(proxied_object=velocity_levels, proxied_interface=NullVelocityLevels())

    def reset(self):
        self.notes = []
        self.source_channel = -1
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/elements/velocity_levels_element.pyc
