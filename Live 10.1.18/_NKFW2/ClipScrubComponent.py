# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipScrubComponent.py
# Compiled at: 2017-04-24 12:52:35
from ClipPositionComponent import ClipPositionComponent, subject_slot

class ClipScrubComponent(ClipPositionComponent):
    """ ClipScrubComponent utilizes a group of buttons to scrub a clip. """

    def __init__(self, playhead_color='Clip.Scrubhead.Even', target_clip_comp=None, realign_on_release=False, name='Clip_Matrix_Scrub_Control', *a, **k):
        super(ClipScrubComponent, self).__init__(playhead_color=playhead_color, target_clip_comp=target_clip_comp, off_method=self.perform_off_action, name=name, *a, **k)
        self._on_global_quantize_changed.subject = self.song()
        self._is_scrubbing = True
        self._last_scrub_position = 0.0
        self._realign_on_release = bool(realign_on_release)

    def perform_position_action(self, position):
        self._clip.scrub(position)
        self._last_scrub_position = position
        self._is_scrubbing = True

    def perform_off_action(self):
        self._clip.stop_scrub()
        self._clip.set_fire_button_state(0)
        if self._realign_on_release:
            self.realign_playing_position()
        self._is_scrubbing = False

    def set_clip(self, clip):
        super(ClipScrubComponent, self).set_clip(clip)
        self._is_scrubbing = False

    def set_position_buttons(self, buttons):
        super(ClipScrubComponent, self).set_position_buttons(buttons)
        self._is_scrubbing = False

    @subject_slot('clip_trigger_quantization')
    def _on_global_quantize_changed(self):
        if self.is_enabled() and self._is_scrubbing and self._clip:
            self._clip.scrub(self._last_scrub_position)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipScrubComponent.pyc
