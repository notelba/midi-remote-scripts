# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\clip_util.py
# Compiled at: 2020-07-20 20:22:59
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import compose, find_if, liveobj_valid

def has_clip(slot):
    """
    Return `True` if `slot` contains
    a clip, `False` if not, or `None`
    for an invalid slot
    """
    if liveobj_valid(slot):
        return slot.has_clip


def clip_of_slot(slot):
    """
    Return the clip of `slot` if one
    exists, otherwise `None`
    """
    if liveobj_valid(slot) and liveobj_valid(slot.clip):
        return slot.clip


def fire(clip_or_slot, **k):
    """
    Fire `clip_slot`, returning `True` if this
    was successful and `False` otherwise
    """
    if liveobj_valid(clip_or_slot):
        clip_or_slot.fire(**k)
        return True
    return False


def delete_clip(slot):
    """
    Delete the clip in `slot` if
    there is one, returning `True`
    if successful and `False` otherwise
    """
    if liveobj_valid(slot) and has_clip(slot):
        slot.delete_clip()
        return True
    return False


def is_looping(clip):
    """
    Return `True` if the looping setting of `clip`
    is enabled, `False` if not, and `None` if
    `clip` is not valid
    """
    if liveobj_valid(clip):
        return clip.looping


def get_clip_time(clip):
    """
    Return a tuple containing the current bars and beats
    of `clip` in terms of the clip's time signature
    """
    sig_num, sig_denom = clip.signature_numerator, clip.signature_denominator
    loop_position = (clip.playing_position - clip.loop_start) * sig_denom / 4.0
    beats = int(loop_position) % sig_num + 1
    bars = int(loop_position / sig_num) + 1
    return (
     bars, beats)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Blackstar_Live_Logic/clip_util.pyc
