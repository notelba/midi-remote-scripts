# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SessionRingComponent.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class SessionRingComponent(ControlSurfaceComponent):
    """ SessionRingComponent works with SlaveManager and handles showing/moving the
    session ring. This is meant to be used when standard session ring handling is not in
    use. It can be used with or without a master component. """

    def __init__(self, slave_manager, highlight_callback, width=8, height=1, show_by_default=True, should_follow_master=True, *a, **k):
        super(SessionRingComponent, self).__init__(*a, **k)
        self.is_private = True
        self._highlight_callback = highlight_callback
        self._width = width
        self._height = height
        self._should_follow_master = bool(should_follow_master)
        self._show_highlight = bool(show_by_default)
        self._track_list = None
        self._scene_list = None
        self._reassign_tracks.subject = slave_manager
        if not self._should_follow_master:
            self._refresh_track_list()
        self._refresh_scene_list()
        self._do_show_highlight()
        return

    def disconnect(self):
        super(SessionRingComponent, self).disconnect()
        self._highlight_callback = None
        self._track_list = None
        self._scene_list = None
        return

    def set_show_highlight(self, show):
        """ Sets whether to show the highlight. """
        self._show_highlight = bool(show)
        self._do_show_highlight()

    def set_should_follow_master(self, follow):
        """ Sets whether the highlight should follow the track offset of the master. """
        self._should_follow_master = follow
        if not self._should_follow_master:
            self._refresh_track_list()
        self._do_show_highlight()

    def set_dimensions(self, width, height):
        """ Sets the dimensions of the highlight. """
        self._width = width
        self._height = height
        self._do_show_highlight()

    @subject_slot('track_offset')
    def _reassign_tracks(self, offset):
        if self._should_follow_master:
            self._do_show_highlight(track_offset=offset)

    def on_track_list_changed(self):
        """ Extends standard to refresh internal track list when not following the
        master. """
        if not self._should_follow_master:
            self._refresh_track_list()
        super(SessionRingComponent, self).on_track_list_changed()

    def on_scene_list_changed(self):
        self._refresh_scene_list()

    def on_selected_track_changed(self):
        if not self._should_follow_master:
            self._do_show_highlight(track_offset=self._get_selected_track_index())

    def on_selected_scene_changed(self):
        self._do_show_highlight(scene_offset=self._get_selected_scene_index())

    def _do_show_highlight(self, track_offset=None, scene_offset=None):
        if self._show_highlight:
            if track_offset is None:
                if self._should_follow_master:
                    offset = self._reassign_tracks.subject.track_offset
                    track_offset = offset if offset >= 0 else 0
                else:
                    track_offset = self._get_selected_track_index()
            if scene_offset is None:
                scene_offset = self._get_selected_scene_index()
            self._highlight_callback(track_offset, scene_offset, self._width, self._height, True)
        else:
            self._highlight_callback(-1, -1, -1, -1, False)
        return

    def _get_selected_track_index(self):
        track = self.song().view.selected_track
        if track not in self._track_list:
            self._refresh_track_list()
        return self._track_list.index(track)

    def _get_selected_scene_index(self):
        scene = self.song().view.selected_scene
        if scene not in self._scene_list:
            self._refresh_scene_list()
        return self._scene_list.index(scene)

    def _refresh_track_list(self):
        self._track_list = list(tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (
         self.song().master_track,))

    def _refresh_scene_list(self):
        self._scene_list = list(self.song().scenes)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SessionRingComponent.pyc
