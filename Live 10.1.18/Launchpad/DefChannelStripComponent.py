# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad\DefChannelStripComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ChannelStripComponent import ChannelStripComponent
from .ConfigurableButtonElement import ConfigurableButtonElement
from itertools import chain

class DefChannelStripComponent(ChannelStripComponent):
    """ Subclass of channel strip component offering defaultbuttons for the timeables """

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._default_volume_button = None
        self._default_panning_button = None
        self._default_send1_button = None
        self._default_send2_button = None
        self._invert_mute_feedback = True
        return

    def disconnect(self):
        """ releasing references and removing listeners"""
        if self._track != None:
            volume = self._track.mixer_device.volume
            panning = self._track.mixer_device.panning
            sends = self._track.mixer_device.sends
            if volume.value_has_listener(self._on_volume_changed):
                volume.remove_value_listener(self._on_volume_changed)
            if panning.value_has_listener(self._on_panning_changed):
                panning.remove_value_listener(self._on_panning_changed)
            if len(sends) > 0 and sends[0].value_has_listener(self._on_send1_changed):
                sends[0].remove_value_listener(self._on_send1_changed)
            if len(sends) > 1 and sends[1].value_has_listener(self._on_send2_changed):
                sends[1].remove_value_listener(self._on_send2_changed)
        if self._default_volume_button != None:
            self._default_volume_button.remove_value_listener(self._default_volume_value)
            self._default_volume_button = None
        if self._default_panning_button != None:
            self._default_panning_button.remove_value_listener(self._default_panning_value)
            self._default_panning_button = None
        if self._default_send1_button != None:
            self._default_send1_button.remove_value_listener(self._default_send1_value)
            self._default_send1_button = None
        if self._default_send2_button != None:
            self._default_send2_button.remove_value_listener(self._default_send2_value)
            self._default_send2_button = None
        ChannelStripComponent.disconnect(self)
        return

    def set_track(self, track):
        assert track == None or isinstance(track, Live.Track.Track)
        if track != self._track:
            if self._track != None:
                volume = self._track.mixer_device.volume
                panning = self._track.mixer_device.panning
                sends = self._track.mixer_device.sends
                if volume.value_has_listener(self._on_volume_changed):
                    volume.remove_value_listener(self._on_volume_changed)
                if panning.value_has_listener(self._on_panning_changed):
                    panning.remove_value_listener(self._on_panning_changed)
                if len(sends) > 0 and sends[0].value_has_listener(self._on_send1_changed):
                    sends[0].remove_value_listener(self._on_send1_changed)
                if len(sends) > 1 and sends[1].value_has_listener(self._on_send2_changed):
                    sends[1].remove_value_listener(self._on_send2_changed)
            ChannelStripComponent.set_track(self, track)
        else:
            self.update()
        return

    def set_default_buttons(self, volume, panning, send1, send2):
        assert volume == None or isinstance(volume, ConfigurableButtonElement)
        assert panning == None or isinstance(panning, ConfigurableButtonElement)
        assert send1 == None or isinstance(send1, ConfigurableButtonElement)
        assert send2 == None or isinstance(send2, ConfigurableButtonElement)
        if volume != self._default_volume_button:
            if self._default_volume_button != None:
                self._default_volume_button.remove_value_listener(self._default_volume_value)
            self._default_volume_button = volume
            if self._default_volume_button != None:
                self._default_volume_button.add_value_listener(self._default_volume_value)
        if panning != self._default_panning_button:
            if self._default_panning_button != None:
                self._default_panning_button.remove_value_listener(self._default_panning_value)
            self._default_panning_button = panning
            if self._default_panning_button != None:
                self._default_panning_button.add_value_listener(self._default_panning_value)
        if send1 != self._default_send1_button:
            if self._default_send1_button != None:
                self._default_send1_button.remove_value_listener(self._default_send1_value)
            self._default_send1_button = send1
            if self._default_send1_button != None:
                self._default_send1_button.add_value_listener(self._default_send1_value)
        if send2 != self._default_send2_button:
            if self._default_send2_button != None:
                self._default_send2_button.remove_value_listener(self._default_send2_value)
            self._default_send2_button = send2
            if self._default_send2_button != None:
                self._default_send2_button.add_value_listener(self._default_send2_value)
        self.update()
        return

    def set_send_controls(self, controls):
        assert controls == None or isinstance(controls, tuple)
        if controls != self._send_controls:
            self._send_controls = controls
            if self._send_controls != None:
                for control in self._send_controls:
                    if control != None:
                        control.reset()

            self.update()
        return

    def update(self):
        super(DefChannelStripComponent, self).update()
        if self._allow_updates:
            if self.is_enabled():
                if self._track != None:
                    volume = self._track.mixer_device.volume
                    panning = self._track.mixer_device.panning
                    sends = self._track.mixer_device.sends
                    if not volume.value_has_listener(self._on_volume_changed):
                        volume.add_value_listener(self._on_volume_changed)
                    if not panning.value_has_listener(self._on_panning_changed):
                        panning.add_value_listener(self._on_panning_changed)
                    if len(sends) > 0:
                        if not sends[0].value_has_listener(self._on_send1_changed):
                            sends[0].add_value_listener(self._on_send1_changed)
                        self._on_send1_changed()
                    elif self._default_send1_button != None:
                        self._default_send1_button.turn_off()
                    if len(sends) > 1:
                        if not sends[1].value_has_listener(self._on_send2_changed):
                            sends[1].add_value_listener(self._on_send2_changed)
                        self._on_send2_changed()
                    elif self._default_send2_button != None:
                        self._default_send2_button.turn_off()
                    self._on_volume_changed()
                    self._on_panning_changed()
                else:
                    if self._default_volume_button != None:
                        self._default_volume_button.reset()
                    if self._default_panning_button != None:
                        self._default_panning_button.reset()
                    if self._default_send1_button != None:
                        self._default_send1_button.reset()
                    if self._default_send2_button != None:
                        self._default_send2_button.reset()
                    if self._mute_button != None:
                        self._mute_button.reset()
                    if self._arm_button != None:
                        self._arm_button.reset()
                    if self._solo_button != None:
                        self._solo_button.reset()
                    if self._volume_control != None:
                        self._volume_control.reset()
                    if self._pan_control != None:
                        self._pan_control.reset()
                    if self._send_controls != None:
                        for send_control in self._send_controls:
                            if send_control != None:
                                send_control.reset()

        return

    def _default_volume_value(self, value):
        if not self._default_volume_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and self._track != None and (value != 0 or not self._default_volume_button.is_momentary()):
                volume = self._track.mixer_device.volume
                if volume.is_enabled:
                    volume.value = volume.default_value
        return

    def _default_panning_value(self, value):
        if not self._default_panning_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and self._track != None and (value != 0 or not self._default_panning_button.is_momentary()):
                panning = self._track.mixer_device.panning
                if panning.is_enabled:
                    panning.value = panning.default_value
        return

    def _default_send1_value(self, value):
        if not self._default_send1_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and self._track != None and len(self._track.mixer_device.sends) > 0 and (value != 0 or not self._default_send1_button.is_momentary()):
                send1 = self._track.mixer_device.sends[0]
                if send1.is_enabled:
                    send1.value = send1.default_value
        return

    def _default_send2_value(self, value):
        if not self._default_send2_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and self._track != None and len(self._track.mixer_device.sends) > 1 and (value != 0 or not self._default_send2_button.is_momentary()):
                send2 = self._track.mixer_device.sends[1]
                if send2.is_enabled:
                    send2.value = send2.default_value
        return

    def _on_mute_changed(self):
        if self.is_enabled() and self._mute_button != None:
            if self._track != None:
                if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute != self._invert_mute_feedback:
                    self._mute_button.turn_on()
                else:
                    self._mute_button.turn_off()
            else:
                self._mute_button.send_value(0)
        return

    def _on_solo_changed(self):
        if self.is_enabled() and self._solo_button != None:
            if self._track != None:
                if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.solo:
                    self._solo_button.turn_on()
                else:
                    self._solo_button.turn_off()
            else:
                self._solo_button.send_value(0)
        return

    def _on_arm_changed(self):
        if self.is_enabled() and self._arm_button != None:
            if self._track != None:
                if self._track in self.song().tracks and self._track.can_be_armed and self._track.arm:
                    self._arm_button.turn_on()
                else:
                    self._arm_button.turn_off()
            else:
                self._arm_button.send_value(0)
        return

    def _on_volume_changed(self):
        assert self._track != None
        if self.is_enabled() and self._default_volume_button != None:
            volume = self._track.mixer_device.volume
            if volume.value == volume.default_value:
                self._default_volume_button.turn_on()
            else:
                self._default_volume_button.turn_off()
        return

    def _on_panning_changed(self):
        assert self._track != None
        if self.is_enabled() and self._default_panning_button != None:
            panning = self._track.mixer_device.panning
            if panning.value == panning.default_value:
                self._default_panning_button.turn_on()
            else:
                self._default_panning_button.turn_off()
        return

    def _on_send1_changed(self):
        assert self._track != None
        sends = self._track.mixer_device.sends
        assert len(sends) > 0
        if self.is_enabled() and self._default_send1_button != None:
            send1 = sends[0]
            if send1.value == send1.default_value:
                self._default_send1_button.turn_on()
            else:
                self._default_send1_button.turn_off()
        return

    def _on_send2_changed(self):
        assert self._track != None
        sends = self._track.mixer_device.sends
        assert len(sends) > 1
        if self.is_enabled() and self._default_send2_button != None:
            send2 = sends[1]
            if send2.value == send2.default_value:
                self._default_send2_button.turn_on()
            else:
                self._default_send2_button.turn_off()
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad/DefChannelStripComponent.pyc
