# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Generic\SpecialMixerComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.MixerComponent import MixerComponent
from .SelectChanStripComponent import SelectChanStripComponent

class SpecialMixerComponent(MixerComponent):
    """ Class encompassing several selecting channel strips to form a mixer """

    def _create_strip(self):
        return SelectChanStripComponent()

    def set_bank_up_button(self, button):
        self.set_bank_buttons(button, self._bank_down_button)

    def set_bank_down_button(self, button):
        self.set_bank_buttons(self._bank_up_button, button)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Generic/SpecialMixerComponent.pyc
