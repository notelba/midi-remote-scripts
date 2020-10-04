# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\device.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import clamp, listens
from ableton.v2.control_surface import ParameterInfo
from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v2.control_surface.control import ButtonControl
from .parameter_mapping_sensitivities import parameter_mapping_sensitivity

class DeviceComponent(DeviceComponentBase):
    __events__ = ('bank', )
    prev_bank_button = ButtonControl(color=b'Device.On')
    next_bank_button = ButtonControl(color=b'Device.On')

    def __init__(self, *a, **k):
        super(DeviceComponent, self).__init__(*a, **k)
        self.__on_bank_changed.subject = self._device_bank_registry
        self._update_bank_scroll_buttons()

    @prev_bank_button.pressed
    def prev_bank_button(self, _):
        self._scroll_bank(-1)

    @next_bank_button.pressed
    def next_bank_button(self, _):
        self._scroll_bank(1)

    def _set_device(self, device):
        super(DeviceComponent, self)._set_device(device)
        self._update_bank_scroll_buttons()

    def _create_parameter_info(self, parameter, name):
        return ParameterInfo(parameter=parameter, name=name, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter, self.device().class_name))

    @listens(b'device_bank')
    def __on_bank_changed(self, device, bank):
        if device == self.device():
            self._set_bank_index(bank)
            self._update_bank_scroll_buttons()
        self.notify_bank()

    def _update_bank_scroll_buttons(self):
        bank = self._bank
        self.prev_bank_button.enabled = bank is not None and bank.index > 0
        self.next_bank_button.enabled = bank is not None and bank.index < bank.bank_count() - 1
        return

    def _scroll_bank(self, offset):
        if self._bank:
            new_index = clamp(self._bank.index + offset, 0, self._bank.bank_count() - 1)
            self._device_bank_registry.set_device_bank(self.device(), new_index)
            self._set_bank_index(new_index)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/SL_MkIII/device.pyc
