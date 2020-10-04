# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_Mini_MK3\elements.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import ComboElement
from novation.launchkey_elements import LaunchkeyElements

class Elements(LaunchkeyElements):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)

        def with_shift(button):
            return ComboElement(control=button, modifier=self.shift_button, name=(b'{}_With_Shift').format(button.name))

        self.play_button_with_shift = with_shift(self.play_button)
        self.record_button_with_shift = with_shift(self.record_button)
        self.scene_launch_button_with_shift = with_shift(self.scene_launch_buttons_raw[0])
        self.stop_solo_mute_button_with_shift = with_shift(self.scene_launch_buttons_raw[1])
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_Mini_MK3/elements.pyc
