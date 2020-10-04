# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ClipCreator.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
_Q = Live.Song.Quantization

class ClipCreator(object):
    """
    Manages clip creation over all components.
    """
    grid_quantization = None
    is_grid_triplet = False
    fixed_length = 8

    def create(self, slot, length=None):
        assert slot.clip == None
        if length is None:
            length = self.fixed_length
        slot.create_clip(length)
        if self.grid_quantization != None:
            slot.clip.view.grid_quantization = self.grid_quantization
            slot.clip.view.grid_is_triplet = self.is_grid_triplet
        slot.fire(force_legato=True, launch_quantization=_Q.q_no_q)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Framework/ClipCreator.pyc
