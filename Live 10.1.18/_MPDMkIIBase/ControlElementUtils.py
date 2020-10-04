# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MPDMkIIBase\ControlElementUtils.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.EncoderElement import EncoderElement
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement

def make_encoder(identifier, channel, name):
    return EncoderElement(MIDI_CC_TYPE, channel, identifier, Live.MidiMap.MapMode.absolute, name=name)


def make_slider(identifier, channel, name):
    return SliderElement(MIDI_CC_TYPE, channel, identifier, name=name)


def make_button(identifier, channel, name):
    return ButtonElement(True, MIDI_CC_TYPE, channel, identifier, name=name)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_MPDMkIIBase/ControlElementUtils.pyc
