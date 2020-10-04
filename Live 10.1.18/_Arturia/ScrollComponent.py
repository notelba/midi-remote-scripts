# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Arturia\ScrollComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ScrollComponent import ScrollComponent as ScrollComponentBase
from _Framework.Control import EncoderControl

class ScrollComponent(ScrollComponentBase):
    scroll_encoder = EncoderControl()

    def set_scroll_encoder(self, encoder):
        self.scroll_encoder.set_control_element(encoder)
        self.update()

    @scroll_encoder.value
    def scroll_encoder(self, value, encoder):
        scroll_step = None
        if value > 0 and self.can_scroll_down():
            scroll_step = self._do_scroll_down
        elif value < 0 and self.can_scroll_up():
            scroll_step = self._do_scroll_up
        if scroll_step is not None:
            scroll_step()
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Arturia/ScrollComponent.pyc
