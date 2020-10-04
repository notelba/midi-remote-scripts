# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\PolySeqComponent.py
# Compiled at: 2017-09-30 15:26:23
from functools import partial
from StepSeqComponentBase import StepSeqComponentBase
from PlayheadComponent import PlayheadComponent
from NoteLaneComponent import NoteLaneComponent

class PolySeqComponent(StepSeqComponentBase):
    """ PolySeqComponent allows for sequencing multiple note lanes at a time. This manages
    all of the necessary sequence-related components for this. """

    def __init__(self, num_steps, num_rows, row_width, channels, res_comp, invert_rows=True, velo_comp=None, targets_comp=None, prefer_playing_clip=False, name='Poly_Sequence_Control', *a, **k):
        super(PolySeqComponent, self).__init__(num_steps, res_comp, targets_comp=targets_comp, prefer_playing_clip=prefer_playing_clip, name=name, *a, **k)
        if prefer_playing_clip:
            targets_comp = None
        self._playhead_component = self.register_component(PlayheadComponent(res_comp, self._page_component, feedback_channels=channels, targets_comp=targets_comp))
        self._note_lane_components = self.register_components(*[ NoteLaneComponent(num_steps, row_width, note=36 + i, channel=channels[i], enumerate_ids=True, resolution_comp=res_comp, page_comp=self._page_component, velo_comp=velo_comp, targets_comp=targets_comp, use_odd_colors=i % 2 == 0) for i in xrange(num_rows)
                                                               ])
        self._num_note_lanes = num_rows
        self._invert_rows = bool(invert_rows)
        return

    def __getattr__(self, name):
        """ Override to extract note lane component index to set buttons for. """
        if name.startswith('set_sequence_buttons_'):
            return partial(self._set_sequence_buttons, int(name[(-1)]))

    def _set_sequence_buttons(self, index, buttons):
        assert index in xrange(self._num_note_lanes)
        if self._invert_rows:
            index = self._num_note_lanes - 1 - index
        self._note_lane_components[index].set_sequence_buttons(buttons)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/PolySeqComponent.pyc
