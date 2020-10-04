# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\StandardNavComponent.py
# Compiled at: 2017-03-07 13:28:53
import Live
from _Framework.CompoundComponent import CompoundComponent
from _Framework.Dependency import depends
from _Framework.ScrollComponent import ScrollComponent, Scrollable
from _Framework.Util import in_range
from ControlUtils import skin_scroll_component, kill_scroll_tasks

class AbstractNav(Scrollable):
    """ Base class for horizontal and vertical scrollables. """

    @depends(song=None)
    def __init__(self, app, song=None, *a, **k):
        self._app_view = app.view
        super(AbstractNav, self).__init__(*a, **k)
        self._song = song

    def scroll_up(self):
        if self.can_scroll_up():
            self._do_nav(-1)

    def scroll_down(self):
        if self.can_scroll_down():
            self._do_nav(1)

    def can_scroll_up(self):
        return self._can_nav(-1)

    def can_scroll_down(self):
        return self._can_nav(1)

    def _do_nav(self, increment):
        raise NotImplementedError

    def _can_nav(self, increment):
        raise NotImplementedError


def can_nav_list(list_to_nav, current_selection, increment):
    """ Returns whether or not it's possible to navigate the given list from the given
    selection by the given increment. """
    try:
        return in_range(list(list_to_nav).index(current_selection) + increment, 0, len(list_to_nav))
    except ValueError:
        return False


def tracks(song):
    """ Returns the list of tracks to use. """
    return list(tuple(song.visible_tracks) + tuple(song.return_tracks) + (
     song.master_track,))


class HorizontalNav(AbstractNav):
    """ Horizontal navigation in either main view. """

    def _do_nav(self, increment):
        if increment > 0:
            self._app_view.scroll_view(Live.Application.Application.View.NavDirection.right, '', False)
        else:
            self._app_view.scroll_view(Live.Application.Application.View.NavDirection.left, '', False)

    def _can_nav(self, increment):
        if self._app_view.is_view_visible('Session'):
            return can_nav_list(tracks(self._song), self._song.view.selected_track, increment)
        else:
            return increment > 0 or self._song.current_song_time != 0.0


class VerticalNav(AbstractNav):
    """ Vertical navigation in either main view. """

    def _do_nav(self, increment):
        if increment > 0:
            self._app_view.scroll_view(Live.Application.Application.View.NavDirection.down, '', False)
        else:
            self._app_view.scroll_view(Live.Application.Application.View.NavDirection.up, '', False)

    def _can_nav(self, increment):
        if self._app_view.is_view_visible('Session'):
            return can_nav_list(self._song.scenes, self._song.view.selected_scene, increment)
        else:
            return can_nav_list(tracks(self._song), self._song.view.selected_track, increment)


class StandardNavComponent(CompoundComponent):
    """ StandardNavComponent manages horizontal and vertical navigation components. """

    def __init__(self, name='Standard_Navigation_Control', **k):
        super(StandardNavComponent, self).__init__(name=name)
        self._horizontal_nav = self.register_component(ScrollComponent(scrollable=HorizontalNav(self.application()), **k))
        self._vertical_nav = self.register_component(ScrollComponent(scrollable=VerticalNav(self.application()), **k))
        self.application().view.add_is_view_visible_listener('Session', self._on_main_view_changed)
        skin_scroll_component(self._horizontal_nav, color='Navigation.StandardEnabled')
        skin_scroll_component(self._vertical_nav, color='Navigation.StandardEnabled')

    def disconnect(self):
        listener = self._on_main_view_changed
        if self.application().view.is_view_visible_has_listener('Session', listener):
            self.application().view.remove_is_view_visible_listener('Session', listener)
        super(StandardNavComponent, self).disconnect()

    def set_up_button(self, button):
        kill_scroll_tasks((self._vertical_nav,))
        self._vertical_nav.set_scroll_up_button(button)

    def set_down_button(self, button):
        kill_scroll_tasks((self._vertical_nav,))
        self._vertical_nav.set_scroll_down_button(button)

    def set_left_button(self, button):
        kill_scroll_tasks((self._horizontal_nav,))
        self._horizontal_nav.set_scroll_up_button(button)

    def set_right_button(self, button):
        kill_scroll_tasks((self._horizontal_nav,))
        self._horizontal_nav.set_scroll_down_button(button)

    def on_track_list_changed(self):
        self._on_tracks_changed()

    def on_selected_track_changed(self):
        self._on_tracks_changed()

    def on_scene_list_changed(self):
        self._on_scenes_changed()

    def on_selected_scene_changed(self):
        self._on_scenes_changed()

    def update(self):
        super(StandardNavComponent, self).update()
        self._on_main_view_changed()

    def _on_tracks_changed(self):
        """ Updates the appropriate nav component for the current main view. """
        if self.is_enabled():
            view = self.application().view
            if view.is_view_visible('Session'):
                self._horizontal_nav.update()
            else:
                self._vertical_nav.update()

    def _on_scenes_changed(self):
        """ Updates the appropriate nav component for the current main view. """
        if self.is_enabled():
            view = self.application().view
            if view.is_view_visible('Session'):
                self._vertical_nav.update()

    def _on_main_view_changed(self):
        """ Updates both nav components upon main view changed. """
        if self.is_enabled():
            self._horizontal_nav.update()
            self._vertical_nav.update()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/StandardNavComponent.pyc
