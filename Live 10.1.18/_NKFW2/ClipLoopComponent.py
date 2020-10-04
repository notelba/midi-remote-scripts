# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipLoopComponent.py
# Compiled at: 2017-03-07 13:28:52
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from ControlUtils import get_group_buttons_pressed, set_group_button_lights
from ClipUtils import apply_loop_settings
from Utils import floats_equal

class ClipLoopComponent(ControlSurfaceComponent):
    """ ClipLoopComponent utilizes a group of buttons to control a clip's loop. """

    def __init__(self, move_start, zoom_loop, use_odd_colors=False, target_clip_comp=None, name='Clip_Matrix_Loop_Control', *a, **k):
        super(ClipLoopComponent, self).__init__(name=name, *a, **k)
        self._move_start_with_loop = bool(move_start)
        self._zoom_loop_on_edit = bool(zoom_loop)
        self._loop_buttons = None
        self._clip = None
        self._in_range_value = 'Clip.Loop.Even.InRange'
        self._partially_in_range_value = 'Clip.Loop.Even.PartiallyInRange'
        self._out_of_range_value = 'Clip.Loop.Even.OutOfRange'
        self.set_use_odd_colors(use_odd_colors, False)
        self._on_target_clip_changed.subject = target_clip_comp
        return

    def disconnect(self):
        super(ClipLoopComponent, self).disconnect()
        self._loop_buttons = None
        self._clip = None
        return

    def set_use_odd_colors(self, use_odd_colors, do_update=True):
        """ Sets whether or not to use odd colors to display the loop. """
        self._in_range_value = 'Clip.Loop.Odd.InRange' if use_odd_colors else 'Clip.Loop.Even.InRange'
        self._partially_in_range_value = 'Clip.Loop.Odd.PartiallyInRange' if use_odd_colors else 'Clip.Loop.Even.PartiallyInRange'
        self._out_of_range_value = 'Clip.Loop.Odd.OutOfRange' if use_odd_colors else 'Clip.Loop.Even.OutOfRange'
        if do_update:
            self._on_loop_properties_changed()

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, clip):
        self.set_clip(clip)

    def set_clip(self, clip):
        """ Sets the clip to control and sets up listeners. """
        assert clip is None or isinstance(clip, Live.Clip.Clip)
        self._clip = clip
        self._on_looping_changed.subject = self._clip
        self._on_loop_start_changed.subject = self._clip
        self._on_loop_end_changed.subject = self._clip
        self._on_end_marker_changed.subject = self._clip
        self._on_loop_properties_changed()
        return

    def set_loop_buttons(self, buttons):
        """ Sets the buttons to use for adjusting the clip's loop. """
        self._loop_buttons = list(buttons) if buttons else None
        self._on_loop_buttons_value.replace_subjects(buttons or [])
        self._on_loop_properties_changed()
        return

    @subject_slot_group('value')
    def _on_loop_buttons_value(self, value, _):
        """ Sets the clip's loop start/end points with multi-press compatibility. """
        if self.is_enabled() and self._clip and self._clip.looping and (not self._clip.is_recording or self._clip.is_overdubbing):
            if value:
                segment_length = self._clip.end_marker / len(self._loop_buttons)
                pressed = get_group_buttons_pressed(self._loop_buttons)
                start = pressed[0] * segment_length
                if len(pressed) == 2:
                    end = pressed[1] * segment_length + segment_length
                else:
                    end = start + segment_length
                apply_loop_settings(self._clip, (
                 start, end), self._move_start_with_loop, False, self._zoom_loop_on_edit)

    def update(self):
        super(ClipLoopComponent, self).update()
        self.set_clip(self._clip)

    @subject_slot('looping')
    def _on_looping_changed(self):
        self._on_loop_properties_changed()

    @subject_slot('loop_start')
    def _on_loop_start_changed(self):
        self._on_loop_properties_changed()

    @subject_slot('loop_end')
    def _on_loop_end_changed(self):
        self._on_end_marker_changed()

    @subject_slot('end_marker')
    def _on_end_marker_changed(self):
        self._on_loop_properties_changed()

    def _on_loop_properties_changed(self):
        """ Updates loop button LEDs to reflect current state and position of the
        clip's loop. """
        if self.is_enabled() and self._loop_buttons:
            if self._clip:
                if self._clip.looping:
                    seg_len = self._clip.end_marker / len(self._loop_buttons)
                    adjusted_end = self._clip.loop_end - seg_len
                    for index, button in enumerate(self._loop_buttons):
                        if button:
                            btn_pos = seg_len * index
                            end_diff = abs(adjusted_end - btn_pos)
                            start_diff = abs(self._clip.loop_start - btn_pos)
                            if btn_pos >= self._clip.loop_start and (btn_pos <= adjusted_end or floats_equal(btn_pos, adjusted_end)):
                                button.set_light(self._in_range_value)
                            elif btn_pos >= self._clip.loop_start and end_diff < seg_len:
                                button.set_light(self._partially_in_range_value)
                            elif btn_pos < self._clip.loop_start and start_diff < seg_len:
                                button.set_light(self._partially_in_range_value)
                            else:
                                button.set_light(self._out_of_range_value)

                else:
                    set_group_button_lights(self._loop_buttons, self._out_of_range_value)
            else:
                set_group_button_lights(self._loop_buttons, 'Clip.NoClip')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipLoopComponent.pyc
