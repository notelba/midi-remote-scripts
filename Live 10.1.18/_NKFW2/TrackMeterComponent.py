# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackMeterComponent.py
# Compiled at: 2017-10-14 17:22:57
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group, CallableSubjectSlotGroup
from _Framework.Util import nop
from ControlUtils import set_group_button_lights
from consts import ZERO_DB_VALUE

class TrackMeterComponent(ControlSurfaceComponent):
    """ TrackMeterComponent allows a group of buttons to be used for displaying a
    track's level meter and controlling its volume. """

    def __init__(self, num_buttons, limit_to_0_db=False, should_invert_buttons=True, name='Track_Meter', *a, **k):
        super(TrackMeterComponent, self).__init__(name=name, *a, **k)
        self._should_invert_buttons = bool(should_invert_buttons)
        self._volume_max = ZERO_DB_VALUE if bool(limit_to_0_db) else 1.0
        self._num_buttons = num_buttons
        self._track = None
        self._meter_buttons = None
        self._volume_buttons = None
        self._scale_factor = self._num_buttons * 3
        r = xrange(self._num_buttons)
        self._dim_values = [ 'Meters.LowDim' for _ in r ]
        self._dim_values[-1] = 'Meters.Mid'
        self._half_values = [ 'Meters.LowHalf' for _ in r ]
        self._half_values[-1] = 'Meters.Mid'
        self._full_values = [ 'Meters.LowFull' for _ in r ]
        self._full_values[-1] = 'Meters.High'
        self._last_meter_value = -1
        self._dummy_listener = self.register_slot_manager(CallableSubjectSlotGroup(event='value', listener=nop, function=nop))
        return

    def disconnect(self):
        super(TrackMeterComponent, self).disconnect()
        self._track = None
        self._meter_buttons = None
        self._volume_buttons = None
        self._dim_values = None
        self._half_values = None
        self._full_values = None
        return

    def set_meter_buttons(self, buttons):
        """ Sets the buttons to use for displaying the track's meter. """
        self._last_meter_value = -1
        if self._should_invert_buttons:
            self._meter_buttons = list(buttons)[::-1] if buttons else []
        else:
            self._meter_buttons = list(buttons) if buttons else []
        if buttons and self.is_enabled():
            set_group_button_lights(buttons, 'DefaultButton.Off')
        self._dummy_listener.replace_subjects(self._meter_buttons)

    def set_volume_buttons(self, buttons):
        """ Sets the buttons to use for controlling the track's volume. """
        if self._should_invert_buttons:
            self._volume_buttons = list(buttons)[::-1] if buttons else []
        else:
            self._volume_buttons = list(buttons) if buttons else []
        self._on_volume_buttons_value.replace_subjects(self._volume_buttons)
        self._update_volume_buttons()

    def set_track(self, track):
        """ Sets the track to control. """
        self._last_meter_value = -1
        self._track = track
        audio_track = track if track and track.has_audio_output else None
        midi_track = track if track and not track.has_audio_output else None
        self._on_output_meter_level_changed.subject = midi_track
        self._on_output_meter_left_changed.subject = audio_track
        self._on_output_meter_right_changed.subject = audio_track
        self._on_volume_changed.subject = track.mixer_device.volume if track else None
        self._update_volume_buttons()
        if audio_track:
            self._update_audio_meter_buttons()
        else:
            self._update_midi_meter_buttons()
        return

    @subject_slot_group('value')
    def _on_volume_buttons_value(self, value, button):
        if self._track and value:
            if self._track.mixer_device.volume.is_enabled:
                self._track.mixer_device.volume.value = self._volume_max / (self._num_buttons - 1) * self._volume_buttons.index(button)

    @subject_slot('output_meter_left')
    def _on_output_meter_left_changed(self):
        self._update_audio_meter_buttons()

    @subject_slot('output_meter_right')
    def _on_output_meter_right_changed(self):
        self._update_audio_meter_buttons()

    @subject_slot('output_meter_level')
    def _on_output_meter_level_changed(self):
        self._update_midi_meter_buttons()

    @subject_slot('value')
    def _on_volume_changed(self):
        self._update_volume_buttons()

    def update(self):
        super(TrackMeterComponent, self).update()
        self.set_track(self._track)

    def _update_audio_meter_buttons(self):
        if self.is_enabled() and self._meter_buttons:
            if self._track:
                self._update_meter_button_leds((self._track.output_meter_left + self._track.output_meter_right) / 2.0)
            else:
                set_group_button_lights(self._meter_buttons, 'DefaultButton.Off')

    def _update_midi_meter_buttons(self):
        if self.is_enabled() and self._meter_buttons:
            if self._track:
                self._update_meter_button_leds(self._track.output_meter_level)
            else:
                set_group_button_lights(self._meter_buttons, 'DefaultButton.Off')

    def _update_meter_button_leds(self, value):
        scaled = int(value / 1.0 * self._scale_factor)
        if self._last_meter_value != scaled:
            if scaled is 0:
                set_group_button_lights(self._meter_buttons, 'DefaultButton.Off')
            else:
                high_btn_index = (scaled - 1) / 3
                high_value_full = scaled % 3 == 0
                high_value_half = scaled % 2 == 0
                for index, button in enumerate(self._meter_buttons):
                    if button:
                        if index < high_btn_index:
                            button.set_light(self._full_values[index])
                        elif index > high_btn_index:
                            button.set_light('DefaultButton.Off')
                        elif high_value_full:
                            button.set_light(self._full_values[index])
                        else:
                            button.set_light(self._half_values[index] if high_value_half else self._dim_values[index])

            self._last_meter_value = scaled

    def _update_volume_buttons(self):
        if self.is_enabled() and self._volume_buttons:
            if self._track:
                param = self._track.mixer_device.volume
                param_value = int(param.value / self._volume_max * self._num_buttons)
                for index, button in enumerate(self._volume_buttons):
                    button.set_light('Meters.Volume' if index <= param_value else 'DefaultButton.Off')

            else:
                set_group_button_lights(self._volume_buttons, 'DefaultButton.Off')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackMeterComponent.pyc
