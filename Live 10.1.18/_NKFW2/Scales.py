# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\Scales.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.SubjectSlot import Subject
from PageSelector import Pageable

class Scales(Pageable):
    """ Scales is a Pageable object that allows scales to be selected. """

    def __init__(self, num_scale_select_buttons=None):
        super(Scales, self).__init__(num_scale_select_buttons or NUM_SCALES)

    @property
    def scale(self):
        """ The current Scale object. """
        return SCALE_TYPES[self._page_index]


class Scale(Subject):
    """ Scale is a simple object that stores the name and
    intervals of a musical scale. """
    __subject_events__ = ('intervals', 'name')

    def __init__(self, name, intervals, can_be_edited=False):
        super(Scale, self).__init__()
        self._intervals = intervals
        self._name = name
        self._can_be_edited = bool(can_be_edited)

    @property
    def can_be_edited(self):
        return self._can_be_edited

    def _get_intervals(self):
        return self._intervals

    def _set_intervals(self, intervals):
        """ Sets the intervals of the scale, which is only
        possible if the scale can_be_edited. """
        assert len(intervals) in range(128)
        if self._can_be_edited:
            self._intervals = intervals

    intervals = property(_get_intervals, _set_intervals)

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        """ Sets the name of the scale, which is only
        possible if the scale can_be_edited. """
        assert isinstance(name, (str, unicode))
        if self._can_be_edited:
            self._name = name

    name = property(_get_name, _set_name)


SCALE_TYPES = [
 Scale('Major', (0, 2, 4, 5, 7, 9, 11)),
 Scale('Minor', (0, 2, 3, 5, 7, 8, 10)),
 Scale('Dorian', (0, 2, 3, 5, 7, 9, 10)),
 Scale('Mixolydian', (0, 2, 4, 5, 7, 9, 10)),
 Scale('Lydian', (0, 2, 4, 6, 7, 9, 11)),
 Scale('Phrygian', (0, 1, 3, 5, 7, 8, 10)),
 Scale('Locrian', (0, 1, 3, 5, 6, 8, 10)),
 Scale('Diminished', (0, 1, 3, 4, 6, 7, 9, 10)),
 Scale('Whole-half', (0, 2, 3, 5, 6, 8, 9, 11)),
 Scale('Whole Tone', (0, 2, 4, 6, 8, 10)),
 Scale('Minor Blues', (0, 3, 5, 6, 7, 10)),
 Scale('Minor Pentatonic', (0, 3, 5, 7, 10)),
 Scale('Major Pentatonic', (0, 2, 4, 7, 9)),
 Scale('Harmonic Minor', (0, 2, 3, 5, 7, 8, 11)),
 Scale('Melodic Minor', (0, 2, 3, 5, 7, 9, 11)),
 Scale('Super Locrian', (0, 1, 3, 4, 6, 8, 10)),
 Scale('Bhairav', (0, 1, 4, 5, 7, 8, 11)),
 Scale('Hungarian Minor', (0, 2, 3, 6, 7, 8, 11)),
 Scale('Minor Gypsy', (0, 1, 4, 5, 7, 8, 10)),
 Scale('Hirojoshi', (0, 2, 3, 7, 8)),
 Scale('In-Sen', (0, 1, 5, 7, 10)),
 Scale('Iwato', (0, 1, 5, 6, 10)),
 Scale('Kumoi', (0, 2, 3, 7, 9)),
 Scale('Pelog', (0, 1, 3, 4, 7, 8)),
 Scale('Spanish', (0, 1, 3, 4, 5, 6, 8, 10))]
NUM_SCALES = len(SCALE_TYPES)
EDITABLE_SCALE = Scale('None', (), True)
CHROMATIC_SCALE = Scale('Chromatic', (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/Scales.pyc
