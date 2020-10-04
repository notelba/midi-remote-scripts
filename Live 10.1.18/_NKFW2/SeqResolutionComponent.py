# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SeqResolutionComponent.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from SpecialControl import RadioButtonGroup
from ShowMessageMixin import ShowMessageMixin
from consts import RESOLUTIONS, NO_TRIPLET_RESOLUTIONS, RESOLUTION_NAMES, NO_TRIPLET_RESOLUTION_NAMES, CLIP_GRID_RESOLUTIONS, NO_TRIPLET_CLIP_GRID_RESOLUTIONS, DEFAULT_RESOLUTION_INDEX, NO_TRIPLET_DEFAULT_RESOLUTION_INDEX
NUM_RESOLUTIONS = len(RESOLUTIONS)

class SeqResolutionComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ SeqResolutionComponent determines the resolution to be used for sequencing
    components. This needs to be extended to add controls for controlling the
    resolution. A standard implementation (StandardSeqResolutionComponent) is
    provided in this module. """
    __subject_events__ = ('resolution', )

    def __init__(self, name='Sequence_Resolution_Control', targets_comp=None, no_triplets=False, *a, **k):
        self._resolutions = NO_TRIPLET_RESOLUTIONS if no_triplets else RESOLUTIONS
        self._resolution_names = NO_TRIPLET_RESOLUTION_NAMES if no_triplets else RESOLUTION_NAMES
        self._grid_resolutions = NO_TRIPLET_CLIP_GRID_RESOLUTIONS if no_triplets else CLIP_GRID_RESOLUTIONS
        def_index = NO_TRIPLET_DEFAULT_RESOLUTION_INDEX if no_triplets else DEFAULT_RESOLUTION_INDEX
        self._resolution = self._resolutions[def_index]
        self._clip = None
        super(SeqResolutionComponent, self).__init__(name=name, *a, **k)
        self.set_clip.subject = targets_comp
        return

    def disconnect(self):
        super(SeqResolutionComponent, self).disconnect()
        self._resolutions = None
        self._resolution_names = None
        self._grid_resolutions = None
        self._clip = None
        return

    def _get_resolution(self):
        """ The sequence resolution to use. """
        return self._resolution

    def _set_resolution(self, res_index):
        """ Sets the resolution to use, updates clip grid resolution and
        notifies listeners. """
        assert res_index in xrange(len(self._resolutions))
        if self.is_enabled():
            self._resolution = self._resolutions[res_index]
            if self._clip:
                self._clip.view.grid_quantization = self._grid_resolutions[res_index]
                self._clip.view.grid_is_triplet = self.is_triplet
            self.notify_resolution(self._resolution)
            self.component_message('Sequence Resolution', self._resolution_names[res_index])

    resolution = property(_get_resolution, _set_resolution)

    @property
    def is_triplet(self):
        """ Returns whether the current resolution is a triplet resolution. """
        return 1.0 % self._resolution != 0.0

    @subject_slot('target_clip')
    def set_clip(self, clip):
        """ Sets the clip to use. This is only used for setting the clip's grid
        resolution on resolution changes. """
        self._clip = clip if clip and clip.is_midi_clip else None
        return


class StandardSeqResolutionComponent(SeqResolutionComponent):
    """ StandardSeqResolutionComponent is a SeqResolutionComponent set up to be
    controlled by a group of buttons.  If less than 5 buttons are used, triplet
    resolutions won't be available. """

    def __init__(self, num_buttons=NUM_RESOLUTIONS, cut_from_top=True, *a, **k):
        no_triplets = num_buttons < 5
        super(StandardSeqResolutionComponent, self).__init__(no_triplets=no_triplets, *a, **k)
        self._resolution_buttons = RadioButtonGroup(num_buttons, 0, True, checked_color='Sequence.Resolution.Selected', unchecked_color='Sequence.Resolution.NotSelected')
        self._offset = len(self._resolutions) - num_buttons if cut_from_top else 0
        self._resolution_buttons.set_checked_index(self._resolutions.index(self._resolution) - self._offset)
        self._on_resolution_button_value.subject = self._resolution_buttons

    def set_resolution_buttons(self, buttons):
        self._resolution_buttons.set_buttons(buttons)

    @subject_slot('checked_index')
    def _on_resolution_button_value(self, index):
        if self.is_enabled():
            self.resolution = index + self._offset
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SeqResolutionComponent.pyc
