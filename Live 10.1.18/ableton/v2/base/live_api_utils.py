# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\live_api_utils.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals

def liveobj_changed(obj, other):
    """
    Check whether obj and other are not equal, properly handling lost weakrefs.

    Use this whenever you cache a Live API object in some variable, and want to check
    whether you need to update the cached object.
    """
    return obj != other or type(obj) != type(other)


def liveobj_valid(obj):
    """
    Check whether obj represents a valid Live API obj.

    This will return False both if obj represents a lost weakref or is None.
    It's important that Live API objects are not checked using "is None", since this
    would treat lost weakrefs as valid.
    """
    return obj != None


def is_parameter_bipolar(param):
    return param.min == -1 * param.max


def duplicate_clip_loop(clip):
    if liveobj_valid(clip) and clip.is_midi_clip:
        try:
            clip.duplicate_loop()
        except RuntimeError:
            pass
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/base/live_api_utils.pyc
