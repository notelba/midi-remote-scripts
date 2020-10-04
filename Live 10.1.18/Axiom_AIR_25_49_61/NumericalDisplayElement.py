# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\NumericalDisplayElement.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from .NumericalDisplaySegment import NumericalDisplaySegment

class NumericalDisplayElement(PhysicalDisplayElement):
    """ Special display element that only displays numerical values """
    _ascii_translations = {b'0': 48, 
       b'1': 49, 
       b'2': 50, 
       b'3': 51, 
       b'4': 52, 
       b'5': 53, 
       b'6': 54, 
       b'7': 55, 
       b'8': 56, 
       b'9': 57}

    def __init__(self, width_in_chars, num_segments):
        PhysicalDisplayElement.__init__(self, width_in_chars, num_segments)
        self._logical_segments = []
        self._translation_table = NumericalDisplayElement._ascii_translations
        width_without_delimiters = self._width - num_segments + 1
        width_per_segment = int(width_without_delimiters / num_segments)
        for index in range(num_segments):
            new_segment = NumericalDisplaySegment(width_per_segment, self.update)
            self._logical_segments.append(new_segment)

    def display_message(self, message):
        if not self._message_header != None:
            raise AssertionError
            assert message != None
            assert isinstance(message, str)
            message = self._block_messages or NumericalDisplaySegment.adjust_string(message, self._width)
            self.send_midi(self._message_header + tuple([ self._translate_char(c) for c in message ]) + self._message_tail)
        return

    def _translate_char(self, char_to_translate):
        assert char_to_translate != None
        assert isinstance(char_to_translate, str) or isinstance(char_to_translate, unicode)
        assert len(char_to_translate) == 1
        if char_to_translate in self._translation_table.keys():
            result = self._translation_table[char_to_translate]
        else:
            result = self._translation_table[b'0']
        return result
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_AIR_25_49_61/NumericalDisplayElement.pyc
