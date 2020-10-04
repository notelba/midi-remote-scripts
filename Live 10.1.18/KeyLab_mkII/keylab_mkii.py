# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\keylab_mkii.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.components import SessionRecordingComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement, PhysicalDisplayElement, SysexElement
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent
from KeyLab_Essential import sysex
from KeyLab_Essential.control_element_utils import create_button, create_pad_led
from KeyLab_Essential.keylab_essential import KeyLabEssential
from .channel_strip import ChannelStripComponent
from .hardware_settings import HardwareSettingsComponent
from .mixer import MixerComponent
from .session import SessionComponent
from .view_control import ViewControlComponent
PAD_IDS = (
 (36, 37, 38, 39, 44, 45, 46, 47), (40, 41, 42, 43, 48, 49, 50, 51))
PAD_LED_IDS = (
 (112, 113, 114, 115, 120, 121, 122, 123),
 (116, 117, 118, 119, 124, 125, 126, 127))
DISPLAY_LINE_WIDTH = 16

class KeyLabMkII(KeyLabEssential):
    mixer_component_type = MixerComponent
    session_component_type = SessionComponent
    view_control_component_type = ViewControlComponent
    hardware_settings_component_type = HardwareSettingsComponent
    channel_strip_component_type = ChannelStripComponent

    def __init__(self, *a, **k):
        super(KeyLabMkII, self).__init__(*a, **k)
        with self.component_guard():
            self._create_session_recording()

    def _create_controls(self):
        super(KeyLabMkII, self)._create_controls()

        def make_button_row(index_offset, name):
            return ButtonMatrixElement(rows=[
             [ create_button(index + index_offset, name=(b'{}_{}').format(name, index)) for index in xrange(8)
             ]], name=(b'{}s').format(name))

        self._select_buttons = make_button_row(24, b'Select_Button')
        self._solo_buttons = make_button_row(8, b'Solo_Button')
        self._mute_buttons = make_button_row(16, b'Mute_Button')
        self._record_arm_buttons = make_button_row(0, b'Record_Arm_Buttons')
        self._automation_button = create_button(56, name=b'Automation_Button')
        self._re_enable_automation_button = create_button(57, name=b'Re_Enable_Automation_Button')
        self._view_button = create_button(74, name=b'View_Button')
        self._pads = ButtonMatrixElement(rows=[ [ create_button(identifier, channel=9, name=(b'Pad_{}_{}').format(col_index, row_index)) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PAD_IDS)
                                              ])
        self._pad_leds = ButtonMatrixElement(rows=[ [ create_pad_led(identifier, (b'Pad_LED_{}_{}').format(col_index, row_index)) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PAD_LED_IDS)
                                                  ], name=b'Pad_LED_Matrix')
        self._display = PhysicalDisplayElement(DISPLAY_LINE_WIDTH, name=b'Display')
        self._display.set_message_parts(sysex.LCD_SET_STRING_MESSAGE_HEADER + (sysex.LCD_LINE_1_ITEM_ID,), (
         sysex.NULL, sysex.LCD_LINE_2_ITEM_ID) + (ord(b' '),) * DISPLAY_LINE_WIDTH + (sysex.NULL, sysex.END_BYTE))
        self._mixer_mode_cycle_button = create_button(51, name=b'Mixer_Mode_Cycle_Button')
        self._vegas_mode_switch = SysexElement(send_message_generator=lambda b: sysex.VEGAS_MODE_MESSAGE_HEADER + (
         b, sysex.END_BYTE), name=b'Vegas_Mode_Switch')

    def _create_mixer(self):
        super(KeyLabMkII, self)._create_mixer()
        self._mixer.layer += Layer(track_select_buttons=self._select_buttons, solo_buttons=self._solo_buttons, mute_buttons=self._mute_buttons, arm_buttons=self._record_arm_buttons, selected_track_name_display=self._display)
        self._mixer_modes = ModesComponent(name=b'Mixer_Modes')
        self._mixer_modes.add_mode(b'volume_mode', AddLayerMode(self._mixer, Layer(volume_controls=self._faders)))
        self._mixer_modes.add_mode(b'sends_a_mode', AddLayerMode(self._mixer, Layer(send_controls=self._faders)))
        self._mixer_modes.layer = Layer(cycle_mode_button=self._mixer_mode_cycle_button)
        self._mixer_modes.selected_mode = b'volume_mode'

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name=b'Session_Recording', is_enabled=False, layer=Layer(automation_button=self._automation_button, re_enable_automation_button=self._re_enable_automation_button))
        self._session_recording.set_enabled(True)

    def _create_view_control(self):
        super(KeyLabMkII, self)._create_view_control()
        self._view_control.layer += Layer(document_view_toggle_button=self._view_button)

    def _create_hardware_settings(self):
        super(KeyLabMkII, self)._create_hardware_settings()
        self._hardware_settings.layer += Layer(vegas_mode_switch=self._vegas_mode_switch)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_mkII/keylab_mkii.pyc
