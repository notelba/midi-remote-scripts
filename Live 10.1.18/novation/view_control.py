# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\view_control.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, ObservablePropertyAlias, clamp, index_if, listens
from ableton.v2.control_surface.components import BasicSceneScroller, BasicTrackScroller, ScrollComponent, ViewControlComponent, all_tracks
from .util import skin_scroll_buttons

class NotifyingTrackScroller(BasicTrackScroller, EventObject):
    __events__ = ('scrolled', )

    def _do_scroll(self, delta):
        super(NotifyingTrackScroller, self)._do_scroll(delta)
        self.notify_scrolled()


class NotifyingTrackPager(NotifyingTrackScroller):

    def __init__(self, track_provider=None, *a, **k):
        super(NotifyingTrackPager, self).__init__(*a, **k)
        assert track_provider is not None
        self._track_provider = track_provider
        return

    def _do_scroll(self, delta):
        selected_track = self._song.view.selected_track
        tracks = all_tracks(self._song)
        selected_track_index = index_if(lambda t: t == selected_track, tracks)
        len_tracks = len(tracks)
        new_index = selected_track_index + delta * self._track_provider.num_tracks
        self._song.view.selected_track = tracks[clamp(new_index, 0, len_tracks - 1)]
        self.notify_scrolled()


class NotifyingViewControlComponent(ViewControlComponent):
    __events__ = ('selection_scrolled', 'selection_paged')

    def __init__(self, track_provider=None, enable_skinning=True, *a, **k):
        self._track_provider = track_provider
        super(NotifyingViewControlComponent, self).__init__(*a, **k)
        self._page_tracks = ScrollComponent(self._create_track_pager(), parent=self)
        self.__on_tracks_changed.subject = self._track_provider
        self.__on_selected_track_changed.subject = self.song.view
        if enable_skinning:
            skin_scroll_buttons(self._page_tracks, b'TrackNavigation.On', b'TrackNavigation.Pressed')
            skin_scroll_buttons(self._scroll_tracks, b'TrackNavigation.On', b'TrackNavigation.Pressed')
            skin_scroll_buttons(self._scroll_scenes, b'SceneNavigation.On', b'SceneNavigation.Pressed')

    def set_prev_track_page_button(self, button):
        self._page_tracks.set_scroll_up_button(button)

    def set_next_track_page_button(self, button):
        self._page_tracks.set_scroll_down_button(button)

    def _create_track_scroller(self):
        scroller = NotifyingTrackScroller()
        self.register_disconnectable(ObservablePropertyAlias(self, property_host=scroller, property_name=b'scrolled', alias_name=b'selection_scrolled'))
        return scroller

    def _create_scene_scroller(self):
        return BasicSceneScroller()

    def _create_track_pager(self):
        pager = NotifyingTrackPager(track_provider=self._track_provider)
        self.register_disconnectable(ObservablePropertyAlias(self, property_host=pager, property_name=b'scrolled', alias_name=b'selection_paged'))
        return pager

    @listens(b'tracks')
    def __on_tracks_changed(self):
        self._update_track_scrollers()

    @listens(b'selected_track')
    def __on_selected_track_changed(self):
        self._update_track_scrollers()

    def _update_track_scrollers(self):
        self._scroll_tracks.update()
        self._page_tracks.update()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/view_control.pyc
