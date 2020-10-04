# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_49_61_Classic\SliderSection.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Axiom.consts import *

class SliderSection:
    """ Class representing the sliders and Zone/Group-buttons on the
        Axiom 49 & 61 Controllers
    """

    def __init__(self, parent):
        self.__parent = parent
        self.__mod_pressed = False

    def build_midi_map(self, script_handle, midi_map_handle):
        feedback_rule = Live.MidiMap.CCFeedbackRule()
        needs_takeover = True
        feedback_rule.channel = 0
        feedback_rule.cc_no = AXIOM_SLI9
        feedback_rule.cc_value_map = tuple()
        feedback_rule.delay_in_ms = -1.0
        for channel in range(16):
            Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, self.__parent.song().master_track.mixer_device.volume, channel, AXIOM_SLI9, Live.MidiMap.MapMode.absolute, feedback_rule, not needs_takeover)

        for channel in range(4):
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, AXIOM_BUT9)
            for slider in range(8):
                tracks = self.__parent.song().visible_tracks
                track_index = slider + channel * 8
                if len(tracks) > track_index:
                    feedback_rule.channel = 0
                    feedback_rule.cc_no = AXIOM_SLIDERS[slider]
                    feedback_rule.cc_value_map = tuple()
                    feedback_rule.delay_in_ms = -1.0
                    Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, tracks[track_index].mixer_device.volume, channel, AXIOM_SLIDERS[slider], Live.MidiMap.MapMode.absolute, feedback_rule, not needs_takeover)
                    Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, AXIOM_BUTTONS[slider])
                else:
                    break

    def receive_midi_cc(self, cc_no, cc_value, channel):
        if list(AXIOM_BUTTONS).count(cc_no) > 0:
            button_index = list(AXIOM_BUTTONS).index(cc_no)
            if cc_no == AXIOM_BUT9:
                self.__mod_pressed = cc_value == 127
            elif button_index in range(8):
                tracks = self.__parent.song().visible_tracks
                track_index = button_index + 8 * channel
                if len(tracks) > track_index:
                    track = tracks[track_index]
                    if track and track.can_be_armed:
                        if not self.__mod_pressed:
                            track.mute = not track.mute
                        else:
                            track.arm = not track.arm
                            if self.__parent.song().exclusive_arm:
                                for t in tracks:
                                    if t.can_be_armed and t.arm and not t == track:
                                        t.arm = False

                            if track.arm:
                                if track.view.select_instrument():
                                    self.__parent.song().view.selected_track = track
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_49_61_Classic/SliderSection.pyc
