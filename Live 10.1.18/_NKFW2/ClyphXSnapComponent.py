# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClyphXSnapComponent.py
# Compiled at: 2018-01-15 18:16:49
from ClyphXSnapBaseComponent import ClyphXSnapBaseComponent, TracksToSnap

class ClyphXSnapComponent(ClyphXSnapBaseComponent):
    """ Snap component for ClyphX that allows snap data to be persisted. """

    def __init__(self, *a, **k):
        super(ClyphXSnapComponent, self).__init__(*a, **k)
        self._rebuild_data = None
        return

    def disconnect(self):
        super(ClyphXSnapComponent, self).disconnect()
        self._rebuild_data = None
        return

    def set_clyphx_instance(self, instance):
        """ Sets the ClyphX instance to use (or None) and locates is snap component. """
        self._snap_component = None
        if instance is not None:
            for c in instance.components:
                c_name = c.__class__.__name__
                if c_name == 'ClyphXSnapActions':
                    self._snap_component = c
                    break

        return

    def get_initial_snap_data(self, num_buttons):
        return [ SnapData() for _ in xrange(num_buttons) ]

    def rebuild(self, data):
        """ Rebuilds snap data based on the given data list. """
        if self.is_enabled():
            if len(data) == self._num_snaps:
                for i, d in enumerate(data):
                    self._snap_data[i].name = d

            self._update_snap_buttons()
            self._rebuild_data = None
        else:
            self._rebuild_data = data
        return

    def delete_snap(self, snap, _):
        snap.name = None
        self._update_snap_buttons()
        self._notify_snap_data()
        return

    def store_or_recall_snap(self, snap, btn_id):
        if snap.name is not None:
            self._snap_component.recall_track_snapshot('', snap, disable_smooth=True)
        else:
            t_list = self._get_tracks_to_snap()
            self._snap_component.store_track_snapshot(t_list, snap, '[]', 'SNAP', self._snap_args, force=True)
            if self._snap_data[btn_id].name is None:
                self.component_message('SNAP ERROR', 'Too many parameters to store!')
            self._update_snap_buttons()
            self._notify_snap_data()
        return

    def button_has_snap(self, btn_id):
        return self._snap_data[btn_id].name is not None

    def _notify_snap_data(self):
        data = [ s.name for s in self._snap_data ]
        self.notify_snap_data(data)

    def _get_tracks_to_snap(self):
        if self._targets_comp and self._tracks_to_snap == TracksToSnap.CURRENT:
            return [self._targets_comp.target_track]
        return list(tuple(self.song().tracks) + tuple(self.song().return_tracks) + (
         self.song().master_track,))

    def update(self):
        super(ClyphXSnapComponent, self).update()
        if self.is_enabled() and self._rebuild_data:
            self.rebuild(self._rebuild_data)


class SnapData(object):
    """ Simple object that stores ClyphX Snap data. """

    def __init__(self):
        self._data = None
        return

    def _set_name(self, data):
        self._data = None
        if data and data.startswith('[] || ('):
            self._data = data
        return

    def _get_name(self):
        return self._data

    name = property(_get_name, _set_name)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClyphXSnapComponent.pyc
