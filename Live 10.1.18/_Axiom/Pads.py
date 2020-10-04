# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Axiom\Pads.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .consts import *

class Pads:
    """ Class representing the Pads section on the Axiom controllers """

    def __init__(self, parent):
        self.__parent = parent

    def build_midi_map(self, script_handle, midi_map_handle):
        for channel in range(4):
            for pad in range(8):
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, AXIOM_PADS[pad])

        for pad in range(8):
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, 15, AXIOM_PADS[pad])

    def receive_midi_cc(self, cc_no, cc_value, channel):
        if list(AXIOM_PADS).count(cc_no) > 0:
            pad_index = list(AXIOM_PADS).index(cc_no)
            index = pad_index + channel * 8
            if cc_value > 0:
                if channel in range(4):
                    if self.__parent.application().view.is_view_visible(b'Session'):
                        tracks = self.__parent.song().visible_tracks
                        if len(tracks) > index:
                            current_track = tracks[index]
                            clip_index = list(self.__parent.song().scenes).index(self.__parent.song().view.selected_scene)
                            current_track.clip_slots[clip_index].fire()
                    elif self.__parent.application().view.is_view_visible(b'Arranger'):
                        if len(self.__parent.song().cue_points) > index:
                            self.__parent.song().cue_points[index].jump()
                elif channel == 15:
                    self.__parent.bank_changed(pad_index)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Axiom/Pads.pyc
