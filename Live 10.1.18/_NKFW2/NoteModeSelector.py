# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\NoteModeSelector.py
# Compiled at: 2017-03-07 13:28:52
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class NoteModeSelector(ControlSurfaceComponent):
    """ NoteModeSelector works with the TargetsComponent to select
    the note mode to use based on the contents of the target track. """
    __subject_events__ = ('note_mode', )

    def __init__(self, targets_comp, *a, **k):
        self.is_private = True
        self._targets = targets_comp
        self._mode = ''
        super(NoteModeSelector, self).__init__(*a, **k)
        self._on_target_drum_rack_changed.subject = targets_comp
        self._on_target_simpler_changed.subject = targets_comp
        self._select_note_mode()

    def disconnect(self):
        super(NoteModeSelector, self).disconnect()
        self._targets = None
        self._mode = None
        return

    @property
    def note_mode(self):
        """ The name of note mode to use. """
        return self._mode

    def _select_note_mode(self):
        mode = 'scale'
        if self._targets.target_drum_rack:
            mode = 'drum_rack'
        elif self._is_slicing():
            mode = 'simpler'
        if self._mode != mode:
            self._mode = mode
            self._tasks.add(self._notify)

    def _notify(self, _=None):
        """ This is triggered via a task to avoid cases where other components listening
        to these targets is notified after this component. """
        self.notify_note_mode(self._mode)

    @subject_slot('target_drum_rack')
    def _on_target_drum_rack_changed(self, _):
        self._select_note_mode()

    @subject_slot('target_simpler')
    def _on_target_simpler_changed(self, simpler):
        self._on_sample_changed.subject = simpler or None
        self._on_playback_mode_changed.subject = simpler or None
        self._select_note_mode()
        return

    @subject_slot('sample')
    def _on_sample_changed(self):
        self._select_note_mode()

    @subject_slot('playback_mode')
    def _on_playback_mode_changed(self):
        self._select_note_mode()

    def _is_slicing(self):
        simpler = self._targets.target_simpler
        return simpler is not None and simpler.sample and simpler.playback_mode == Live.SimplerDevice.PlaybackMode.slicing
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/NoteModeSelector.pyc
