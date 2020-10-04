# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\device.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import clamp, listens, liveobj_valid
from ableton.v2.control_surface import ParameterInfo
from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v2.control_surface.control import ButtonControl, TextDisplayControl, ToggleButtonControl

class DeviceComponent(DeviceComponentBase):
    prev_bank_button = ButtonControl(color=b'Action.Off', pressed_color=b'Action.On')
    next_bank_button = ButtonControl(color=b'Action.Off', pressed_color=b'Action.On')
    bank_name_display = TextDisplayControl()
    device_lock_button = ToggleButtonControl()

    def __init__(self, toggle_lock=None, *a, **k):
        super(DeviceComponent, self).__init__(*a, **k)
        assert toggle_lock is not None
        self._toggle_lock = toggle_lock
        self.__on_is_locked_to_device_changed.subject = self._device_provider
        self.__on_is_locked_to_device_changed()
        return

    @prev_bank_button.pressed
    def prev_bank_button(self, _):
        self._scroll_bank(-1)

    @next_bank_button.pressed
    def next_bank_button(self, _):
        self._scroll_bank(1)

    @device_lock_button.toggled
    def device_lock_button(self, toggled, _):
        self._toggle_lock()
        self._update_device_lock_button()

    def _create_parameter_info(self, parameter, name):
        return ParameterInfo(parameter=parameter, name=name, default_encoder_sensitivity=1.0)

    def _set_bank_index(self, index):
        super(DeviceComponent, self)._set_bank_index(index)
        self._update_bank_name_display()

    def _scroll_bank(self, offset):
        bank = self._bank
        if bank:
            new_index = clamp(bank.index + offset, 0, bank.bank_count() - 1)
            self._device_bank_registry.set_device_bank(self.device(), new_index)

    def _update_bank_name_display(self):
        bank_name = b''
        device = self.device()
        if liveobj_valid(device):
            device_bank_names = self._banking_info.device_bank_names(device)
            if device_bank_names:
                bank_name = device_bank_names[self._device_bank_registry.get_device_bank(device)]
        self.bank_name_display[0] = bank_name

    def _update_device_lock_button(self):
        self.device_lock_button.is_toggled = self._device_provider.is_locked_to_device

    @listens(b'is_locked_to_device')
    def __on_is_locked_to_device_changed(self):
        self._update_device_lock_button()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/device.pyc
