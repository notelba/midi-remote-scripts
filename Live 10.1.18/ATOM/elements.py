# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\elements.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import Live
from ableton.v2.base import depends, recursive_map
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, EncoderElement
SESSION_WIDTH = 4
SESSION_HEIGHT = 4

@depends(skin=None)
def create_button(identifier, name, msg_type=MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, 0, identifier, name=name, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.relative_smooth_signed_bit, name=name, **k)


class Elements(object):

    def __init__(self, *a, **k):
        super(Elements, self).__init__(*a, **k)
        self.shift_button = create_button(32, b'Shift_Button', resource_type=PrioritizedResource)
        self.zoom_button = create_button(104, b'Zoom_Button', resource_type=PrioritizedResource)
        self.note_repeat_button = create_button(24, b'Note_Repeat_Button')
        self.full_level_button = create_button(25, b'Full_Level_Button')
        self.bank_button = create_button(26, b'Bank_Button')
        self.preset_button = create_button(27, b'Preset_Button')
        self.show_hide_button = create_button(29, b'Show_Hide_Button')
        self.nudge_button = create_button(30, b'Nudge_Button')
        self.editor_button = create_button(31, b'Editor_Button')
        self.set_loop_button = create_button(85, b'Set_Loop_Button')
        self.setup_button = create_button(86, b'Setup_Button')
        self.up_button = create_button(87, b'Up_Button')
        self.down_button = create_button(89, b'Down_Button')
        self.left_button = create_button(90, b'Left_Button')
        self.right_button = create_button(102, b'Right_Button')
        self.select_button = create_button(103, b'Select_Button')
        self.click_button = create_button(105, b'Click_Button')
        self.record_button = create_button(107, b'Record_Button')
        self.play_button = create_button(109, b'Play_Button')
        self.stop_button = create_button(111, b'Stop_Button')
        self.pads_raw = [ [ create_button(offset + col_index, (b'{}_Pad_{}').format(col_index, row_index), msg_type=MIDI_NOTE_TYPE) for col_index in xrange(SESSION_WIDTH) ] for row_index, offset in enumerate(xrange(48, 32, -4))
                        ]
        self.pads = ButtonMatrixElement(rows=self.pads_raw, name=b'Pads')

        def with_modifier(modifier_button, button):
            return ComboElement(control=button, modifier=modifier_button, name=(b'{}_With_{}').format(button.name, modifier_button.name.split(b'_')[0]))

        self.play_button_with_shift = with_modifier(self.shift_button, self.play_button)
        self.stop_button_with_shift = with_modifier(self.shift_button, self.stop_button)
        self.pads_with_shift = ButtonMatrixElement(name=b'Pads_With_Shift', rows=recursive_map(partial(with_modifier, self.shift_button), self.pads_raw))
        self.pads_with_zoom = ButtonMatrixElement(name=b'Pads_With_Zoom', rows=recursive_map(partial(with_modifier, self.zoom_button), self.pads_raw))
        self.encoders = ButtonMatrixElement(rows=[
         [ create_encoder(index + 14, (b'Encoder_{}').format(index)) for index in xrange(4)
         ]], name=b'Encoders')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/elements.pyc
