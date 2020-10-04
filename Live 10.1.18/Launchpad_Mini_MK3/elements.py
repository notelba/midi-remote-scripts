# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Mini_MK3\elements.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends
from ableton.v2.control_surface.elements import ColorSysexElement
from novation import sysex
from novation.launchpad_elements import create_button, LaunchpadElements
from . import sysex_ids as ids

class Elements(LaunchpadElements):
    model_id = ids.LP_MINI_MK3_ID
    default_layout = sysex.KEYS_LAYOUT_BYTE

    @depends(skin=None)
    def __init__(self, skin=None, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.drums_mode_button = create_button(96, b'Drums_Mode_Button')
        self.keys_mode_button = create_button(97, b'Keys_Mode_Button')
        self.user_mode_button = create_button(98, b'User_Mode_Button')
        session_button_color_identifier = sysex.STD_MSG_HEADER + (
         ids.LP_MINI_MK3_ID,
         20)
        self.session_button_color_element = ColorSysexElement(name=b'Session_Button_Color_Element', sysex_identifier=session_button_color_identifier, send_message_generator=lambda v: session_button_color_identifier + v + (sysex.SYSEX_END_BYTE,), skin=skin)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Mini_MK3/elements.pyc
