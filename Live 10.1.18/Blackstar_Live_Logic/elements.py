# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\elements.py
# Compiled at: 2020-07-20 20:22:59
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import MIDI_CC_TYPE
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, SysexElement
from ableton.v2.control_surface.midi import SYSEX_END
from .midi import LIVE_INTEGRATION_MODE_ID, NUMERIC_DISPLAY_COMMAND, SYSEX_HEADER
from .skin import skin
from .time_display import TimeDisplayElement
NUM_LOOPER_SWITCHES = 6

def create_button(identifier, name, msg_type=MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, 15, identifier, skin=skin, name=name, **k)


class Elements(object):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.foot_switches = ButtonMatrixElement(rows=[
         [ create_button(i, (b'Foot_Switch_{}').format(i)) for i in range(NUM_LOOPER_SWITCHES)
         ]], name=b'Foot_Switches')
        self.time_display = TimeDisplayElement(SYSEX_HEADER + NUMERIC_DISPLAY_COMMAND, (SYSEX_END,))
        self.live_integration_mode_switch = SysexElement(name=b'Live_Integration_Mode_Switch', send_message_generator=lambda v: LIVE_INTEGRATION_MODE_ID + (v, SYSEX_END))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Blackstar_Live_Logic/elements.pyc
