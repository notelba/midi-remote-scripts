# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\StepSeqComponentBase.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from PlayingOrSelectedClipMixin import PlayingOrSelectedClipMixin
from ShowMessageMixin import ShowMessageMixin
from SeqPageComponent import SeqPageComponent
from Utils import live_object_is_valid

class StepSeqComponentBase(PlayingOrSelectedClipMixin, CompoundComponent, ShowMessageMixin):
    """ StepSeqComponentBase is the base class for step-sequencing components. It allows
    for sequencing into the selected clip or it can prefer to sequence into the playing
    clip. Sub-classes must create their own PlayheadComponent and NoteLaneComponents. """

    def __init__(self, num_steps, res_comp, targets_comp=None, prefer_playing_clip=False, *a, **k):
        super(StepSeqComponentBase, self).__init__(targets_comp=targets_comp, *a, **k)
        self._clip = None
        if prefer_playing_clip:
            targets_comp = None
        else:
            self.set_track.subject = None
            self.set_track = lambda x: None
            self.set_clip = lambda x: None
            self._track = None
        self._page_component = self.register_component(SeqPageComponent(num_steps, res_comp, targets_comp=targets_comp))
        return

    def disconnect(self):
        super(StepSeqComponentBase, self).disconnect()
        self._clip = None
        return

    def set_physical_display_element(self, element):
        """ Sets the display element of the SeqPageComponent. """
        super(StepSeqComponentBase, self).set_physical_display_element(element)
        self._page_component.set_physical_display_element(element)

    def set_playhead(self, playhead):
        """ Sets the playhead object to use. """
        self._playhead_component.set_playhead(playhead)

    def set_page_buttons(self, buttons):
        """ Sets the buttons to use for selecting pages/adjusting the clip's loop. """
        self._page_component.set_page_buttons(buttons)

    def set_delete_button(self, button):
        """ Sets the delete modifier to use. """
        self._page_component.set_delete_button(button)

    def set_duplicate_button(self, button):
        """ Sets the duplicate modifier to use. """
        self._page_component.set_duplicate_button(button)

    def set_clip(self, clip):
        """ Used when prefer_playing_clip to set the clip of sub-components. """
        if clip != self._clip or not live_object_is_valid(self._clip):
            self._clip = clip if clip and clip.is_midi_clip else None
            self._page_component.set_clip(clip)
            self._playhead_component.set_clip(clip)
            for n in self._note_lane_components:
                n.set_clip(clip)

            self.on_clip_changed()
        return

    @subject_slot('target_track')
    def set_track(self, track):
        """ Used when prefer_playing_clip to set the track of sub-components. """
        super(StepSeqComponentBase, self).set_track(track)
        self._page_component.set_track(track)
        for n in self._note_lane_components:
            n.set_track(track)

    def on_clip_changed(self):
        """ Called when the clip this component controls changes. """
        pass
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/StepSeqComponentBase.pyc
