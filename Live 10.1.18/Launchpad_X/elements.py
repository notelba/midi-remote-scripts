# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\elements.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import depends
from ableton.v2.control_surface.elements import ButtonMatrixElement, ColorSysexElement, SysexElement
from novation import sysex
from novation.launchpad_elements import create_button, create_slider, LaunchpadElements, SESSION_WIDTH, BUTTON_FADER_COLOR_CHANNEL
from . import sysex_ids as ids

class Elements(LaunchpadElements):
    model_id = ids.LP_X_ID
    default_layout = sysex.NOTE_LAYOUT_BYTE
    button_fader_cc_offset = 21

    @depends(skin=None)
    def __init__(self, skin=None, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self._create_drum_pads()
        self._create_scale_pads()
        self._create_scale_feedback_switch()
        self.note_mode_button = create_button(96, b'Note_Mode_Button')
        self.custom_mode_button = create_button(97, b'Custom_Mode_Button')
        self.record_button = create_button(98, b'Record_Button')
        self.button_faders = ButtonMatrixElement(rows=[
         [ create_slider(index + self.button_fader_cc_offset, (b'Button_Fader_{}').format(index)) for index in xrange(SESSION_WIDTH)
         ]], name=b'Button_Faders')
        self.button_fader_color_elements_raw = [ create_button(index + self.button_fader_cc_offset, (b'Button_Fader_Color_Element_{}').format(index), channel=BUTTON_FADER_COLOR_CHANNEL) for index in xrange(SESSION_WIDTH)
                                               ]
        self.button_fader_color_elements = ButtonMatrixElement(rows=[
         self.button_fader_color_elements_raw], name=b'Button_Fader_Color_Elements')
        self.note_layout_switch = SysexElement(name=b'Note_Layout_Switch', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (
         ids.LP_X_ID, sysex.NOTE_LAYOUT_COMMAND_BYTE, v, sysex.SYSEX_END_BYTE), default_value=sysex.SCALE_LAYOUT_BYTE)
        session_button_color_identifier = sysex.STD_MSG_HEADER + (ids.LP_X_ID, 20)
        self.session_button_color_element = ColorSysexElement(name=b'Session_Button_Color_Element', sysex_identifier=session_button_color_identifier, send_message_generator=lambda v: session_button_color_identifier + v + (sysex.SYSEX_END_BYTE,), skin=skin)
        self.button_fader_setup_element = SysexElement(name=b'Button_Fader_Setup_Element', send_message_generator=partial(self._fader_setup_message_generator, 0))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_X/elements.pyc
