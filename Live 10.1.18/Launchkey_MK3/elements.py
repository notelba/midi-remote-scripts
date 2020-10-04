# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\elements.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.elements import ButtonMatrixElement
from novation import sysex
from novation.launchkey_elements import create_button, create_encoder, LaunchkeyElements, SESSION_WIDTH
from . import midi
from .rgb_button import RgbButtonElement
from .simple_display import SimpleDisplayElement

@depends(skin=None)
def create_rgb_button(identifier, name, msg_type=MIDI_CC_TYPE, **k):
    return RgbButtonElement(True, msg_type, 15, identifier, name=name, **k)


def create_display_element(command_bytes, name):
    return SimpleDisplayElement(midi.DISPLAY_HEADER + command_bytes, (sysex.SYSEX_END_BYTE,), name=name)


def create_parameter_display_matrix(command_byte, start_index, name):
    return ButtonMatrixElement(rows=[
     [ create_display_element((command_byte, start_index + index), (b'_Display_{}').format(name, index)) for index in range(8)
     ]], name=(b'{}_Displays').format(name))


class Elements(LaunchkeyElements):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.fader_button_modes_button = create_button(45, b'Fader_Button_Modes_Button')
        self.device_select_button = create_button(51, b'Device_Select_Button')
        self.device_lock_button = create_button(52, b'Device_Lock_Button')
        self.capture_midi_button = create_button(74, b'Capture_MIDI_Button')
        self.quantize_button = create_button(75, b'Quantize_Button')
        self.click_button = create_button(76, b'Click_Button')
        self.undo_button = create_button(77, b'Undo_Button')
        self.up_button = create_rgb_button(106, b'Up_Button')
        self.down_button = create_rgb_button(107, b'Down_Button')
        self.stop_button = create_button(116, b'Stop_Button')
        self.loop_button = create_button(118, b'Loop_Button')
        self.secondary_up_button = create_button(104, b'')
        self.secondary_down_button = create_button(105, b'')
        self.device_select_matrix = ButtonMatrixElement(rows=[ [ create_button(offset + col_index, (b'{}_Device_Select_Button_{}').format(col_index, row_index), msg_type=MIDI_NOTE_TYPE, channel=0) for col_index in range(SESSION_WIDTH) ] for row_index, offset in enumerate(range(64, 87, 16))
                                                             ], name=b'Device_Select_Matrix')
        self.fader_layout_switch = create_button(10, b'Fader_Layout_Switch')
        self.fader_buttons = ButtonMatrixElement(rows=[
         [ create_rgb_button(index + 37, (b'Fader_Button_{}').format(index)) for index in range(SESSION_WIDTH)
         ]], name=b'Fader_Button')
        self.faders = ButtonMatrixElement(rows=[
         [ create_encoder(index + 53, (b'Fader_{}').format(index)) for index in range(SESSION_WIDTH)
         ]], name=b'Faders')
        self.master_fader = create_encoder(61, b'Master_Fader')
        self.notification_display = ButtonMatrixElement(rows=[
         [ create_display_element(midi.NOTIFICATION_DISPLAY_COMMAND_BYTES[index], (b'Notification_Display_Line_{}').format(index)) for index in range(2)
         ]], name=b'Notification_Display')
        self.pot_parameter_name_displays = create_parameter_display_matrix(midi.PARAMETER_NAME_DISPLAY_COMMAND_BYTE, midi.POT_PARAMETER_DISPLAY_START_INDEX, b'Pot_Parameter_Name')
        self.pot_parameter_value_displays = create_parameter_display_matrix(midi.PARAMETER_VALUE_DISPLAY_COMMAND_BYTE, midi.POT_PARAMETER_DISPLAY_START_INDEX, b'Pot_Parameter_Value')
        self.fader_parameter_name_displays = create_parameter_display_matrix(midi.PARAMETER_NAME_DISPLAY_COMMAND_BYTE, midi.FADER_PARAMETER_DISPLAY_START_INDEX, b'Fader_Parameter_Name')
        self.fader_parameter_value_displays = create_parameter_display_matrix(midi.PARAMETER_VALUE_DISPLAY_COMMAND_BYTE, midi.FADER_PARAMETER_DISPLAY_START_INDEX, b'Fader_Parameter_Value')
        self.master_fader_parameter_name_display = create_display_element((
         midi.PARAMETER_NAME_DISPLAY_COMMAND_BYTE,
         midi.MASTER_PARAMETER_DISPLAY_INDEX), b'Master_Fader_Parameter_Name_Display')
        self.master_fader_parameter_value_display = create_display_element((
         midi.PARAMETER_VALUE_DISPLAY_COMMAND_BYTE,
         midi.MASTER_PARAMETER_DISPLAY_INDEX), b'Master_Fader_Parameter_Value_Display')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_MK3/elements.pyc
