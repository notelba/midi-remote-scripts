# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\track_mixer_control_component.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import clamp, depends, listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import SimpleItemSlot
from ableton.v2.control_surface.control import control_list, ButtonControl, MappedSensitivitySettingControl
from pushbase.mixer_utils import has_pan_mode, is_set_to_split_stereo
from .item_lister import IconItemSlot
from .real_time_channel import RealTimeDataComponent
from .mixer_control_component import assign_parameters

class TrackMixerControlComponent(Component):
    __events__ = ('parameters', 'scroll_offset', 'items')
    BUTTON_SKIN = dict(color=b'TrackControlView.ButtonOff', pressed_color=b'TrackControlView.ButtonOn', disabled_color=b'TrackControlView.ButtonDisabled')
    controls = control_list(MappedSensitivitySettingControl)
    scroll_right_button = ButtonControl(**BUTTON_SKIN)
    scroll_left_button = ButtonControl(**BUTTON_SKIN)

    @depends(tracks_provider=None, real_time_mapper=None, register_real_time_data=None)
    def __init__(self, real_time_mapper=None, register_real_time_data=None, tracks_provider=None, *a, **k):
        assert liveobj_valid(real_time_mapper)
        assert tracks_provider is not None
        super(TrackMixerControlComponent, self).__init__(*a, **k)
        self._tracks_provider = tracks_provider
        self._on_return_tracks_changed.subject = self.song
        self.real_time_meter_channel = RealTimeDataComponent(parent=self, real_time_mapper=real_time_mapper, register_real_time_data=register_real_time_data, channel_type=b'meter')
        self._scroll_offset = 0
        self._items = []
        self._number_return_tracks = self._number_sends()
        self._update_scroll_buttons()
        self.__on_selected_item_changed.subject = self._tracks_provider
        self.__on_selected_item_changed()
        return

    def set_controls(self, controls):
        self.controls.set_control_element(controls)
        self._update_controls()

    @listens(b'panning_mode')
    def __on_pan_mode_changed(self):
        self._update_controls()
        self._update_scroll_offset()

    @listens(b'selected_item')
    def __on_selected_item_changed(self):
        self._update_scroll_offset()
        self._update_real_time_channel_id()
        mixer = self._tracks_provider.selected_item.mixer_device
        self.__on_pan_mode_changed.subject = mixer if has_pan_mode(mixer) else None
        self.__on_pan_mode_changed()
        return

    def update(self):
        super(TrackMixerControlComponent, self).update()
        if self.is_enabled():
            self._update_controls()
            self._update_scroll_buttons()
            self._update_real_time_channel_id()

    def _update_real_time_channel_id(self):
        self.real_time_meter_channel.set_data(self._tracks_provider.selected_item.mixer_device)

    def _update_controls(self):
        if self.is_enabled():
            assign_parameters(self.controls, self.parameters[self.scroll_offset:])
            self.notify_parameters()

    @property
    def parameters(self):
        return self._get_track_mixer_parameters()

    @property
    def scroll_offset(self):
        return self._scroll_offset

    @listens(b'return_tracks')
    def _on_return_tracks_changed(self):
        self._update_controls()
        self._update_scroll_offset()

    def _number_sends(self):
        mixable = self._tracks_provider.selected_item
        if mixable != self.song.master_track:
            return len(mixable.mixer_device.sends)
        return 0

    def _max_return_tracks(self):
        mixer = self._tracks_provider.selected_item.mixer_device
        if is_set_to_split_stereo(mixer):
            return 5
        return 6

    def _update_scroll_offset(self):
        new_number_return_tracks = self._number_sends()
        max_return_tracks = self._max_return_tracks()
        if max_return_tracks <= new_number_return_tracks < self._number_return_tracks and max_return_tracks + self._scroll_offset > new_number_return_tracks:
            delta = min(new_number_return_tracks - self._number_return_tracks, 0)
            self._scroll_controls(delta)
        elif new_number_return_tracks < max_return_tracks or self._tracks_provider.selected_item == self.song.master_track:
            self._scroll_offset = 0
        self._update_controls()
        self._update_scroll_buttons()
        self._number_return_tracks = new_number_return_tracks

    def _get_track_mixer_parameters(self):
        mixer_params = []
        if self._tracks_provider.selected_item:
            mixer = self._tracks_provider.selected_item.mixer_device
            mixer_params = [mixer.volume]
            if is_set_to_split_stereo(mixer):
                mixer_params += [mixer.left_split_stereo, mixer.right_split_stereo]
            else:
                mixer_params += [mixer.panning]
            mixer_params += list(mixer.sends)
        return mixer_params

    @scroll_right_button.pressed
    def scroll_right_button(self, button):
        self._scroll_controls(1)

    @scroll_left_button.pressed
    def scroll_left_button(self, button):
        self._scroll_controls(-1)

    def _update_scroll_buttons(self):
        if self.is_enabled():
            num_return_tracks = self._number_sends()
            self.scroll_right_button.enabled = num_return_tracks > self._max_return_tracks() + self._scroll_offset
            self.scroll_left_button.enabled = self._scroll_offset > 0
            self._update_view_slots()

    @property
    def items(self):
        return self._items

    def _update_view_slots(self):
        self._items = [ IconItemSlot() for _ in xrange(6) ]
        self._items.append(IconItemSlot(icon=b'page_left.svg' if self.scroll_left_button.enabled else b''))
        self._items.append(IconItemSlot(icon=b'page_right.svg' if self.scroll_right_button.enabled else b''))
        self.notify_items()

    def _scroll_controls(self, delta):
        num_return_tracks = self._number_sends()
        self._scroll_offset = clamp(self._scroll_offset + delta, 0, num_return_tracks if num_return_tracks > self._max_return_tracks() else 0)
        self.notify_scroll_offset()
        self._update_controls()
        self._update_scroll_buttons()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/track_mixer_control_component.pyc
