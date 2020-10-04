# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\scroll.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import nop
from ableton.v2.control_surface.components import ScrollComponent as ScrollComponentBase
from ableton.v2.control_surface.control import EncoderControl

class ScrollComponent(ScrollComponentBase):
    scroll_encoder = EncoderControl()

    @scroll_encoder.value
    def scroll_encoder(self, value, _):
        scroll_step = nop
        if value > 0 and self.can_scroll_down():
            scroll_step = self._do_scroll_down
        elif value < 0 and self.can_scroll_up():
            scroll_step = self._do_scroll_up
        scroll_step()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/iRig_Keys_IO/scroll.pyc
