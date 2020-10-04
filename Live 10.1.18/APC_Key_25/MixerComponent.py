# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_Key_25\MixerComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _APC.MixerComponent import MixerComponent as MixerComponentBase
from _APC.MixerComponent import ChanStripComponent as ChanStripComponentBase
from _Framework.Util import nop

class ChanStripComponent(ChanStripComponentBase):

    def __init__(self, *a, **k):
        self.reset_button_on_exchange = nop
        super(ChanStripComponent, self).__init__(*a, **k)


class MixerComponent(MixerComponentBase):

    def on_num_sends_changed(self):
        if self.send_index is None and self.num_sends > 0:
            self.send_index = 0
        return

    def _create_strip(self):
        return ChanStripComponent()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC_Key_25/MixerComponent.pyc
