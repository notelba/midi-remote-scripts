# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialDeviceComponent.py
# Compiled at: 2017-09-30 15:26:23
import Live
NavDirection = Live.Application.Application.View.NavDirection
from _Framework.DeviceComponent import DeviceComponent, subject_slot
from _Framework.Control import ButtonControl
from _Framework.Util import nop
from _Framework import Task
from ShowMessageMixin import ShowMessageMixin, DisplayType
from SpecialControl import SpecialButtonControl
from ControlUtils import release_parameters, is_button_pressed
from Utils import live_object_is_valid, increment_selected_chain, get_enclosing_rack
BANK_LENGTH = 8
EMPTY_BANK = [ None for _ in xrange(BANK_LENGTH) ]

class SpecialDeviceComponent(DeviceComponent, ShowMessageMixin):
    """ SpecialDeviceComponent extends standard to include the ability to have more than
    8 parameter controls, device navigation controls, momentary/toggle on/off button and
    better skin support. """
    d = dict(color='Navigation.DeviceEnabled', pressed_color='Navigation.Pressed', disabled_color='Navigation.Disabled')
    device_left_button = ButtonControl(**d)
    device_right_button = ButtonControl(**d)
    device_on_off_button = SpecialButtonControl(color='Device.Off', on_color='Device.On', disabled_color='Device.NoDevice')

    def __init__(self, follow_track=True, targets_comp=None, bank_always=False, name='Device_Control', from_test=False, *a, **k):
        self._bank_always = bool(bank_always)
        self._bank_index = 0
        self._bank_name = '<No Bank>'
        self._suppress_show_msg = True
        super(SpecialDeviceComponent, self).__init__(device_selection_follows_track_selection=follow_track, name=name, *a, **k)
        if not from_test:
            self._show_msg_callback = self.canonical_parent.show_message
        self._parameter_controls = []
        self._empty_control_slots = self.register_slot_manager()
        self._num_filled_banks = 0
        self._on_toggle_lock_to_item.subject = targets_comp
        self._show_msg_callback = self._handle_show_msg
        self._unsuppress_show_msg_task = self._tasks.add(Task.run(self._unsuppress_show_msg))
        self._unsuppress_show_msg_task.kill()
        self._shift_button = None
        return

    def disconnect(self):
        super(SpecialDeviceComponent, self).disconnect()
        self._unsuppress_show_msg_task = None
        self._shift_button = None
        return

    def set_parameter_controls(self, controls):
        """ Extends standard to set num filled banks. """
        filled = [ p for p in controls if p ] if controls else None
        self._num_filled_banks = len(filled) / BANK_LENGTH if filled else 0
        self._suppress_show_msg = True
        super(SpecialDeviceComponent, self).set_parameter_controls(controls)
        return

    def set_parameter_controls_a(self, controls):
        """ Sets the controls to use for controlling the 1st set of 8 parameters. """
        self._set_parameter_controls(controls, 0)

    def set_parameter_controls_b(self, controls):
        """ Sets the controls to use for controlling the 2nd set of 8 parameters. """
        self._set_parameter_controls(controls, BANK_LENGTH)

    def set_parameter_controls_c(self, controls):
        """ Sets the controls to use for controlling the 3rd set of 8 parameters. """
        self._set_parameter_controls(controls, BANK_LENGTH * 2)

    def set_parameter_controls_d(self, controls):
        """ Sets the controls to use for controlling the 4th set of 8 parameters. """
        self._set_parameter_controls(controls, BANK_LENGTH * 3)

    def _set_parameter_controls(self, controls, insert_start):
        self._suppress_show_msg = True
        if self._parameter_controls is not None:
            release_parameters(self._parameter_controls)
            controls = controls or EMPTY_BANK
            num_current = len(self._parameter_controls)
            insert_end = insert_start + BANK_LENGTH
            if insert_end > num_current:
                num_to_pad = (insert_end - num_current) / BANK_LENGTH - 1
                for _ in xrange(num_to_pad):
                    self._parameter_controls.extend(EMPTY_BANK)

                self._parameter_controls.extend(controls)
            else:
                for index, control in enumerate(controls):
                    self._parameter_controls[index + insert_start] = control

            filled = [ p for p in self._parameter_controls if p ]
            self._num_filled_banks = len(filled) / BANK_LENGTH if filled else 0
            self.update()
        return

    def set_bank_nav_buttons(self, down_button, up_button):
        """ Overrides standard to always call method to update LEDs. """
        super(SpecialDeviceComponent, self).set_bank_nav_buttons(down_button, up_button)
        self._update_device_bank_nav_buttons()

    def set_shift_button(self, button):
        """ Sets the shift modifier to use for changing the functionality of
        dev left/right to nav chains and hide/show chains. """
        self._shift_button = button

    @device_left_button.pressed
    def device_left_button(self, _):
        self._navigate_devices(NavDirection.left)

    @device_right_button.pressed
    def device_right_button(self, _):
        self._navigate_devices(NavDirection.right)

    @subject_slot('toggle_lock_to_item')
    def _on_toggle_lock_to_item(self):
        """ Handles alternate form of locking via TargetsComponent. """
        if self._lock_callback:
            self._lock_callback()

    def set_lock_to_device(self, lock, device):
        """ Extends standard to display lock status on physical display. """
        super(SpecialDeviceComponent, self).set_lock_to_device(lock, device)
        self.component_message('Locked To' if self._locked_to_device else 'Unlocked From', device.name, display_type=DisplayType.PHYSICAL)

    def _navigate_devices(self, direction):
        view = self.application().view
        if not view.is_view_visible('Detail') or not view.is_view_visible('Detail/DeviceChain'):
            view.show_view('Detail')
            view.show_view('Detail/DeviceChain')
        elif is_button_pressed(self._shift_button):
            rack = get_enclosing_rack(self._device)
            if rack:
                if direction == NavDirection.right:
                    if rack.view.is_showing_chain_devices:
                        increment_selected_chain(rack, 1, wrap=True, show_msg=self.component_message)
                    else:
                        rack.view.is_showing_chain_devices = True
                else:
                    rack.view.is_showing_chain_devices = False
        else:
            view.scroll_view(direction, 'Detail/DeviceChain', False)

    @device_on_off_button.pressed
    def device_on_off_button(self, _):
        self._toggle_device_state()

    @device_on_off_button.released_delayed
    def device_on_off_button(self, _):
        self._toggle_device_state()

    @device_on_off_button.pressed_delayed
    def device_on_off_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    @device_on_off_button.released_immediately
    def device_on_off_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    def _toggle_device_state(self):
        if self.is_enabled() and self._device:
            parameter = self._on_off_parameter()
            if parameter and parameter.is_enabled:
                parameter.value = float(int(parameter.value == 0.0))

    def _bank_up_value(self, value):
        """ Overrides standard to properly deal with more than 8 parameter controls. """
        if self.is_enabled() and self._device and value and self._can_bank_up():
            self._increment_bank_index(1)

    def _bank_down_value(self, value):
        """ Overrides standard to properly deal with more than 8 parameter controls. """
        if self.is_enabled() and self._device and value and self._can_bank_down():
            self._increment_bank_index(-1)

    def _increment_bank_index(self, delta):
        delta = self._num_filled_banks * delta
        self._bank_name = ''
        self._bank_index = max(0, min(self._number_of_parameter_banks() - 1, self._bank_index + delta))
        self.update()

    def update(self):
        """ Extends standard to not update if no controls assigned. """
        if self._num_filled_banks == 0:
            return
        self._empty_control_slots.disconnect()
        super(SpecialDeviceComponent, self).update()

    def _update_on_off_button(self):
        """ Overrides standard to update customized on/off button. """
        if self.is_enabled():
            enable = False
            turn_on = False
            if self._device:
                enable = True
                parameter = self._on_off_parameter()
                turn_on = parameter and parameter.value
            self.device_on_off_button.enabled = enable
            self.device_on_off_button.is_on = turn_on

    def _update_device_bank_nav_buttons(self):
        """ Overrides standard to use skin values and properly deal with more than 8
        parameter controls. """
        if self.is_enabled():
            if self._bank_up_button:
                value_to_send = 'Device.NoDevice'
                if self._device:
                    value_to_send = 'Device.BankEnabled' if self._can_bank_up() else 'Device.BankDisabled'
                self._bank_up_button.set_light(value_to_send)
            if self._bank_down_button:
                value_to_send = 'Device.NoDevice'
                if self._device:
                    value_to_send = 'Device.BankEnabled' if self._can_bank_down() else 'Device.BankDisabled'
                self._bank_down_button.set_light(value_to_send)

    def _can_bank_up(self):
        num_banks = self._number_of_parameter_banks()
        return self._bank_index is None or num_banks > self._bank_index + self._num_filled_banks

    def _can_bank_down(self):
        return self._bank_index is None or self._bank_index > 0

    def _is_banking_enabled(self):
        """ Extends standard to always return true if elected. """
        if self._bank_always:
            return True
        return super(SpecialDeviceComponent, self)._is_banking_enabled()

    def _assign_parameters(self):
        """ Overrides standard to add listeners for unused controls to prevent
        leaking. """
        assert self.is_enabled()
        assert self._device is not None
        assert self._parameter_controls is not None
        self._bank_name, bank = self._current_bank_details()
        for control, parameter in zip(self._parameter_controls, bank):
            if control is not None:
                if live_object_is_valid(parameter):
                    control.connect_to(parameter)
                else:
                    control.release_parameter()
                    self._empty_control_slots.register_slot(control, nop, 'value')

        self._release_parameters(self._parameter_controls[len(bank):])
        return

    def _release_parameters(self, controls):
        """ Extends standard to add listeners for unused controls to prevent leaking. """
        super(SpecialDeviceComponent, self)._release_parameters(controls)
        if controls:
            for control in controls:
                if control:
                    self._empty_control_slots.register_slot(control, nop, 'value')

    def _current_bank_details(self):
        """ Overrides standard to assign multiple banks of parameters where possible. """
        bank_name = self._bank_name
        bank = []
        best_of = self._best_of_parameter_bank()
        banks = self._parameter_banks()
        if banks:
            num_extra_control_banks = self._num_filled_banks - 1
            if self._bank_index is not None or not best_of:
                index = self._bank_index if self._bank_index is not None else 0
                bank = list(banks[index])
                bank_name = self._parameter_bank_names()[index]
                num_extra_param_banks = self._number_of_parameter_banks() - index - 1
                for i in xrange(num_extra_param_banks):
                    target_index = index + i + 1
                    if i < num_extra_control_banks:
                        bank.extend(banks[target_index])
                        bank_name += '   /   %s' % self._parameter_bank_names()[target_index]

            else:
                bank = best_of
                bank_name = 'Best of Parameters'
        return (
         bank_name, bank)

    def _unsuppress_show_msg(self):
        self._suppress_show_msg = False

    def _handle_show_msg(self, _):
        """ Hack that overrides the base component's usage of show_msg_callback so that
        it follows the format used by the rest of the framework and can also be
        suppressed while controls are being set on the component. """
        self._unsuppress_show_msg_task.kill()
        if self._suppress_show_msg:
            self._unsuppress_show_msg_task.restart()
        else:
            self._show_msg(self.canonical_parent.show_message, 'Device', self._device.name, 'Bank', self._bank_name, DisplayType.BOTH)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialDeviceComponent.pyc
