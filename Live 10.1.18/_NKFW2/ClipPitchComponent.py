# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipPitchComponent.py
# Compiled at: 2017-09-30 15:26:22
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from LaunchQuantizeComponent import LaunchQuantizeComponent
from ControlUtils import is_button_pressed, set_group_button_lights

class ClipPitchComponent(ControlSurfaceComponent):
    """ ClipPitchComponent utilizes a button matrix to play a clip chromatically. """

    def __init__(self, qntz_component, targets_comp=None, name='Clip_Matrix_Chromatic_Control', *a, **k):
        assert isinstance(qntz_component, LaunchQuantizeComponent)
        super(ClipPitchComponent, self).__init__(name=name, *a, **k)
        self._legato_active = False
        self._clip = None
        self._track = None
        self._pitch_parameter = None
        self._quantize_component = qntz_component
        self._ascending_pitch_buttons = None
        self._descending_pitch_buttons = None
        self._select_button = None
        self._on_target_clip_changed.subject = targets_comp
        self._on_target_track_changed.subject = targets_comp
        return

    def disconnect(self):
        super(ClipPitchComponent, self).disconnect()
        self._clip = None
        self._track = None
        self._pitch_parameter = None
        self._quantize_component = None
        self._ascending_pitch_buttons = None
        self._descending_pitch_buttons = None
        self._select_button = None
        return

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, clip):
        self.set_clip(clip)

    def set_clip(self, clip):
        """ Sets the clip to control and sets up listeners if is audio clip.
        This does not work on arrangement view clips. """
        assert clip is None or isinstance(clip, Live.Clip.Clip)
        self._clip = clip if clip is not None and not clip.is_arrangement_clip else None
        self._on_pitch_coarse_changed.subject = clip if self._clip and self._clip.is_audio_clip else None
        self._on_pitch_changed()
        return

    @subject_slot('target_track')
    def _on_target_track_changed(self, track):
        self.set_track(track)

    def set_track(self, track):
        """ Sets the track to control and adds device listener if it's a MIDI track. """
        assert track is None or isinstance(track, Live.Track.Track)
        self._pitch_parameter = None
        self._track = None
        if track and track.has_midi_input:
            self._track = track
        self._on_devices_changed.subject = self._track
        if self._track and self.is_enabled():
            self._on_devices_changed()
            self._on_pitch_changed()
        return

    def set_pitch_matrix(self, matrix):
        """ Sets a matrix to use for playing ascending and descending pitches. This
        requires that the matrix has an even number of rows. """
        assert matrix is None or matrix.height() % 2 == 0
        upper_buttons = []
        lower_buttons = []
        if matrix:
            height = matrix.height()
            width = matrix.width()
            div = height / 2
            for row in xrange(div - 1, -1, -1):
                for column in xrange(width):
                    upper_buttons.append(matrix.get_button(column, row))

            for row in xrange(div, height):
                for column in xrange(width - 1, -1, -1):
                    lower_buttons.append(matrix.get_button(column, row))

        self.set_ascending_pitch_buttons(upper_buttons)
        self.set_descending_pitch_buttons(lower_buttons)
        return

    def set_ascending_pitch_buttons(self, buttons):
        """ Sets the buttons to use for triggering ascending pitches. """
        self._ascending_pitch_buttons = list(buttons) if buttons else None
        self._on_ascending_pitch_buttons_value.replace_subjects(buttons or [])
        self._on_pitch_changed()
        return

    def set_descending_pitch_buttons(self, buttons):
        """ Sets the buttons to use for triggering descending pitches. """
        self._descending_pitch_buttons = list(buttons) if buttons else None
        self._on_descending_pitch_buttons_value.replace_subjects(buttons or [])
        self._on_pitch_changed()
        return

    def set_legato_button(self, button):
        """ Sets the button to use for toggling legato state. """
        self._on_legato_button_value.subject = button if button else None
        self._update_legato_button()
        return

    def set_select_button(self, button):
        """ Sets the button to use as the select modifier. """
        self._select_button = button

    @subject_slot_group('value')
    def _on_ascending_pitch_buttons_value(self, value, button):
        if self.is_enabled() and self._can_control_pitch():
            button_index = self._ascending_pitch_buttons.index(button)
            if value:
                self._set_pitch(button_index)
            self._handle_launch(value)

    @subject_slot_group('value')
    def _on_descending_pitch_buttons_value(self, value, button):
        if self.is_enabled() and self._can_control_pitch():
            button_index = self._descending_pitch_buttons.index(button)
            if value:
                self._set_pitch(-button_index)
            self._handle_launch(value)

    def _can_control_pitch(self):
        return self._clip is not None and (self._clip.is_audio_clip or self._pitch_parameter is not None)

    def _set_pitch(self, pitch):
        """ Sets the ascending or descending pitch on the appropriate
        parameter/setting. """
        if self._clip.is_audio_clip:
            self._clip.pitch_coarse = pitch
        elif self._pitch_parameter and self._pitch_parameter.is_enabled:
            self._pitch_parameter.value = pitch

    def _handle_launch(self, value):
        """ Handles launching the clip (or not if select is pressed) with legato or
        with quantization override. """
        if is_button_pressed(self._select_button):
            return
        if self._legato_active:
            if value:
                self._clip.canonical_parent.fire(force_legato=True, launch_quantization=self._quantize_component.quantization)
        elif value:
            last_qntz = int(self.song().clip_trigger_quantization)
            self.song().clip_trigger_quantization = self._quantize_component.quantization
            self._clip.set_fire_button_state(True)
            self.song().clip_trigger_quantization = last_qntz
        else:
            self._clip.set_fire_button_state(False)

    @subject_slot('value')
    def _on_legato_button_value(self, value):
        """ Toggles legato state. """
        if self.is_enabled() and value:
            self._legato_active = not self._legato_active
            self._update_legato_button()

    def update(self):
        super(ClipPitchComponent, self).update()
        self.set_clip(self._clip)
        self.set_track(self._track)
        self._update_legato_button()

    @subject_slot('devices')
    def _on_devices_changed(self):
        """ Called on devices changed on MIDI track to locate pitch device and
        its pitch parameter. """
        self._pitch_parameter = None
        if self._track:
            for device in self._track.devices:
                if device and device.class_name == 'MidiPitcher':
                    self._pitch_parameter = device.parameters[1]
                    break

        self._on_pitch_parameter_changed.subject = self._pitch_parameter
        return

    @subject_slot('pitch_coarse')
    def _on_pitch_coarse_changed(self):
        if self.is_enabled():
            self._on_pitch_changed(self._clip.pitch_coarse)

    @subject_slot('value')
    def _on_pitch_parameter_changed(self):
        if self.is_enabled():
            self._on_pitch_changed(int(self._pitch_parameter.value))

    def _on_pitch_changed(self, pitch=None):
        """ Updates pitch matrix LEDs to reflect clip pitch. """
        if self.is_enabled():
            if pitch is None:
                pitch = 0
                if self._clip:
                    if self._clip.is_audio_clip:
                        pitch = int(self._clip.pitch_coarse)
                    elif self._pitch_parameter:
                        pitch = int(self._pitch_parameter.value)
            self._update_pitch_buttons('Ascending', self._ascending_pitch_buttons, pitch >= 0, pitch)
            self._update_pitch_buttons('Descending', self._descending_pitch_buttons, pitch <= 0, abs(pitch))
        return

    @staticmethod
    def _update_pitch_buttons(name, buttons, predicate, pitch):
        if buttons:
            set_group_button_lights(buttons, 'Clip.Pitch.%s' % name)
            if predicate:
                if pitch in xrange(len(buttons)):
                    buttons[pitch].set_light('Clip.Pitch.Selected')
                else:
                    buttons[(-1)].set_light('Clip.Pitch.Selected')

    def _update_legato_button(self):
        """ Updates the legato button's LED. """
        if self.is_enabled():
            button = self._on_legato_button_value.subject
            if button:
                button.set_light('Clip.LegatoOn' if self._legato_active else 'Clip.LegatoOff')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipPitchComponent.pyc
