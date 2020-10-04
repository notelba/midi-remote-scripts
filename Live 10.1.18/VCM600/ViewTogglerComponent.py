# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\ViewTogglerComponent.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement

class ViewTogglerComponent(ControlSurfaceComponent):
    """ Component that can toggle the device chain- and clip view of a number of tracks """

    def __init__(self, num_tracks):
        assert num_tracks > 0
        ControlSurfaceComponent.__init__(self)
        self._num_tracks = num_tracks
        self._chain_buttons = None
        self._clip_buttons = None
        self._ignore_track_selection = False
        self.application().view.add_is_view_visible_listener(b'Detail', self._on_detail_view_changed)
        self.application().view.add_is_view_visible_listener(b'Detail/Clip', self._on_views_changed)
        return

    def disconnect(self):
        self.application().view.remove_is_view_visible_listener(b'Detail', self._on_detail_view_changed)
        self.application().view.remove_is_view_visible_listener(b'Detail/Clip', self._on_views_changed)
        if self._chain_buttons != None:
            for button in self._chain_buttons:
                button.remove_value_listener(self._chain_value)

            self._chain_buttons = None
        if self._clip_buttons != None:
            for button in self._clip_buttons:
                button.remove_value_listener(self._clip_value)

            self._clip_buttons = None
        return

    def set_buttons(self, chain_buttons, clip_buttons):
        assert chain_buttons == None or isinstance(chain_buttons, tuple) and len(chain_buttons) == self._num_tracks
        assert clip_buttons == None or isinstance(clip_buttons, tuple) and len(clip_buttons) == self._num_tracks
        if self._chain_buttons != None:
            for button in self._chain_buttons:
                button.remove_value_listener(self._chain_value)

        self._chain_buttons = chain_buttons
        if self._chain_buttons != None:
            for button in self._chain_buttons:
                assert isinstance(button, ButtonElement)
                button.add_value_listener(self._chain_value, identify_sender=True)

        if self._clip_buttons != None:
            for button in self._clip_buttons:
                button.remove_value_listener(self._clip_value)

        self._clip_buttons = clip_buttons
        if self._clip_buttons != None:
            for button in self._clip_buttons:
                assert isinstance(button, ButtonElement)
                button.add_value_listener(self._clip_value, identify_sender=True)

        self.on_selected_track_changed()
        return

    def on_selected_track_changed(self):
        self._update_buttons()

    def on_enabled_changed(self):
        self.update()

    def update(self):
        super(ViewTogglerComponent, self).update()
        if self.is_enabled():
            self._update_buttons()
        else:
            if self._chain_buttons != None:
                for button in self._chain_buttons:
                    button.turn_off()

            if self._clip_buttons != None:
                for button in self._clip_buttons:
                    button.turn_off()

        return

    def _on_detail_view_changed(self):
        self._update_buttons()

    def _on_views_changed(self):
        self._update_buttons()

    def _update_buttons(self):
        tracks = self.song().visible_tracks
        for index in range(self._num_tracks):
            if len(tracks) > index and tracks[index] == self.song().view.selected_track and self.application().view.is_view_visible(b'Detail'):
                if self.application().view.is_view_visible(b'Detail/DeviceChain'):
                    self._chain_buttons[index].turn_on()
                else:
                    self._chain_buttons[index].turn_off()
                if self.application().view.is_view_visible(b'Detail/Clip'):
                    self._clip_buttons[index].turn_on()
                else:
                    self._clip_buttons[index].turn_off()
            else:
                if self._chain_buttons != None:
                    self._chain_buttons[index].turn_off()
                if self._clip_buttons != None:
                    self._clip_buttons[index].turn_off()

        return

    def _chain_value(self, value, sender):
        assert sender in self._chain_buttons
        tracks = self.song().visible_tracks
        if not sender.is_momentary() or value != 0:
            index = list(self._chain_buttons).index(sender)
            self._ignore_track_selection = True
            if len(tracks) > index:
                if self.song().view.selected_track != tracks[index]:
                    self.song().view.selected_track = tracks[index]
                    if not self.application().view.is_view_visible(b'Detail') or not self.application().view.is_view_visible(b'Detail/DeviceChain'):
                        self.application().view.show_view(b'Detail')
                        self.application().view.show_view(b'Detail/DeviceChain')
                elif self.application().view.is_view_visible(b'Detail/DeviceChain') and self.application().view.is_view_visible(b'Detail'):
                    self.application().view.hide_view(b'Detail')
                else:
                    self.application().view.show_view(b'Detail')
                    self.application().view.show_view(b'Detail/DeviceChain')
            self._ignore_track_selection = False

    def _clip_value(self, value, sender):
        assert sender in self._clip_buttons
        tracks = self.song().visible_tracks
        if not sender.is_momentary() or value != 0:
            index = list(self._clip_buttons).index(sender)
            self._ignore_track_selection = True
            if len(tracks) > index:
                if self.song().view.selected_track != tracks[index]:
                    self.song().view.selected_track = tracks[index]
                    if not self.application().view.is_view_visible(b'Detail') or not self.application().view.is_view_visible(b'Detail/Clip'):
                        self.application().view.show_view(b'Detail')
                        self.application().view.show_view(b'Detail/Clip')
                elif self.application().view.is_view_visible(b'Detail/Clip') and self.application().view.is_view_visible(b'Detail'):
                    self.application().view.hide_view(b'Detail')
                else:
                    self.application().view.show_view(b'Detail')
                    self.application().view.show_view(b'Detail/Clip')
            self._ignore_track_selection = False
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/VCM600/ViewTogglerComponent.pyc
