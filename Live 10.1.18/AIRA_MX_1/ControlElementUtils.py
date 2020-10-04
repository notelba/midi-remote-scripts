# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AIRA_MX_1\ControlElementUtils.py
# Compiled at: 2020-07-31 16:19:16
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Resource import PrioritizedResource
from _Framework.Dependency import depends
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE
from _Framework.ComboElement import ComboElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement

@depends(skin=None)
def make_button(name, identifier, channel=0, msg_type=MIDI_NOTE_TYPE, is_momentary=True, is_modifier=False, skin=None):
    return ButtonElement(is_momentary, msg_type, channel, identifier, name=name, resource_type=PrioritizedResource if is_modifier else None, skin=skin)


def make_encoder(name, identifier, channel=0):
    return EncoderElement(MIDI_CC_TYPE, channel, identifier, Live.MidiMap.MapMode.absolute, name=name)


def with_modifier(control, modifier):
    return ComboElement(control, modifiers=[
     modifier], name=control.name + b'_With_Modifier')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/AIRA_MX_1/ControlElementUtils.pyc
