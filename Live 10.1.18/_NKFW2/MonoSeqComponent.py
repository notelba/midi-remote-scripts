# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\MonoSeqComponent.py
# Compiled at: 2017-09-30 15:26:23
from itertools import chain, starmap
from StepSeqComponentBase import StepSeqComponentBase
from PlayheadComponent import PlayheadComponent
from NoteLaneComponent import NoteLaneComponent

class MonoSeqComponent(StepSeqComponentBase):
    """ MonoSeqComponent allows for sequencing a single note lane at a time. This manages
    all of the necessary sequence-related components for this. """

    def __init__(self, matrix_raw, num_steps, num_rows, row_width, channels, res_comp, velo_comp=None, targets_comp=None, should_enumerate=False, playhead_offsets=(0, 0), prefer_playing_clip=False, name='Mono_Sequence_Control', *a, **k):
        super(MonoSeqComponent, self).__init__(num_steps, res_comp, targets_comp=targets_comp, prefer_playing_clip=prefer_playing_clip, name=name, *a, **k)
        if prefer_playing_clip:
            targets_comp = None
        notes, t_notes = self._create_playhead_notes(matrix_raw, num_rows, row_width, playhead_offsets, should_enumerate)
        self._playhead_component = self.register_component(PlayheadComponent(res_comp, self._page_component, notes=notes, triplet_notes=t_notes, feedback_channels=channels, targets_comp=targets_comp))
        self._note_lane_components = self.register_components(*[
         NoteLaneComponent(num_steps, row_width, channel=channels[0], enumerate_ids=should_enumerate, resolution_comp=res_comp, page_comp=self._page_component, velo_comp=velo_comp, targets_comp=targets_comp, use_odd_colors=True)])
        return

    def set_note_component(self, component):
        """ Sets the component to use for determining the note to sequence. The component
        must have an observable selected_note property. """
        self._note_lane_components[0].set_note_component(component)

    def set_sequence_buttons(self, buttons):
        """ Sets the buttons to use for sequencing. """
        self._note_lane_components[0].set_sequence_buttons(buttons)

    @staticmethod
    def _create_playhead_notes(matrix, num_rows, row_width, offsets, should_enumerate):
        if should_enumerate:
            row_start_notes = [ i * row_width for i in xrange(num_rows) ]
            row_end_notes = [ i * row_width + row_width for i in xrange(num_rows) ]
            triplet_end_notes = [ i * row_width + row_width - 1 for i in xrange(num_rows) ]
        else:
            row_start_notes = [ matrix[(i + offsets[0])][(0 + offsets[1])].message_identifier() for i in xrange(num_rows) ]
            row_end_notes = [ matrix[(i + offsets[0])][(-1)].message_identifier() + 1 for i in xrange(num_rows)
                            ]
            triplet_end_notes = [ matrix[(i + offsets[0])][(-1)].message_identifier() - 1 for i in xrange(num_rows)
                                ]
        notes = chain(*starmap(range, [ [row_start_notes[i], row_end_notes[i]] for i in xrange(num_rows)
                                      ]))
        triplet_notes = chain(*starmap(range, [ [row_start_notes[i], triplet_end_notes[i]] for i in xrange(num_rows)
                                              ]))
        return (notes, triplet_notes)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/MonoSeqComponent.pyc
