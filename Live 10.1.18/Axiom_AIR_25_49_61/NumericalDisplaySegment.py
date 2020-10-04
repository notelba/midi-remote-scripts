# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\NumericalDisplaySegment.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.LogicalDisplaySegment import LogicalDisplaySegment

class NumericalDisplaySegment(LogicalDisplaySegment):
    """ Special display segment that only displays numerical values """

    @staticmethod
    def adjust_string(original, length):
        characters_to_retain = {b'0': 48, 
           b'1': 49, 
           b'2': 50, 
           b'3': 51, 
           b'4': 52, 
           b'5': 53, 
           b'6': 54, 
           b'7': 55, 
           b'8': 56, 
           b'9': 57}
        resulting_string = b''
        for char in original:
            if char in characters_to_retain:
                resulting_string = resulting_string + char

        if len(resulting_string) > length:
            resulting_string = resulting_string[:length]
        if len(resulting_string) < length:
            resulting_string = resulting_string.rjust(length)
        return resulting_string

    def __init__(self, width, update_callback):
        LogicalDisplaySegment.__init__(self, width, update_callback)

    def display_string(self):
        resulting_string = b' ' * self._width
        if self._data_source != None:
            resulting_string = NumericalDisplaySegment.adjust_string(self._data_source.display_string(), self._width)
        return resulting_string
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_AIR_25_49_61/NumericalDisplaySegment.pyc
