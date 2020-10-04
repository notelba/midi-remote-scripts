# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClyphXProSnapComponent.py
# Compiled at: 2018-01-15 18:16:49
from _Framework.SubjectSlot import subject_slot
from ClyphXSnapBaseComponent import ClyphXSnapBaseComponent, TracksToSnap
from consts import ASCII_A
from ClyphX_Pro.clyphx_pro.consts import DATA_HEADER

class ClyphXProSnapComponent(ClyphXSnapBaseComponent):
    """ Snap component for ClyphX Pro. """

    def __init__(self, *a, **k):
        super(ClyphXProSnapComponent, self).__init__(*a, **k)
        self._on_song_data_changed.subject = self._song

    def set_clyphx_instance(self, instance):
        self._snap_component = instance

    def get_initial_snap_data(self, num_buttons):
        d = []
        for i in xrange(num_buttons):
            header = '%s - %s' % (self._header, i)
            ident = DATA_HEADER % header
            d.append(self._song.get_data(ident, None) is not None)

        return d

    def delete_snap(self, snap, btn_id):
        if snap:
            header = '%s - %s' % (self._header, btn_id)
            self._song.set_data(DATA_HEADER % header, None)
        current = self.song().master_track.mixer_device.cue_volume.value
        self._song.master_track.mixer_device.cue_volume.value = 0.0
        self._song.master_track.mixer_device.cue_volume.value = 1.0
        self._song.master_track.mixer_device.cue_volume.value = current
        return

    def store_or_recall_snap(self, snap, btn_id):
        ident = '[%s - %s]' % (self._header, btn_id)
        if snap:
            self._snap_component.trigger_action_list('%s %s' % (ident, self._recall_args))
        else:
            track_spec = self._get_track_spec_to_snap()
            action = '%s %sSNAP %s' % (ident, track_spec, self._snap_args)
            self._snap_component.trigger_action_list(action)

    def button_has_snap(self, btn_id):
        return self._snap_data[btn_id]

    def _get_track_spec_to_snap(self):
        if self._tracks_to_snap == TracksToSnap.CURRENT:
            current = self._targets_comp.target_track
            if current in self._song.tracks:
                return '%s/' % (list(self._song.tracks).index(current) + 1)
            if current in self._song.return_tracks:
                idx = list(self._song.return_tracks).index(current)
                return '%s/' % chr(idx + ASCII_A)
            return 'MST/'
        return 'ALL/'

    @subject_slot('data')
    def _on_song_data_changed(self):
        self._snap_data = self.get_initial_snap_data(self._num_snaps)
        self._update_snap_buttons()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClyphXProSnapComponent.pyc
