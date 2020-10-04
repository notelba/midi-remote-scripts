# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Generic\SelectChanStripComponent.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ChannelStripComponent import ChannelStripComponent

class SelectChanStripComponent(ChannelStripComponent):
    """ Subclass of channel strip component that selects tracks that it arms """

    def __init__(self):
        ChannelStripComponent.__init__(self)

    def _arm_value(self, value):
        assert self._arm_button != None
        assert value in range(128)
        if self.is_enabled():
            track_was_armed = False
            if self._track != None and self._track.can_be_armed:
                track_was_armed = self._track.arm
            ChannelStripComponent._arm_value(self, value)
            if self._track != None and self._track.can_be_armed:
                if self._track.arm and not track_was_armed:
                    if self._track.view.select_instrument():
                        self.song().view.selected_track = self._track
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Generic/SelectChanStripComponent.pyc
