# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Code_Series\element_utils.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE
from ableton.v2.control_surface.elements import ButtonElement, EncoderElement, SliderElement
IS_MOMENTARY = True
CHANNEL = 0

@depends(skin=None)
def make_button(identifier, name, **k):
    return ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, CHANNEL, identifier, name=name, **k)


def make_slider(channel, name):
    return SliderElement(MIDI_PB_TYPE, channel, 0, name=name)


def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.relative_smooth_signed_bit, name=name)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Code_Series/element_utils.pyc
