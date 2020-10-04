# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\clip_actions.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import duplicate_clip_loop, listens, liveobj_valid
from ...control_surface import Component
from ...control_surface.control import ButtonControl

class ClipActionsComponent(Component):
    delete_button = ButtonControl(color=b'Action.Available')
    duplicate_button = ButtonControl(color=b'Action.Available')
    double_loop_button = ButtonControl(color=b'Action.Available')

    def __init__(self, *a, **k):
        super(ClipActionsComponent, self).__init__(*a, **k)
        view = self.song.view
        self.__on_selected_scene_changed.subject = view
        self.__on_selected_track_changed.subject = view
        self.__on_selected_track_changed()

    @property
    def clip_slot(self):
        return self.song.view.highlighted_clip_slot

    @delete_button.released
    def delete_button(self, _):
        self.clip_slot.delete_clip()

    @duplicate_button.pressed
    def duplicate_button(self, _):
        clip_slot = self.clip_slot
        view = self.song.view
        track = view.selected_track
        try:
            source_index = list(track.clip_slots).index(clip_slot)
            target_index = track.duplicate_clip_slot(source_index)
            view.highlighted_clip_slot = track.clip_slots[target_index]
            view.detail_clip = view.highlighted_clip_slot.clip
            if clip_slot.clip.is_playing:
                view.highlighted_clip_slot.fire(force_legato=True, launch_quantization=Live.Song.Quantization.q_no_q)
        except (Live.Base.LimitationError, RuntimeError):
            pass

    @double_loop_button.pressed
    def double_loop_button(self, _):
        duplicate_clip_loop(self.clip_slot.clip)

    @listens(b'selected_scene')
    def __on_selected_scene_changed(self):
        self._update_clip_slot()

    @listens(b'selected_track')
    def __on_selected_track_changed(self):
        self.__on_input_routing_type_changed.subject = self.song.view.selected_track
        self._update_clip_slot()

    @listens(b'input_routing_type')
    def __on_input_routing_type_changed(self):
        self._update_action_buttons()

    @listens(b'has_clip')
    def __on_has_clip_changed(self):
        self._update_action_buttons()

    def _update_clip_slot(self):
        self.__on_has_clip_changed.subject = self.song.view.highlighted_clip_slot
        self.__on_has_clip_changed()

    def _update_action_buttons(self):
        can_perform_clip_action = self._can_perform_clip_action()
        self.delete_button.enabled = can_perform_clip_action
        self.duplicate_button.enabled = can_perform_clip_action
        self.double_loop_button.enabled = can_perform_clip_action and self.clip_slot.clip.is_midi_clip

    def _can_perform_clip_action(self):
        clip_slot = self.clip_slot
        return liveobj_valid(clip_slot) and clip_slot.has_clip
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/components/clip_actions.pyc
