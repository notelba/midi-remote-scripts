# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\TrackEQComponent.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.EncoderElement import EncoderElement
from _Generic.Devices import get_parameter_by_name
EQ_DEVICES = {b'Eq8': {b'Gains': [ b'%i Gain A' % (index + 1) for index in range(8) ]}, b'FilterEQ3': {b'Gains': [
                           b'GainLo', b'GainMid', b'GainHi'], 
                  b'Cuts': [
                          b'LowOn', b'MidOn', b'HighOn']}}

class TrackEQComponent(ControlSurfaceComponent):
    """ Class representing a track's EQ, it attaches to the last EQ device in the track """

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._track = None
        self._device = None
        self._gain_controls = None
        self._cut_buttons = None
        return

    def disconnect(self):
        if self._gain_controls != None:
            for control in self._gain_controls:
                control.release_parameter()

            self._gain_controls = None
        if self._cut_buttons != None:
            for button in self._cut_buttons:
                button.remove_value_listener(self._cut_value)

        self._cut_buttons = None
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            self._track = None
        self._device = None
        if self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if b'Cuts' in device_dict.keys():
                cut_names = device_dict[b'Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter != None and parameter.value_has_listener(self._on_cut_changed):
                        parameter.remove_value_listener(self._on_cut_changed)

        return

    def on_enabled_changed(self):
        self.update()

    def set_track(self, track):
        assert track == None or isinstance(track, Live.Track.Track)
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            if self._gain_controls != None and self._device != None:
                for control in self._gain_controls:
                    control.release_parameter()

        self._track = track
        if self._track != None:
            self._track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()
        return

    def set_cut_buttons(self, buttons):
        assert buttons == None or isinstance(buttons, tuple)
        if buttons != self._cut_buttons:
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    button.remove_value_listener(self._cut_value)

            self._cut_buttons = buttons
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    button.add_value_listener(self._cut_value, identify_sender=True)

            self.update()
        return

    def set_gain_controls(self, controls):
        assert controls != None
        assert isinstance(controls, tuple)
        if self._device != None and self._gain_controls != None:
            for control in self._gain_controls:
                control.release_parameter()

        for control in controls:
            assert control != None
            assert isinstance(control, EncoderElement)

        self._gain_controls = controls
        self.update()
        return

    def update(self):
        super(TrackEQComponent, self).update()
        if self.is_enabled() and self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if self._gain_controls != None:
                gain_names = device_dict[b'Gains']
                for index in range(len(self._gain_controls)):
                    self._gain_controls[index].release_parameter()
                    if len(gain_names) > index:
                        parameter = get_parameter_by_name(self._device, gain_names[index])
                        if parameter != None:
                            self._gain_controls[index].connect_to(parameter)

            if self._cut_buttons != None and b'Cuts' in device_dict.keys():
                cut_names = device_dict[b'Cuts']
                for index in range(len(self._cut_buttons)):
                    self._cut_buttons[index].turn_off()
                    if len(cut_names) > index:
                        parameter = get_parameter_by_name(self._device, cut_names[index])
                        if parameter != None:
                            if parameter.value == 0.0:
                                self._cut_buttons[index].turn_on()
                            if not parameter.value_has_listener(self._on_cut_changed):
                                parameter.add_value_listener(self._on_cut_changed)

        else:
            if self._cut_buttons != None:
                for button in self._cut_buttons:
                    if button != None:
                        button.turn_off()

            if self._gain_controls != None:
                for control in self._gain_controls:
                    control.release_parameter()

        return

    def _cut_value(self, value, sender):
        if not sender in self._cut_buttons:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and self._device != None and (not sender.is_momentary() or value is not 0):
                device_dict = EQ_DEVICES[self._device.class_name]
                if b'Cuts' in device_dict.keys():
                    cut_names = device_dict[b'Cuts']
                    index = list(self._cut_buttons).index(sender)
                    if index in range(len(cut_names)):
                        parameter = get_parameter_by_name(self._device, cut_names[index])
                        if parameter != None and parameter.is_enabled:
                            parameter.value = float(int(parameter.value + 1) % 2)
        return

    def _on_devices_changed(self):
        if self._device != None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if b'Cuts' in device_dict.keys():
                cut_names = device_dict[b'Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter != None and parameter.value_has_listener(self._on_cut_changed):
                        parameter.remove_value_listener(self._on_cut_changed)

        self._device = None
        if self._track != None:
            for index in range(len(self._track.devices)):
                device = self._track.devices[(-1 * (index + 1))]
                if device.class_name in EQ_DEVICES.keys():
                    self._device = device
                    break

        self.update()
        return

    def _on_cut_changed(self):
        assert self._device != None
        assert b'Cuts' in EQ_DEVICES[self._device.class_name].keys()
        if self.is_enabled() and self._cut_buttons != None:
            cut_names = EQ_DEVICES[self._device.class_name][b'Cuts']
            for index in range(len(self._cut_buttons)):
                self._cut_buttons[index].turn_off()
                if len(cut_names) > index:
                    parameter = get_parameter_by_name(self._device, cut_names[index])
                    if parameter != None and parameter.value == 0.0:
                        self._cut_buttons[index].turn_on()

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/VCM600/TrackEQComponent.pyc
