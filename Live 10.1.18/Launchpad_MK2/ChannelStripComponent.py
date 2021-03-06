# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\ChannelStripComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from _Framework.SubjectSlot import subject_slot
from _Framework.Control import ButtonControl
from _Framework.ChannelStripComponent import ChannelStripComponent as ChannelstripComponentBase
PAN_VALUE_DEVIATION_TOLERANCE = 0.01563

class ChannelStripComponent(ChannelstripComponentBase):
    volume_reset_button = ButtonControl()
    pan_reset_button = ButtonControl()
    send_a_reset_button = ButtonControl()
    send_b_reset_button = ButtonControl()

    def __init__(self, *a, **k):
        super(ChannelStripComponent, self).__init__(*a, **k)
        self._arm_on_value = 127
        self._arm_off_value = 0
        self._solo_on_value = 127
        self._solo_off_value = 0
        self._mute_on_value = 127
        self._mute_off_value = 0

    def set_mute_values(self, mute_on_value, mute_off_value):
        self._mute_on_value = mute_on_value
        self._mute_off_value = mute_off_value

    def set_solo_values(self, solo_on_value, solo_off_value):
        self._solo_on_value = solo_on_value
        self._solo_off_value = solo_off_value

    def set_arm_values(self, arm_on_value, arm_off_value):
        self._arm_on_value = arm_on_value
        self._arm_off_value = arm_off_value

    def _on_mute_changed(self):
        if self.is_enabled() and self._mute_button is not None:
            self._mute_button.set_light(self._mute_color_value())
        return

    def _on_solo_changed(self):
        if self.is_enabled() and self._solo_button is not None:
            self._solo_button.set_light(self._solo_color_value())
        return

    def _on_arm_changed(self):
        if self.is_enabled() and self._arm_button is not None:
            self._arm_button.set_light(self._arm_color_value())
        return

    def _mute_color_value(self):
        if self._track != None or self.empty_color is None:
            if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute != self._invert_mute_feedback:
                return self._mute_on_value
            else:
                return self._mute_off_value

        else:
            return self.empty_color
        return

    def _solo_color_value(self):
        if self._track != None or self.empty_color is None:
            if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.solo:
                return self._solo_on_value
            else:
                return self._solo_off_value

        else:
            return self.empty_color
        return

    def _arm_color_value(self):
        if self._track != None or self.empty_color is None:
            if self._track in self.song().tracks and self._track.can_be_armed and self._track.arm:
                return self._arm_on_value
            else:
                return self._arm_off_value

        else:
            return self.empty_color
        return

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        if self._track != None:
            self._on_volume_changed.subject = self._track.mixer_device.volume
            self._on_pan_changed.subject = self._track.mixer_device.panning
            sends = self._track.mixer_device.sends
            if len(sends) > 0:
                self._on_send_a_changed.subject = self._track.mixer_device.sends[0]
            if len(sends) > 1:
                self._on_send_b_changed.subject = self._track.mixer_device.sends[1]
        self._update_volume_button_led()
        self._update_pan_button_led()
        self._update_send_a_button_led()
        self._update_send_b_button_led()
        return

    @subject_slot(b'value')
    def _on_volume_changed(self):
        self._update_volume_button_led()

    @subject_slot(b'value')
    def _on_pan_changed(self):
        self._update_pan_button_led()

    @subject_slot(b'value')
    def _on_send_a_changed(self):
        self._update_send_a_button_led()

    @subject_slot(b'value')
    def _on_send_b_changed(self):
        self._update_send_b_button_led()

    def _update_volume_button_led(self):
        if self._track == None:
            self.volume_reset_button.color = b'Mixer.Disabled'
        else:
            volume = self._track.mixer_device.volume
            if volume.value != volume.default_value:
                self.volume_reset_button.color = b'Mixer.Volume.On'
            else:
                self.volume_reset_button.color = b'Mixer.Volume.Off'
        return

    def _update_pan_button_led(self):
        if self._track == None:
            self.pan_reset_button.color = b'Mixer.Disabled'
        else:
            panning = self._track.mixer_device.panning
            if abs(panning.value) > PAN_VALUE_DEVIATION_TOLERANCE:
                self.pan_reset_button.color = b'Mixer.Pan.On'
            else:
                self.pan_reset_button.color = b'Mixer.Pan.Off'
        return

    def _update_send_a_button_led(self):
        if self._track == None or len(self._track.mixer_device.sends) < 1:
            self.send_a_reset_button.color = b'Mixer.Disabled'
        else:
            send = self._track.mixer_device.sends[0]
            if send.value != send.default_value:
                self.send_a_reset_button.color = b'Sends.Send0.On'
            else:
                self.send_a_reset_button.color = b'Sends.Send0.Off'
        return

    def _update_send_b_button_led(self):
        if self._track == None or len(self._track.mixer_device.sends) < 2:
            self.send_b_reset_button.color = b'Mixer.Disabled'
        else:
            send = self._track.mixer_device.sends[1]
            if send.value != send.default_value:
                self.send_b_reset_button.color = b'Sends.Send1.On'
            else:
                self.send_b_reset_button.color = b'Sends.Send1.Off'
        return

    @volume_reset_button.pressed
    def volume_reset_button(self, button):
        if self._track != None:
            volume = self._track.mixer_device.volume
            if volume.is_enabled:
                volume.value = volume.default_value
        return

    @pan_reset_button.pressed
    def pan_reset_button(self, button):
        if self._track != None:
            panning = self._track.mixer_device.panning
            if panning.is_enabled:
                panning.value = panning.default_value
        return

    @send_a_reset_button.pressed
    def send_a_reset_button(self, button):
        if self._track != None and len(self._track.mixer_device.sends) > 0:
            send = self._track.mixer_device.sends[0]
            if send.is_enabled:
                send.value = send.default_value
        return

    @send_b_reset_button.pressed
    def send_b_reset_button(self, button):
        if self._track != None and len(self._track.mixer_device.sends) > 1:
            send = self._track.mixer_device.sends[1]
            if send.is_enabled:
                send.value = send.default_value
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_MK2/ChannelStripComponent.pyc
