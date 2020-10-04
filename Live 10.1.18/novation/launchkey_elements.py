# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\launchkey_elements.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
SESSION_WIDTH = 8
SESSION_HEIGHT = 2
DRUM_CHANNEL = 9

@depends(skin=None)
def create_button(identifier, name, msg_type=MIDI_CC_TYPE, channel=15, **k):
    return ButtonElement(True, msg_type, channel, identifier, name=name, **k)


def create_encoder(identifier, name, **k):
    return EncoderElement(MIDI_CC_TYPE, 15, identifier, Live.MidiMap.MapMode.absolute, name=name, **k)


class LaunchkeyElements(object):

    def __init__(self, *a, **k):
        super(LaunchkeyElements, self).__init__(*a, **k)
        self.right_button = create_button(102, b'Right_Button')
        self.left_button = create_button(103, b'Left_Button')
        self.shift_button = create_button(108, b'Shift_Button', resource_type=PrioritizedResource, channel=0)
        self.play_button = create_button(115, b'Play_Button')
        self.record_button = create_button(117, b'Record_Button')
        self.scene_launch_buttons_raw = [
         create_button(104, b'Scene_Launch_Button', channel=0),
         create_button(105, b'Stop_Solo_Mute_Button', channel=0)]
        self.scene_launch_buttons = ButtonMatrixElement(rows=[
         self.scene_launch_buttons_raw], name=b'Scene_Launch_Buttons')
        self.clip_launch_matrix = ButtonMatrixElement(rows=[ [ create_button(offset + col_index, (b'{}_Clip_Launch_Button_{}').format(col_index, row_index), msg_type=MIDI_NOTE_TYPE, channel=0) for col_index in xrange(SESSION_WIDTH) ] for row_index, offset in enumerate(xrange(96, 119, 16))
                                                           ], name=b'Clip_Launch_Matrix')
        drum_pad_rows = (
         (48, 49, 50, 51),
         (44, 45, 46, 47),
         (40, 41, 42, 43),
         (36, 37, 38, 39))
        self.drum_pads = ButtonMatrixElement(rows=[ [ create_button(row_identifiers[col_index], (b'Drum_Pad_{}_{}').format(col_index, row_index), msg_type=MIDI_NOTE_TYPE, channel=DRUM_CHANNEL) for col_index in xrange(4) ] for row_index, row_identifiers in enumerate(drum_pad_rows)
                                                  ], name=b'Drum_Pads')
        self.pots = ButtonMatrixElement(rows=[
         [ create_encoder(index + 21, (b'Pot_{}').format(index)) for index in xrange(SESSION_WIDTH)
         ]], name=b'Pots')
        self.incontrol_mode_switch = create_button(12, b'InControl_Mode_Switch', msg_type=MIDI_NOTE_TYPE)
        self.pad_layout_switch = create_button(3, b'Pad_Layout_Switch')
        self.pot_layout_switch = create_button(9, b'Pot_Layout_Switch')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/launchkey_elements.pyc
