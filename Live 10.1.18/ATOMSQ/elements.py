# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\elements.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement, SysexElement
from . import midi
from .simple_display import SimpleDisplayElement
from .skin import rgb_skin, skin
from .touch_strip import TouchStripElement
SESSION_WIDTH = 16
SESSION_HEIGHT = 1
BANK_BUTTON_NAMES = [ (b'bank_{}_button').format(l) for l in b'abcdefgh' ]
DISPLAY_RGB_VALUES = {b'r': 0, b'g': 91, b'b': 91}
TOUCH_STRIP_LED_CC_RANGE = range(55, 80)

def create_button(identifier, name, msg_type=MIDI_CC_TYPE, skin=skin, **k):
    return ButtonElement(True, msg_type, 0, identifier, name=name, skin=skin, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.relative_smooth_signed_bit, name=name, **k)


def create_display_element(strip_id, name, r=127, g=127, b=127, center=True):
    return SimpleDisplayElement(midi.DISPLAY_HEADER + (strip_id, r, g, b, int(not center)), (
     midi.SYSEX_END_BYTE,), name=name)


class Elements(object):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.display_encoder = create_encoder(29, b'Display_Encoder')
        self.shift_button = create_button(31, b'Shift_Button', resource_type=PrioritizedResource)
        self.plus_button = create_button(0, b'Plus_Button', msg_type=MIDI_NOTE_TYPE, skin=rgb_skin)
        self.minus_button = create_button(1, b'Minus_Button', msg_type=MIDI_NOTE_TYPE, skin=rgb_skin)
        self.song_mode_button = create_button(32, b'Song_Mode_Button')
        self.instrument_mode_button = create_button(33, b'Instrument_Mode_Button')
        self.editor_mode_button = create_button(34, b'Editor_Mode_Button')
        self.user_mode_button = create_button(35, b'User_Mode_Button')
        self.display_left_button = create_button(42, b'Display_Left_Button')
        self.display_right_button = create_button(43, b'Display_Right_Button')
        self.up_button = create_button(87, b'Up_Button')
        self.down_button = create_button(89, b'Down_Button')
        self.left_button = create_button(90, b'Left_Button')
        self.right_button = create_button(102, b'Right_Button')
        self.click_button = create_button(105, b'Click_Button')
        self.record_button = create_button(107, b'Record_Button')
        self.play_button = create_button(109, b'Play_Button', skin=rgb_skin)
        self.stop_button = create_button(111, b'Stop_Button')
        for i, name in enumerate(BANK_BUTTON_NAMES):
            setattr(self, name, create_button(i, name.title(), skin=rgb_skin))

        def with_shift(button):
            return ComboElement(control=button, modifier=self.shift_button, name=(b'{}_With_Shift').format(button.name))

        self.play_button_with_shift = with_shift(self.play_button)
        self.stop_button_with_shift = with_shift(self.stop_button)
        self.record_button_with_shift = with_shift(self.record_button)
        self.up_button_with_shift = with_shift(self.up_button)
        self.down_button_with_shift = with_shift(self.down_button)
        self.display_buttons_raw = [ create_button(index + 36, (b'Display_Button_{}').format(index)) for index in range(6)
                                   ]
        self.display_buttons = ButtonMatrixElement(rows=[
         self.display_buttons_raw], name=b'Display_Buttons')
        self.lower_pads = ButtonMatrixElement(rows=[
         [ create_button(36 + index, (b'Lower_Pad_{}').format(index), msg_type=MIDI_NOTE_TYPE, skin=rgb_skin) for index in range(SESSION_WIDTH)
         ]], name=b'Lower_Pads')
        self.upper_pads = ButtonMatrixElement(rows=[
         [ create_button(52 + index, (b'Upper_Pad_{}').format(index), msg_type=MIDI_NOTE_TYPE, skin=rgb_skin) for index in range(SESSION_WIDTH)
         ]], name=b'Upper_Pads')
        self.encoders_raw = [ create_encoder(index + 14, (b'Encoder_{}').format(index)) for index in range(8) ]
        self.encoders = ButtonMatrixElement(rows=[self.encoders_raw], name=b'Encoders')
        self.button_label_display_matrix = ButtonMatrixElement(rows=[
         [ create_display_element(strip_id, (b'Button_Label_Display_{}').format(index), **DISPLAY_RGB_VALUES) for index, strip_id in enumerate((0,
                                                                                                                                       1,
                                                                                                                                       2,
                                                                                                                                       11,
                                                                                                                                       12,
                                                                                                                                       13))
         ]], name=b'Button_Label_Displays')
        self.track_name_display = create_display_element(6, b'Track_Name_Display', **DISPLAY_RGB_VALUES)
        self.device_name_display = create_display_element(7, b'Device_Name_Display', **DISPLAY_RGB_VALUES)
        self.lower_firmware_toggle_switch = SysexElement(name=b'Lower_Firmware_Toggle_Switch', send_message_generator=lambda v: midi.LOWER_FIRMWARE_TOGGLE_HEADER + (
         v, midi.SYSEX_END_BYTE))
        self.upper_firmware_toggle_switch = SysexElement(name=b'Upper_Firmware_Toggle_Switch', send_message_generator=lambda v: midi.UPPER_FIRMWARE_TOGGLE_HEADER + (
         v, midi.SYSEX_END_BYTE))
        self.touch_strip_tap = create_button(64, b'Touch_Strip_Tap')
        self.touch_strip_leds = [ create_button(led_id, (b'Touch_Strip_LED_{}').format(index)) for index, led_id in enumerate(TOUCH_STRIP_LED_CC_RANGE)
                                ]
        self.touch_strip = TouchStripElement(name=b'Touch_Strip', msg_type=MIDI_PB_TYPE, channel=15, touch_element=self.touch_strip_tap, leds=self.touch_strip_leds)
        self.touch_strip.set_needs_takeover(False)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/elements.pyc
