# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\util.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import find_nearest_color
from .colors import CLIP_COLOR_TABLE, RGB_COLOR_TABLE, Rgb

def skin_scroll_buttons(scoll_component, color, pressed_color):
    scoll_component.scroll_up_button.color = color
    scoll_component.scroll_down_button.color = color
    scoll_component.scroll_up_button.pressed_color = pressed_color
    scoll_component.scroll_down_button.pressed_color = pressed_color


def is_song_recording(song):
    return song.session_record or song.record_mode


def get_midi_color_value_for_track(track):
    """
    Returns midi value corresponding to track color for a valid track,
    otherwise return Rgb.BLACK (the off color)
    """
    if liveobj_valid(track):
        color = CLIP_COLOR_TABLE.get(track.color, None)
        if color is None:
            color = find_nearest_color(RGB_COLOR_TABLE, track.color)
        return color
    return Rgb.BLACK.midi_value
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/util.pyc
