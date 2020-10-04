# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackNameManager.py
# Compiled at: 2017-04-24 12:52:36
from itertools import count
from _Framework.SubjectSlot import SlotManager, subject_slot_group

class TrackNameManager(SlotManager):
    """ TrackNameManager handles displaying track names served via the channel strips
    of a SpecialMixerComponent. """

    def __init__(self, *a, **k):
        super(TrackNameManager, self).__init__(*a, **k)
        self._display_line = None
        self._channel_strips = None
        return

    def disconnect(self):
        super(TrackNameManager, self).disconnect()
        self._display_line = None
        self._channel_strips = None
        return

    def set_display_line(self, line):
        """ Sets the display line to use for showing track names. """
        self._display_line = line
        if line and self._channel_strips:
            self.update()

    def set_mixer_component(self, mixer):
        """ Sets the SpecialMixerComponent that is the source for track names. """
        self._channel_strips = mixer.channel_strips() if mixer else []
        self._on_track_name_changed.replace_subjects(self._channel_strips, count())
        if mixer and self._display_line:
            self.update()

    def update(self):
        if self._display_line and self._channel_strips:
            for s in self._channel_strips:
                s.update_track_name_data_source()

    @subject_slot_group('track_name')
    def _on_track_name_changed(self, name, is_selected, index):
        if self._display_line:
            self._update_track_name_display(name, is_selected, index)

    def _update_track_name_display(self, name, is_selected, index):
        raise NotImplementedError
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackNameManager.pyc
