# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\ControlElementUtils.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import Live
from _Framework.Dependency import depends
from _Framework.Resource import PrioritizedResource
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.SliderElement import SliderElement
from _Framework.ComboElement import ComboElement
from .consts import STANDARD_CHANNEL

@depends(skin=None)
def make_button(identifier, msg_type=MIDI_NOTE_TYPE, is_momentary=True, skin=None, is_modifier=False, name=b''):
    return ButtonElement(is_momentary, msg_type, STANDARD_CHANNEL, identifier, skin=skin, name=name, resource_type=PrioritizedResource if is_modifier else None)


def make_encoder(identifier, name=b''):
    return EncoderElement(MIDI_CC_TYPE, STANDARD_CHANNEL, identifier, Live.MidiMap.MapMode.absolute, name=name)


def make_slider(identifier, name=b'', channel=STANDARD_CHANNEL):
    return SliderElement(MIDI_CC_TYPE, channel, identifier, name=name)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_MK2/ControlElementUtils.pyc
