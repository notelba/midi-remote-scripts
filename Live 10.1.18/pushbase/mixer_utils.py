# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\mixer_utils.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live

def is_set_to_split_stereo(mixer):
    modes = Live.MixerDevice.MixerDevice.panning_modes
    return modes.stereo_split == getattr(mixer, b'panning_mode', modes.stereo)


def has_pan_mode(mixer):
    return hasattr(mixer, b'panning_mode')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/pushbase/mixer_utils.pyc
