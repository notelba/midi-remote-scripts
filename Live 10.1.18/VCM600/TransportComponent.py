# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\TransportComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.TransportComponent import TransportComponent as TransportComponentBase

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._punch_in_toggle.is_momentary = False
        self._punch_out_toggle.is_momentary = False
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/VCM600/TransportComponent.pyc
