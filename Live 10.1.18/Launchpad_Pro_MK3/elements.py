# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro_MK3\elements.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import PrioritizedResource
from ableton.v2.control_surface.elements import ButtonMatrixElement, ComboElement, SysexElement
from novation import sysex
from novation.launchpad_elements import create_button, create_slider, LaunchpadElements, SESSION_WIDTH, BUTTON_FADER_COLOR_CHANNEL
from . import sysex_ids as ids
FADER_MODES = [
 b'volume', b'pan', b'sends', b'device']

def create_modifier_button(identifier, name):
    return create_button(identifier, (b'{}_Button').format(name), resource_type=PrioritizedResource)


class Elements(LaunchpadElements):
    model_id = ids.LP_PRO_MK3_ID
    default_layout = ids.NOTE_LAYOUT_BYTES

    def __init__(self, *a, **k):
        super(Elements, self).__init__(arrow_button_identifiers=(80, 70, 91, 92), session_mode_button_identifier=93, *a, **k)
        self._create_drum_pads()
        self._create_scale_pads()
        self._create_scale_feedback_switch()
        self.quantize_button = create_modifier_button(40, b'Quantize')
        self.duplicate_button = create_modifier_button(50, b'Duplicate')
        self.clear_button = create_modifier_button(60, b'Clear')
        self.shift_button = create_modifier_button(90, b'Shift')
        self.record_arm_button = create_button(1, b'Record_Arm_Button')
        self.mute_button = create_button(2, b'Mute_Button')
        self.solo_button = create_button(3, b'Solo_Button')
        self.volume_button = create_button(4, b'Volume_Button')
        self.pan_button = create_button(5, b'Pan_Button')
        self.sends_button = create_button(6, b'Sends_Button')
        self.device_button = create_button(7, b'Device_Button')
        self.stop_clip_button = create_button(8, b'Stop_Clip_Button')
        self.record_button = create_button(10, b'Record_Button')
        self.play_button = create_button(20, b'Play_Button')
        self.fixed_length_button = create_button(30, b'Fixed_Length_Button')
        self.track_select_buttons_raw = [ create_button(index + 101, (b'Track_Select_Button_{}').format(index)) for index in xrange(SESSION_WIDTH)
                                        ]
        self.track_select_buttons = ButtonMatrixElement(rows=[
         self.track_select_buttons_raw], name=b'Track_Select_Buttons')
        for bank, bank_name in enumerate(FADER_MODES):
            capitalized_name = bank_name.capitalize()
            control_elements_name = (b'{}_button_faders').format(bank_name)
            setattr(self, control_elements_name, ButtonMatrixElement(rows=[
             [ create_slider(index + bank * SESSION_WIDTH, (b'{}_Button_Fader_{}').format(capitalized_name, index)) for index in range(SESSION_WIDTH)
             ]], name=(b'{}_Button_Faders').format(capitalized_name)))
            color_elements_name = (b'{}_button_fader_color_elements').format(bank_name)
            setattr(self, color_elements_name, ButtonMatrixElement(rows=[
             [ create_button(index + bank * SESSION_WIDTH, (b'{}_Button_Fader_Color_Element_{}').format(capitalized_name, index), channel=BUTTON_FADER_COLOR_CHANNEL) for index in range(SESSION_WIDTH)
             ]], name=(b'{}_Button_Fader_Color_Elements').format(capitalized_name)))

        def with_shift(button):
            return ComboElement(control=button, modifier=self.shift_button, name=(b'{}_With_Shift').format(button.name))

        self.track_select_buttons_with_shift = ButtonMatrixElement(rows=[[ with_shift(button) for button in self.track_select_buttons_raw ]], name=b'Track_Select_Buttons_With_Shift')
        self.up_button_with_shift = with_shift(self.up_button)
        self.down_button_with_shift = with_shift(self.down_button)
        self.left_button_with_shift = with_shift(self.left_button)
        self.right_button_with_shift = with_shift(self.right_button)
        self.quantize_button_with_shift = with_shift(self.quantize_button)
        self.duplicate_button_with_shift = with_shift(self.duplicate_button)
        self.clear_button_with_shift = with_shift(self.clear_button)
        self.record_arm_button_with_shift = with_shift(self.record_arm_button)
        self.mute_button_with_shift = with_shift(self.mute_button)
        self.solo_button_with_shift = with_shift(self.solo_button)
        self.sends_button_with_shift = with_shift(self.sends_button)
        self.volume_button_with_shift = with_shift(self.volume_button)
        self.pan_button_with_shift = with_shift(self.pan_button)
        self.device_button_with_shift = with_shift(self.device_button)
        self.stop_clip_button_with_shift = with_shift(self.stop_clip_button)
        self.record_button_with_shift = with_shift(self.record_button)
        self.play_button_with_shift = with_shift(self.play_button)
        self.fixed_length_button_with_shift = with_shift(self.fixed_length_button)
        print_to_clip_identifier = sysex.STD_MSG_HEADER + (
         self.model_id,
         sysex.PRINT_COMMAND_BYTE)
        self.print_to_clip_element = SysexElement(name=b'Print_To_Clip_Element', sysex_identifier=print_to_clip_identifier, send_message_generator=lambda v: print_to_clip_identifier + (
         v, sysex.SYSEX_END_BYTE))
        self.print_to_clip_enabler_element = SysexElement(name=b'Print_To_Clip_Enabler', send_message_generator=lambda v: sysex.STD_MSG_HEADER + (
         self.model_id, sysex.PRINT_ENABLE_COMMAND_BYTE, v, sysex.SYSEX_END_BYTE), default_value=0)
        self.fader_setup_element = SysexElement(name=b'Fader_Setup_Element', send_message_generator=self._fader_setup_message_generator)
        self.stop_fader_element = SysexElement(name=b'Stop_Fader_Element', send_message_generator=self._stop_fader_message_generator, sysex_identifier=sysex.STD_MSG_HEADER + (
         self.model_id, sysex.STOP_FADER_COMMAND_BYTE))

    def _stop_fader_message_generator(self, bank):
        return sysex.STD_MSG_HEADER + (
         self.model_id,
         sysex.STOP_FADER_COMMAND_BYTE,
         bank,
         sysex.SYSEX_END_BYTE)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro_MK3/elements.pyc
