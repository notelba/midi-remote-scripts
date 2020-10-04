# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\TrackFilterComponent.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.EncoderElement import EncoderElement
from _Generic.Devices import get_parameter_by_name
FILTER_DEVICES = {b'AutoFilter': {b'Frequency': b'Frequency', b'Resonance': b'Resonance'}, b'Operator': {b'Frequency': b'Filter Freq', b'Resonance': b'Filter Res'}, b'OriginalSimpler': {b'Frequency': b'Filter Freq', b'Resonance': b'Filter Res'}, b'MultiSampler': {b'Frequency': b'Filter Freq', b'Resonance': b'Filter Res'}, b'UltraAnalog': {b'Frequency': b'F1 Freq', b'Resonance': b'F1 Resonance'}, b'StringStudio': {b'Frequency': b'Filter Freq', b'Resonance': b'Filter Reso'}}

class TrackFilterComponent(ControlSurfaceComponent):
    """ Class representing a track's filter, attaches to the last filter in the track """

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._track = None
        self._device = None
        self._freq_control = None
        self._reso_control = None
        return

    def disconnect(self):
        if self._freq_control != None:
            self._freq_control.release_parameter()
            self._freq_control = None
        if self._reso_control != None:
            self._reso_control.release_parameter()
            self._reso_control = None
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            self._track = None
        self._device = None
        return

    def on_enabled_changed(self):
        self.update()

    def set_track(self, track):
        assert track == None or isinstance(track, Live.Track.Track)
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            if self._device != None:
                if self._freq_control != None:
                    self._freq_control.release_parameter()
                if self._reso_control != None:
                    self._reso_control.release_parameter()
        self._track = track
        if self._track != None:
            self._track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()
        return

    def set_filter_controls(self, freq, reso):
        assert isinstance(freq, EncoderElement)
        assert isinstance(freq, EncoderElement)
        if self._device != None:
            if self._freq_control != None:
                self._freq_control.release_parameter()
            if self._reso_control != None:
                self._reso_control.release_parameter()
        self._freq_control = freq
        self._reso_control = reso
        self.update()
        return

    def update(self):
        super(TrackFilterComponent, self).update()
        if self.is_enabled() and self._device != None:
            device_dict = FILTER_DEVICES[self._device.class_name]
            if self._freq_control != None:
                self._freq_control.release_parameter()
                parameter = get_parameter_by_name(self._device, device_dict[b'Frequency'])
                if parameter != None:
                    self._freq_control.connect_to(parameter)
            if self._reso_control != None:
                self._reso_control.release_parameter()
                parameter = get_parameter_by_name(self._device, device_dict[b'Resonance'])
                if parameter != None:
                    self._reso_control.connect_to(parameter)
        return

    def _on_devices_changed(self):
        self._device = None
        if self._track != None:
            for index in range(len(self._track.devices)):
                device = self._track.devices[(-1 * (index + 1))]
                if device.class_name in FILTER_DEVICES.keys():
                    self._device = device
                    break

        self.update()
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/VCM600/TrackFilterComponent.pyc
