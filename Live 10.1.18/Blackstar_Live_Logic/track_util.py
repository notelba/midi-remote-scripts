# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\track_util.py
# Compiled at: 2020-07-20 20:22:59
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from ableton.v2.base import const, compose, depends, find_if, liveobj_valid
import Live
from .clip_util import clip_of_slot, has_clip

def playing_slot_index(track):
    """
    Return the index of the playing
    slot in `track`, if `track` is
    valid, otherwise `None`
    """
    if liveobj_valid(track):
        return track.playing_slot_index


def playing_or_recording_clip_slot(track):
    """
    Return the playing or recording clip slot
    of `track` if one exists, otherwise `None`
    """
    index = playing_slot_index(track)
    if index is not None and index >= 0:
        slot = track.clip_slots[index]
        if liveobj_valid(slot):
            return slot
    return


def fired_clip_slot(track):
    """
    Return the fired clip slot of `track`
    if it exists, otherwise `None`
    """
    if liveobj_valid(track) and track.fired_slot_index >= 0:
        slot = track.clip_slots[track.fired_slot_index]
        if liveobj_valid(slot):
            return slot


def is_fired(track):
    """
    Return `True` if any clip
    slot or the stop button of
    `track` is fired, `False`
    if not, and `None` for an invalid
    track
    """
    if liveobj_valid(track):
        return track.fired_slot_index != -1


def playing_clip_slot(track):
    """
    Return the playing clip slot
    of `track` if one exists, otherwise `None`
    """
    slot = playing_or_recording_clip_slot(track)
    if liveobj_valid(slot) and not slot.is_recording:
        return slot
    else:
        return


def recording_clip_slot(track):
    """
    Return the recording clip slot
    of `track` if one exists, otherwise `None`
    """
    slot = playing_or_recording_clip_slot(track)
    if liveobj_valid(slot) and slot.is_recording:
        return slot
    else:
        return


playing_or_recording_clip = compose(clip_of_slot, playing_or_recording_clip_slot)
playing_clip = compose(clip_of_slot, playing_clip_slot)
recording_clip = compose(clip_of_slot, recording_clip_slot)

@depends(song=const(None))
def get_or_create_first_empty_clip_slot(track, song=None):
    """
    Return the first empty clip slot, creating a new scene if there
    is currently none available. Return `None` if this fails
    """
    assert song is not None, b'A song instance must be injected to use `get_or_create_first_empty_clip_slot`'
    if liveobj_valid(track):
        first_empty_slot = find_if(lambda s: not s.has_clip, track.clip_slots)
        if first_empty_slot and liveobj_valid(first_empty_slot):
            return first_empty_slot
        try:
            song.create_scene(-1)
            slot = track.clip_slots[(-1)]
            if liveobj_valid(slot):
                return slot
        except Live.Base.LimitationError:
            pass

    return


def last_slot_with_clip(track):
    """
    Return the last clip slot of `track`
    that contains a clip
    """
    return find_if(has_clip, reversed(clip_slots(track)))


def clip_slots(track):
    """
    Return a list of clip slots of `track` or
    the empty list if the track is not valid
    """
    if liveobj_valid(track):
        return track.clip_slots
    return []


def is_playing(track):
    """
    Return `True` if `track` is not playing,
    `False` if it is, and `None` if it is invalid
    """
    if liveobj_valid(track):
        return track.playing_slot_index >= 0


def is_group_track(track):
    """
    Return `True` if `track` is a group track,
    `False` if not, and `None` if it is invalid
    """
    if liveobj_valid(track):
        return track.is_foldable


def is_grouped(track):
    """
    Return `True` if `track` is grouped by a group track,
    `False` if not, and `None` if it is invalid
    """
    if liveobj_valid(track):
        return track.is_grouped


def group_track(track):
    """
    Return the group track containing
    `track` if `track` is grouped or
    `None` otherwise
    """
    if is_grouped(track):
        return track.group_track


def flatten_tracks(tracks):
    """
    Return an iterator over
    `tracks` which replaces group
    tracks with their children
    """
    return chain(*((grouped_tracks(t) if is_group_track(t) else [t]) for t in tracks))


@depends(song=const(None))
def grouped_tracks(track, song=None):
    """
    Return an iterator over tracks that
    are grouped by `track`
    """
    if not song is not None:
        raise AssertionError(b'A song instance must be injected to use `grouped_tracks`')
        return is_group_track(track) or []
    else:
        return flatten_tracks(filter(lambda t: group_track(t) == track, song.tracks))


def toggle_fold(track):
    """
    Toggle the fold state of a group
    track, returning `False` if this
    is not possible
    """
    if is_group_track(track):
        track.fold_state = not track.fold_state
        return True
    return False


def is_folded(track):
    """
    Return `True` if `track` is a folded
    group track, otherwise `False`
    """
    if is_group_track(track):
        return track.fold_state


def has_clips(track):
    """
    Return `True` if `track` has any clips,
    otherwise `False`
    """
    if is_group_track(track):
        return any(map(has_clips, grouped_tracks(track)))
    else:
        return any(map(has_clip, clip_slots(track)))


def can_be_armed(track):
    """
    Return `True` if `track` can be armed,
    `False` if not, and `None` if it is invalid
    """
    if liveobj_valid(track):
        return track.can_be_armed


def arm(track):
    """
    Arm `track`, returning `True` if successful
    and `False` for an invalid or not armable track
    """
    if can_be_armed(track):
        track.arm = True
        return True
    return False


def unarm(track):
    """
    Unarm `track`, returning `True` if successful
    and `False` for an invalid or not armable track
    """
    if can_be_armed(track):
        track.arm = False
        return True
    return False


def stop_all_clips(track, quantized=True):
    """
    Trigger the stop all button on the track,
    returning `True` if successful and `False`
    for an invalid track
    """
    if liveobj_valid(track):
        track.stop_all_clips(quantized)
        return True
    return False


def unarm_tracks(tracks):
    """
    Unarm each track in `tracks` that can be armed
    """
    for track in tracks:
        unarm(track)


def tracks(song):
    """
    Return a list of valid tracks in `song`
    """
    return filter(liveobj_valid, song.tracks)


def visible_tracks(song):
    """
    Return a list of valid visible tracks in `song`
    """
    return filter(liveobj_valid, song.visible_tracks)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Blackstar_Live_Logic/track_util.pyc
