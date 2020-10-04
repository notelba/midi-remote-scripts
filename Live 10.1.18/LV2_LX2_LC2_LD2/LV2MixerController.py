# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV2_LX2_LC2_LD2\LV2MixerController.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .ParamMap import ParamMap
from .FaderfoxMixerController import FaderfoxMixerController
from .consts import *

class LV2MixerController(FaderfoxMixerController):
    """Mixer parameters of LX2"""
    __module__ = __name__
    __filter_funcs__ = [
     b'update_display', b'log']

    def __init__(self, parent):
        LV2MixerController.realinit(self, parent)

    def realinit(self, parent):
        FaderfoxMixerController.realinit(self, parent)
        self.reset_status_cache()
        self.parent.song().add_tracks_listener(self.on_tracks_added_or_deleted)
        self.tracks_with_listener = []

    def reset_status_cache(self):
        self.status_cache = {b'mute': [ -1 for i in range(0, 12) ], b'solo': [ -1 for i in range(0, 12) ], b'arm': [ -1 for i in range(0, 12) ], b'current_monitoring_state': [ -1 for i in range(0, 12) ], b'master': {b'solo': -1, b'mute': -1, b'arm': -1}, b'master_note': {b'solo': MASTER_SOLO_NOTE, 
                            b'mute': MASTER_MUTE_NOTE, 
                            b'arm': MASTER_ARM_NOTE}}
        self.set_tracks_arm_status()
        self.set_tracks_mute_status()
        self.set_tracks_solo_status()
        self.set_tracks_monitoring_status()

    def remove_track_listeners(self):
        for track in self.tracks_with_listener:
            if track:
                if track.can_be_armed:
                    track.remove_arm_listener(self.on_track_arm_changed)
                track.remove_mute_listener(self.on_track_mute_changed)
                track.remove_solo_listener(self.on_track_solo_changed)
                if hasattr(track, b'current_monitoring_state'):
                    track.remove_current_monitoring_state_listener(self.on_track_monitoring_changed)

        self.tracks_with_listener = []

    def disconnect(self):
        FaderfoxMixerController.disconnect(self)
        self.remove_track_listeners()
        self.parent.song().remove_tracks_listener(self.on_tracks_added_or_deleted)

    def receive_midi_note(self, channel, status, note_no, note_vel):
        if status == NOTEOFF_STATUS:
            return
        if channel == CHANNEL_SETUP2 and note_no in TRACK_SELECT_NOTES:
            idx = note_no - TRACK_SELECT_NOTES[0]
            track = self.helper.get_track(idx)
            self.set_selected_track(track)
        if channel == CHANNEL_SETUP2 and note_no == MASTER_TRACK_SELECT_NOTE:
            self.set_selected_track(self.parent.song().master_track)
        if channel == TRACK_CHANNEL_SETUP2 and status == NOTEON_STATUS:
            self.handle_status_note(note_no, MUTE_NOTES, b'mute')
            self.handle_status_note(note_no, ARM_NOTES, b'arm')
            self.handle_status_note(note_no, SOLO_NOTES, b'solo')
            self.handle_status_note(note_no, MONITOR_NOTES, b'monitor')

    def on_tracks_added_or_deleted(self):
        self.reset_status_cache()

    def map_track_params(self, script_handle, midi_map_handle):
        self.remove_track_listeners()
        for idx in range(0, 12):
            tracks = tuple(self.parent.song().tracks) + tuple(self.parent.song().return_tracks)
            if len(tracks) > idx:
                track = tracks[idx]
                if track.can_be_armed:
                    track.add_arm_listener(self.on_track_arm_changed)
                track.add_mute_listener(self.on_track_mute_changed)
                track.add_solo_listener(self.on_track_solo_changed)
                if hasattr(track, b'current_monitoring_state'):
                    track.add_current_monitoring_state_listener(self.on_track_monitoring_changed)
                    self.log(b'added track %s to monitoring')
                self.tracks_with_listener += [track]

        FaderfoxMixerController.map_track_params(self, script_handle, midi_map_handle)
        self.reset_status_cache()

    def send_track_status_midi(self, status, note):
        if status:
            self.parent.send_midi((TRACK_CHANNEL_SETUP2 + NOTEON_STATUS, note, STATUS_ON))
        else:
            self.parent.send_midi((
             TRACK_CHANNEL_SETUP2 + NOTEOFF_STATUS, note, STATUS_OFF2))

    def set_tracks_status(self, attr, notes):
        tracks = tuple(self.parent.song().tracks) + tuple(self.parent.song().return_tracks)
        for idx in range(0, 12):
            status = 0
            if len(tracks) > idx:
                track = tracks[idx]
                if not hasattr(track, attr):
                    continue
                if not track.can_be_armed and attr == b'arm':
                    continue
                status = track.__getattribute__(attr)
                if attr == b'mute':
                    status = not status
                if attr == b'current_monitoring_state':
                    self.log(b'current monitoring state of %s : %s' % (track, status))
                    status = status != 2
                    self.log(b'status is now %s' % track.monitoring_states.OFF)
            if self.status_cache[attr][idx] != status:
                self.send_track_status_midi(status, notes[idx])
                self.status_cache[attr][idx] = status

    def set_tracks_mute_status(self):
        self.set_tracks_status(b'mute', MUTE_NOTES)

    def set_tracks_arm_status(self):
        self.set_tracks_status(b'arm', ARM_NOTES)

    def set_tracks_solo_status(self):
        self.set_tracks_status(b'solo', SOLO_NOTES)

    def set_tracks_monitoring_status(self):
        self.set_tracks_status(b'current_monitoring_state', MONITOR_NOTES)

    def on_track_arm_changed(self):
        self.set_tracks_arm_status()

    def on_track_mute_changed(self):
        self.set_tracks_mute_status()

    def on_track_solo_changed(self):
        self.set_tracks_solo_status()

    def on_track_monitoring_changed(self):
        self.log(b'monitoring state changed')
        self.set_tracks_monitoring_status()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/LV2_LX2_LC2_LD2/LV2MixerController.pyc
