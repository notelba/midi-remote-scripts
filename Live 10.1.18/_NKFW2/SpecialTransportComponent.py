# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialTransportComponent.py
# Compiled at: 2017-04-24 12:52:35
from functools import partial
import Live
RQ = Live.Song.RecordingQuantization
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Control import ButtonControl
from _Framework.SubjectSlot import subject_slot
from _Framework import Task
from SpecialControl import SpecialButtonControl
SEEK_SPEED = 10.0

class SpecialTransportComponent(ControlSurfaceComponent):
    """ Unlike other SpecialxxxComponents, this doesn't actually extend an existing
    component, it redoes it with skin support and some different features. """
    play_button = SpecialButtonControl(color='Transport.PlayOff', on_color='Transport.PlayOn')
    play_toggle_button = SpecialButtonControl(color='Transport.PlayOff', on_color='Transport.PlayOn')
    continue_button = SpecialButtonControl(color='Transport.ContinueOff', on_color='Transport.ContinueOn')
    stop_button = SpecialButtonControl(color='Transport.StopOff', on_color='Transport.StopOn')
    overdub_button = SpecialButtonControl(color='Transport.OverdubOff', on_color='Transport.OverdubOn')
    record_button = SpecialButtonControl(color='Transport.RecordOff', on_color='Transport.RecordOn')
    metronome_button = SpecialButtonControl(color='Transport.MetronomeOff', on_color='Transport.MetronomeOn')
    loop_button = SpecialButtonControl(color='Transport.LoopOff', on_color='Transport.LoopOn')
    record_quantize_button = SpecialButtonControl(color='Transport.RecordQuantizeOff', on_color='Transport.RecordQuantizeOn')
    prev_cue_button = SpecialButtonControl(color='Transport.CannotJumpToPrevCue', on_color='Transport.CanJumpToPrevCue')
    next_cue_button = SpecialButtonControl(color='Transport.CannotJumpToNextCue', on_color='Transport.CanJumpToNextCue')
    tap_tempo_button = ButtonControl(**dict(color='Transport.TapTempo', pressed_color='Transport.TapTempoPressed', disabled_color='DefaultButton.Disabled'))
    revert_button = ButtonControl(**dict(color='Transport.Revert', pressed_color='Transport.RevertPressed', disabled_color='DefaultButton.Disabled'))

    def __init__(self, name='Transport_Control', *a, **k):
        super(SpecialTransportComponent, self).__init__(name=name, *a, **k)
        self._relative_tempo_control = None
        self._relative_tempo_fine_control = None
        self._ffwd_button = None
        self._rwd_button = None
        self._rwd_task = Task.Task()
        self._ffwd_task = Task.Task()
        self._nudge_down_button = None
        self._nudge_up_button = None
        self._last_record_quantization = RQ.rec_q_sixtenth
        self._on_is_playing_changed.subject = self.song()
        self._on_overdub_changed.subject = self.song()
        self._on_record_mode_changed.subject = self.song()
        self._on_metronome_changed.subject = self.song()
        self._on_loop_changed.subject = self.song()
        self._on_record_quantize_changed.subject = self.song()
        self._on_can_jump_to_prev_cue_changed.subject = self.song()
        self._on_can_jump_to_next_cue_changed.subject = self.song()
        self._end_undo_step_task = self._tasks.add(Task.sequence(Task.wait(1.5), Task.run(self.song().end_undo_step)))
        self._end_undo_step_task.kill()
        return

    def disconnect(self):
        super(SpecialTransportComponent, self).disconnect()
        self._relative_tempo_control = None
        self._relative_tempo_fine_control = None
        self._ffwd_button = None
        self._rwd_button = None
        self._nudge_down_button = None
        self._nudge_up_button = None
        self._rwd_task = None
        self._ffwd_task = None
        self._end_undo_step_task = None
        return

    def set_relative_tempo_control(self, control):
        """ Sets the relative encoder to use for adjusting tempo in 1-BPM increments. """
        self._relative_tempo_control = control
        self._on_relative_tempo_control_value.subject = control

    def set_relative_tempo_fine_control(self, control):
        """ Sets the relative encoder to use for adjusting tempo in .1-BPM increments. """
        self._relative_tempo_fine_control = control
        self._on_relative_tempo_fine_control_value.subject = control

    def set_seek_forward_button(self, ffwd_button):
        """ Sets the button to use for fastforwarding. """
        if self._ffwd_button != ffwd_button:
            self._ffwd_button = ffwd_button
            self._ffwd_value_slot.subject = ffwd_button
            self._ffwd_task.kill()
            self._update_seek_buttons()

    def set_seek_backward_button(self, rwd_button):
        """ Sets the button to use for rewinding. """
        if self._rwd_button != rwd_button:
            self._rwd_button = rwd_button
            self._rwd_value_slot.subject = rwd_button
            self._rwd_task.kill()
            self._update_seek_buttons()

    def set_nudge_down_button(self, button):
        """ Sets the button to use for nudging down. """
        self.song().nudge_down = False
        if self._nudge_down_button != button:
            self._nudge_down_button = button
            self._on_nudge_down_button_value.subject = button
            self._update_nudge_buttons()

    def set_nudge_up_button(self, button):
        """ Sets the button to use for nudging up. """
        self.song().nudge_up = False
        if self._nudge_up_button != button:
            self._nudge_up_button = button
            self._on_nudge_up_button_value.subject = button
            self._update_nudge_buttons()

    @play_button.pressed
    def play_button(self, _):
        self.song().start_playing()

    @play_toggle_button.pressed
    def play_toggle_button(self, _):
        self.song().is_playing = not self.song().is_playing

    @continue_button.pressed
    def continue_button(self, _):
        self.song().continue_playing()

    @stop_button.pressed
    def stop_button(self, _):
        self.song().stop_playing()

    @overdub_button.pressed
    def overdub_button(self, _):
        self.song().overdub = not self.song().overdub

    @record_button.pressed
    def record_button(self, _):
        self.song().record_mode = not self.song().record_mode

    @metronome_button.pressed
    def metronome_button(self, _):
        self.song().metronome = not self.song().metronome

    @loop_button.pressed
    def loop_button(self, _):
        self.song().loop = not self.song().loop

    @record_quantize_button.pressed
    def record_quantize_button(self, _):
        is_on = self.song().midi_recording_quantization != RQ.rec_q_no_q
        if is_on:
            self._last_record_quantization = self.song().midi_recording_quantization
            self.song().midi_recording_quantization = RQ.rec_q_no_q
        else:
            self.song().midi_recording_quantization = self._last_record_quantization

    @prev_cue_button.pressed
    def prev_cue_button(self, _):
        if self.song().can_jump_to_prev_cue:
            self.song().jump_to_prev_cue()

    @next_cue_button.pressed
    def next_cue_button(self, _):
        if self.song().can_jump_to_next_cue:
            self.song().jump_to_next_cue()

    @tap_tempo_button.pressed
    def tap_tempo_button(self, _):
        if not self._end_undo_step_task.is_running:
            self.song().begin_undo_step()
        self._end_undo_step_task.restart()
        self.song().tap_tempo()

    @revert_button.pressed
    def revert_button(self, _):
        self.song().current_song_time = 0

    @subject_slot('value')
    def _on_nudge_down_button_value(self, value):
        if self.is_enabled():
            self.song().nudge_down = value is not 0
            self._nudge_down_button.set_light('Transport.NudgePressed' if value else 'Transport.Nudge')

    @subject_slot('value')
    def _on_nudge_up_button_value(self, value):
        if self.is_enabled():
            self.song().nudge_up = value is not 0
            self._nudge_up_button.set_light('Transport.NudgePressed' if value else 'Transport.Nudge')

    @subject_slot('value')
    def _ffwd_value_slot(self, value):
        if self.is_enabled():
            self._ffwd_value(value)
            self._ffwd_button.set_light('Transport.SeekPressed' if value else 'Transport.SeekIdle')

    def _ffwd_value(self, value):
        if self._ffwd_button.is_momentary():
            self._ffwd_task.kill()
            if value:
                self._ffwd_task = self._tasks.add(partial(self._move_current_song_time, SEEK_SPEED))
        else:
            self.song().current_song_time += 1

    @subject_slot('value')
    def _rwd_value_slot(self, value):
        if self.is_enabled():
            self._rwd_value(value)
            self._rwd_button.set_light('Transport.SeekPressed' if value else 'Transport.SeekIdle')

    def _rwd_value(self, value):
        if self._rwd_button.is_momentary():
            self._rwd_task.kill()
            if value:
                self._rwd_task = self._tasks.add(partial(self._move_current_song_time, -SEEK_SPEED))
        else:
            song = self.song()
            song.current_song_time = max(0.0, song.current_song_time - 1)

    def _move_current_song_time(self, speed, delta):
        song = self.song()
        song.current_song_time = max(0.0, song.current_song_time + speed * delta)
        return Task.RUNNING

    @subject_slot('value')
    def _on_relative_tempo_control_value(self, value):
        self._adjust_tempo(self._relative_tempo_control, value, False)

    @subject_slot('value')
    def _on_relative_tempo_fine_control_value(self, value):
        self._adjust_tempo(self._relative_tempo_fine_control, value, True)

    def _adjust_tempo(self, control, value, is_fine):
        factor = control.get_adjustment_factor(value, 0)
        if is_fine:
            factor *= 0.1
        self.song().tempo = max(20, min(999, self.song().tempo + factor))

    def update(self):
        super(SpecialTransportComponent, self).update()
        self._on_is_playing_changed()
        self._on_overdub_changed()
        self._on_record_mode_changed()
        self._on_metronome_changed()
        self._on_loop_changed()
        self._on_record_quantize_changed()
        self._on_can_jump_to_prev_cue_changed()
        self._on_can_jump_to_next_cue_changed()
        self._update_nudge_buttons()
        self._update_seek_buttons()

    def _update_nudge_buttons(self):
        if self.is_enabled():
            if self._nudge_down_button:
                self._nudge_down_button.set_light('Transport.Nudge')
            if self._nudge_up_button:
                self._nudge_up_button.set_light('Transport.Nudge')

    def _update_seek_buttons(self):
        if self.is_enabled():
            if self._ffwd_button:
                self._ffwd_button.set_light('Transport.SeekIdle')
            if self._rwd_button:
                self._rwd_button.set_light('Transport.SeekIdle')

    @subject_slot('is_playing')
    def _on_is_playing_changed(self):
        self._update_play_button()
        self._update_play_toggle_button()
        self._update_continue_button()
        self._update_stop_button()

    @subject_slot('overdub')
    def _on_overdub_changed(self):
        if self.is_enabled():
            self.overdub_button.is_on = self.song().overdub

    @subject_slot('record_mode')
    def _on_record_mode_changed(self):
        if self.is_enabled():
            self.record_button.is_on = self.song().record_mode

    @subject_slot('metronome')
    def _on_metronome_changed(self):
        if self.is_enabled():
            self.metronome_button.is_on = self.song().metronome

    @subject_slot('loop')
    def _on_loop_changed(self):
        if self.is_enabled():
            self.loop_button.is_on = self.song().loop

    @subject_slot('midi_recording_quantization')
    def _on_record_quantize_changed(self):
        if self.is_enabled():
            self.record_quantize_button.is_on = self.song().midi_recording_quantization != RQ.rec_q_no_q

    @subject_slot('can_jump_to_prev_cue')
    def _on_can_jump_to_prev_cue_changed(self):
        if self.is_enabled():
            self.prev_cue_button.is_on = self.song().can_jump_to_prev_cue

    @subject_slot('can_jump_to_next_cue')
    def _on_can_jump_to_next_cue_changed(self):
        if self.is_enabled():
            self.next_cue_button.is_on = self.song().can_jump_to_next_cue

    def _update_play_button(self):
        if self.is_enabled():
            self.play_button.is_on = self.song().is_playing

    def _update_play_toggle_button(self):
        if self.is_enabled():
            self.play_toggle_button.is_on = self.song().is_playing

    def _update_continue_button(self):
        if self.is_enabled():
            self.continue_button.is_on = self.song().is_playing

    def _update_stop_button(self):
        if self.is_enabled():
            self.stop_button.is_on = not self.song().is_playing
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialTransportComponent.pyc
