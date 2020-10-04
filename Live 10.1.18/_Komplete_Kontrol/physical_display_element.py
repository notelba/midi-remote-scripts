# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\physical_display_element.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, imap
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase

class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        return chain(*imap(lambda x: self._translate_string(unicode(x).strip()), display._logical_segments))

    def _request_send_message(self):
        self._send_message()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Komplete_Kontrol/physical_display_element.pyc
