# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV2_LX2_LC2_LD2\FaderfoxScript.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live, sys
from .consts import *
from .FaderfoxHelper import FaderfoxHelper
from .ParamMap import ParamMap
from .Devices import *
from _Generic.util import DeviceAppointer

class FaderfoxScript:
    __filter_funcs__ = [
     b'update_display', b'log', b'song']
    __module__ = __name__
    __doc__ = b'Automap script for Faderfox controllers'
    __version__ = b'V1.1'
    __name__ = b'Generic Faderfox Script'

    def __init__(self, c_instance):
        self.suffix = b''
        self.is_lv1 = False
        FaderfoxScript.realinit(self, c_instance)

    def realinit(self, c_instance):
        self.c_instance = c_instance
        self.helper = FaderfoxHelper(self)
        self.param_map = ParamMap(self)
        self.mixer_controller = None
        self.device_controller = None
        self.transport_controller = None
        self.components = []
        live = b'Live 6 & 7'
        if self.is_live_5():
            live = b'Live 5'
        self.show_message(self.__name__ + b' ' + self.__version__ + b' for ' + live)
        self.is_lv1 = False
        self._device_appointer = DeviceAppointer(song=self.song(), appointed_device_setter=self._set_appointed_device)
        return

    def is_live_5(self):
        return hasattr(Live, b'is_live_5')

    def log(self, string):
        pass

    def logfmt(self, fmt, *args):
        pass

    def disconnect(self):
        for c in self.components:
            c.disconnect()

        self._device_appointer.disconnect()

    def application(self):
        return Live.Application.get_application()

    def song(self):
        return self.c_instance.song()

    def suggest_input_port(self):
        return str(b'')

    def suggest_output_port(self):
        return str(b'')

    def can_lock_to_devices(self):
        return True

    def lock_to_device(self, device):
        if self.device_controller:
            self.device_controller.lock_to_device(device)

    def unlock_to_device(self, device):
        if self.device_controller:
            self.device_controller.unlock_from_device(device)

    def _set_appointed_device(self, device):
        if self.device_controller:
            self.device_controller.set_appointed_device(device)

    def toggle_lock(self):
        self.c_instance.toggle_lock()

    def suggest_map_mode(self, cc_no, channel):
        return Live.MidiMap.MapMode.absolute

    def restore_bank(self, bank):
        pass

    def show_message(self, message):
        if hasattr(self.c_instance, b'show_message'):
            self.c_instance.show_message(message)

    def instance_identifier(self):
        return self.c_instance.instance_identifier()

    def connect_script_instances(self, instanciated_scripts):
        pass

    def request_rebuild_midi_map(self):
        self.c_instance.request_rebuild_midi_map()

    def send_midi(self, midi_event_bytes):
        self.c_instance.send_midi(midi_event_bytes)

    def refresh_state(self):
        for c in self.components:
            c.refresh_state()

    def build_midi_map(self, midi_map_handle):
        self.log(b'script build midi map')
        script_handle = self.c_instance.handle()
        self.param_map.remove_mappings()
        for c in self.components:
            self.log(b'build midi map on %s' % c)
            c.build_midi_map(script_handle, midi_map_handle)

    def update_display(self):
        for c in self.components:
            c.update_display()

    def receive_midi(self, midi_bytes):
        channel = midi_bytes[0] & CHAN_MASK
        status = midi_bytes[0] & STATUS_MASK
        if status == CC_STATUS:
            cc_no = midi_bytes[1]
            cc_value = midi_bytes[2]
            for c in self.components:
                c.receive_midi_cc(channel, cc_no, cc_value)

            self.param_map.receive_midi_cc(channel, cc_no, cc_value)
        elif status == NOTEON_STATUS or status == NOTEOFF_STATUS:
            note_no = midi_bytes[1]
            note_vel = midi_bytes[2]
            for c in self.components:
                c.receive_midi_note(channel, status, note_no, note_vel)

            self.param_map.receive_midi_note(channel, status, note_no, note_vel)
        else:
            assert False, b'Unknown MIDI message %s' % str(midi_bytes)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/LV2_LX2_LC2_LD2/FaderfoxScript.pyc
