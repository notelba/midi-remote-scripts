# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\MidiMap.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .ButtonMatrixElement import ButtonMatrixElement
from .ButtonElement import ButtonElement
from .EncoderElement import EncoderElement
from .SliderElement import SliderElement

def make_button(name, channel, number, midi_message_type):
    is_momentary = True
    return ButtonElement(not is_momentary, midi_message_type, channel, number, name=name)


def make_slider(name, channel, number, midi_message_type):
    return SliderElement(midi_message_type, channel, number, name=name)


def make_encoder(name, channel, number, midi_message_type):
    return EncoderElement(midi_message_type, channel, number, Live.MidiMap.MapMode.absolute, name=name)


class MidiMap(dict):

    def add_button(self, name, channel, number, midi_message_type):
        assert name not in self.keys()
        self[name] = make_button(name, channel, number, midi_message_type)

    def add_matrix(self, name, element_factory, channel, numbers, midi_message_type):
        assert name not in self.keys()

        def one_dimensional_name(base_name, x, _y):
            return b'%s[%d]' % (base_name, x)

        def two_dimensional_name(base_name, x, y):
            return b'%s[%d,%d]' % (base_name, x, y)

        name_factory = two_dimensional_name if len(numbers) > 1 else one_dimensional_name
        elements = [ [ element_factory(name_factory(name, column, row), channel, identifier, midi_message_type) for column, identifier in enumerate(identifiers) ] for row, identifiers in enumerate(numbers)
                   ]
        self[name] = ButtonMatrixElement(rows=elements)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Framework/MidiMap.pyc
