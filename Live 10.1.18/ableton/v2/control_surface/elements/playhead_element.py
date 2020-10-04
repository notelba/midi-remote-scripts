# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\playhead_element.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ...base import nop
from .proxy_element import ProxyElement

class NullPlayhead(object):
    notes = []
    start_time = 0.0
    step_length = 1.0
    velocity = 0.0
    wrap_around = False
    track = None
    clip = None
    set_feedback_channels = nop


class PlayheadElement(ProxyElement):

    def __init__(self, playhead=None, *a, **k):
        super(PlayheadElement, self).__init__(proxied_object=playhead, proxied_interface=NullPlayhead())

    def reset(self):
        self.track = None
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/elements/playhead_element.pyc
