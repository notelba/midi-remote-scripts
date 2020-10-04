# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launch_Control_XL\DeviceComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Control import control_list, ButtonControl
from _Framework.DeviceComponent import DeviceComponent as DeviceComponentBase
from _Framework.ModesComponent import EnablingModesComponent, tomode

class DeviceComponent(DeviceComponentBase):
    parameter_lights = control_list(ButtonControl, control_count=8, enabled=False, color=b'Device.Parameters', disabled_color=b'Device.NoDevice')
    prev_device_button = ButtonControl(color=b'DefaultButton.On')
    next_device_button = ButtonControl(color=b'DefaultButton.On')

    @prev_device_button.pressed
    def prev_device_button(self, button):
        self._scroll_device_view(Live.Application.Application.View.NavDirection.left)

    @next_device_button.pressed
    def next_device_button(self, button):
        self._scroll_device_view(Live.Application.Application.View.NavDirection.right)

    def _scroll_device_view(self, direction):
        self.application().view.show_view(b'Detail')
        self.application().view.show_view(b'Detail/DeviceChain')
        self.application().view.scroll_view(direction, b'Detail/DeviceChain', False)

    def set_device(self, device):
        super(DeviceComponent, self).set_device(device)
        for light in self.parameter_lights:
            light.enabled = bool(device)

    def set_bank_buttons(self, buttons):
        for button in buttons or []:
            if button:
                button.set_on_off_values(b'Device.BankSelected', b'Device.BankUnselected')

        super(DeviceComponent, self).set_bank_buttons(buttons)

    def _is_banking_enabled(self):
        return True


class DeviceModeComponent(EnablingModesComponent):
    device_mode_button = ButtonControl()

    def __init__(self, device_settings_mode=None, *a, **k):
        super(DeviceModeComponent, self).__init__(*a, **k)
        assert device_settings_mode is not None
        self._device_settings_mode = tomode(device_settings_mode)
        return

    @device_mode_button.released_immediately
    def device_mode_button(self, button):
        self.cycle_mode()

    @device_mode_button.pressed_delayed
    def device_mode_button(self, button):
        self.selected_mode = b'enabled'
        self._device_settings_mode.enter_mode()

    @device_mode_button.released_delayed
    def device_mode_button(self, button):
        self._device_settings_mode.leave_mode()

    def _update_buttons(self, selected_mode):
        self.device_mode_button.color = b'DefaultButton.On' if selected_mode == b'enabled' else b'DefaultButton.Off'
        super(DeviceModeComponent, self)._update_buttons(selected_mode)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launch_Control_XL/DeviceComponent.pyc
