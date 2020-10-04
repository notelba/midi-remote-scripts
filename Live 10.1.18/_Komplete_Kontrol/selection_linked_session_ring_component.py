# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\selection_linked_session_ring_component.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import SessionRingComponent

class SelectionLinkedSessionRingComponent(SessionRingComponent):

    def __init__(self, *a, **k):
        super(SelectionLinkedSessionRingComponent, self).__init__(*a, **k)
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()

    @listens(b'selected_track')
    def __on_selected_track_changed(self):
        selected_track = self.song.view.selected_track
        if selected_track not in self.controlled_tracks():
            all_tracks = list(self.tracks_to_use())
            self.track_offset = all_tracks.index(selected_track)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Komplete_Kontrol/selection_linked_session_ring_component.pyc
