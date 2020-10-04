# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\UserDevicesComponent.py
# Compiled at: 2017-03-07 13:28:53
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot
from PageSelector import PageSelector, Pageable
from ShowMessageMixin import ShowMessageMixin
from ControlUtils import release_parameters, parameter_is_quantized
from Utils import live_object_is_valid, get_device_parameter
DEV_ID_POS = 0
PARAM_NAME_POS = 1
BTN_TYPE_POS = 2
BTN_OFF_POS = 3
BTN_ON_POS = 4

class UserDevicesComponent(ControlSurfaceComponent):
    """ UserDevicesComponent allows specific devices to be controlled on a track.  This
    is meant to be used in conjunction with another component that handles setting the
    track to use as well as the page of parameter to control.

    dev_class_names = Tuple of device class names.

    dev_ins_names =   Tuple of device instance names to allow for devices of a class
                      with a particular name to be retrieved. This tuple has to be the
                      the same length as dev_class_names. Use None in cases where
                      instance name should be ignored.

    enc_mapping =     Tuple containing a tuple of tuples (one tuple per page)
                      for each encoder in the form: (dev_index, param_name)

    btn_mapping =     (Optional). Tuple containing a tuple of tuples (one tuple per page)
                      for each button in the form:
                      (dev_index, param_name, is_momentary, off_val, on_val)
    param_dict =      (Optional )Dict of device class names containing parameter names
                      and number of toggle steps for button control.

    # NOTES:
    # -- Cannot bind multiple encoders to the same parameter.
    # -- Can bind a button and encoder to the same parameter.
    """
    __subject_events__ = ('devices', 'track', 'encoder_parameters', 'button_parameters')

    def __init__(self, manager, dev_class_names, dev_ins_names, enc_mapping, btn_mapping=None, param_dict=None, targets_comp=None, name='User_Device_Control', *a, **k):
        assert isinstance(dev_class_names, tuple)
        assert isinstance(dev_ins_names, tuple) and len(dev_ins_names) == len(dev_class_names)
        assert isinstance(enc_mapping, tuple)
        assert btn_mapping is None or isinstance(btn_mapping, tuple)
        assert isinstance(param_dict, dict)
        super(UserDevicesComponent, self).__init__(name=name, *a, **k)
        self._param_dict = param_dict
        self._device_class_names = dev_class_names
        self._device_instance_names = dev_ins_names
        self._encoder_mapping = enc_mapping
        self._button_mapping = btn_mapping
        self._current_devices = [ None for _ in xrange(len(dev_class_names)) ]
        self._encoder_controls = None
        self._button_controls = None
        self._button_params = []
        self._page_index = 0
        self._track = None
        self._manager = manager
        self._on_device_list_changed.subject = manager
        self._on_track_changed.subject = targets_comp
        self.update()
        return

    def disconnect(self):
        release_parameters(self._encoder_controls)
        super(UserDevicesComponent, self).disconnect()
        self._param_dict = None
        self._device_class_names = None
        self._device_instance_names = None
        self._encoder_mapping = None
        self._button_mapping = None
        self._current_devices = None
        self._encoder_controls = None
        self._button_controls = None
        self._button_params = None
        return

    @property
    def devices(self):
        return [ d for d in self._current_devices if d is not None ]

    @property
    def track(self):
        return self._track

    @property
    def encoder_parameters(self):
        if self._encoder_controls:
            return [ None if e.mapped_parameter() is None else e.mapped_parameter() for e in self._encoder_controls
                   ]
        else:
            return []

    @property
    def button_parameters(self):
        return self._button_params

    @subject_slot('target_track')
    def _on_track_changed(self, track):
        self.set_track(track)

    def set_track(self, track):
        """ Extends standard to notify listeners on changes. """
        self._track = track
        self.notify_track()

    def set_page_index(self, index):
        """ Sets the page index to use and updates all connections. """
        self._page_index = index
        self._update_encoder_connections()
        self._update_button_connections()

    def set_encoder_controls(self, controls):
        """ Sets the encoders/knobs/faders to use for controlling parameters. """
        release_parameters(self._encoder_controls)
        self._encoder_controls = controls
        self._update_encoder_connections()

    def set_button_controls(self, controls):
        """ Sets the buttons to use for controlling parameters. """
        self._on_button_parameter_changed.replace_subjects([])
        self._button_controls = list(controls) if controls else None
        self._on_button_control_value.replace_subjects(controls or [])
        self._update_button_connections()
        return

    @subject_slot_group('value')
    def _on_button_control_value(self, value, button):
        """ Called when any button_control is pressed/released to either toggle values
        or increment values of quantized parameters. This provide momentary control
        if specified. """
        if self.is_enabled():
            button_index = self._button_controls.index(button)
            if value or self._button_mapping[button_index][self._page_index][BTN_TYPE_POS]:
                param = self._button_params[button_index]
                if param:
                    if parameter_is_quantized(param) or self._is_toggle_param(param):
                        factor = self._get_toggle_factor(param)
                        if param.value == param.max:
                            param.value = param.min
                        elif param.value + factor > param.max:
                            param.value = param.max
                        else:
                            param.value = param.value + factor
                    else:
                        param.value = param.min if param.value == param.max else param.max

    @subject_slot('devices')
    def _on_device_list_changed(self, track_changed=False):
        """ Called when either the track or list of devices on the track changes. Will
        trigger a full update if the current devices to control were changed
        (added/removed). """
        if self.is_enabled():
            new_devices = []
            i_name_list = self._device_instance_names
            for index, class_name in enumerate(self._device_class_names):
                new_device = self._manager.get_device_by_class_name(class_name, i_name_list[index])
                new_devices.append(new_device)

            devices_were_deleted = False
            for d in self._current_devices:
                if not live_object_is_valid(d):
                    devices_were_deleted = True

            if track_changed or devices_were_deleted or cmp(new_devices, self._current_devices):
                self._current_devices = new_devices
                self.notify_devices()
                self.set_page_index(self._page_index)

    def _update_encoder_connections(self):
        """ Connects encoders to specified parameters for the current page. """
        release_parameters(self._encoder_controls)
        if self.is_enabled() and self._encoder_controls:
            for index, control in enumerate(self._encoder_controls):
                if control:
                    param = self._get_parameter_for_control(control, self._encoder_mapping[index])
                    control.connect_to(param)

        self.notify_encoder_parameters()

    def _update_button_connections(self):
        """ Sets up listeners for button control specified parameters for the
        current page. """
        self._on_button_parameter_changed.replace_subjects([])
        self._button_params = []
        if self.is_enabled() and self._button_controls:
            self._button_params = [ None for index in xrange(len(self._button_controls)) ]
            for index, control in enumerate(self._button_controls):
                if control:
                    param = self._get_parameter_for_control(control, self._button_mapping[index])
                    if param:
                        self._button_params[index] = param
                    self._update_button_control_led(index)

            self._on_button_parameter_changed.replace_subjects(self._button_params)
        self.notify_button_parameters()
        return

    @subject_slot_group('value')
    def _on_button_parameter_changed(self, parameter):
        """ Called when any button control parameter changes to update the LED of the
        associated button. """
        if self.is_enabled():
            param_index = self._button_params.index(parameter)
            if self._button_controls and self._button_controls[param_index]:
                self._update_button_control_led(param_index)

    def _update_button_control_led(self, index):
        button = self._button_controls[index]
        param = self._button_params[index]
        turn_on = param and (param.max - param.min + param.min) / 2.0 <= param.value
        mapping = self._button_mapping[index][self._page_index]
        button.send_value(mapping[(BTN_ON_POS if turn_on else BTN_OFF_POS)])

    def _get_parameter_for_control(self, control, mapping):
        """ Returns the parameter to control for the given control for the current
        page. """
        mapping_page = mapping[self._page_index]
        device_id = mapping_page[DEV_ID_POS]
        target_device = None if device_id == -1 else self._current_devices[device_id]
        if control and target_device:
            return get_device_parameter(target_device, mapping_page[PARAM_NAME_POS])
        else:
            return

    def _is_toggle_param(self, param):
        """ Returns whether the given param is defined as a toggle param in the
        param_dict. """
        parent = 'MixerDevice' if type(param.canonical_parent) == Live.MixerDevice.MixerDevice else param.canonical_parent.class_name
        return parent in self._param_dict and param.original_name in self._param_dict[parent]

    def _get_toggle_factor(self, param):
        """ Returns the toggle factor to use for the given parameter. """
        if parameter_is_quantized(param):
            return 1
        else:
            parent = 'MixerDevice' if type(param.canonical_parent) == Live.MixerDevice.MixerDevice else param.canonical_parent.class_name
            return (param.max - param.min) / self._param_dict[parent][param.original_name]


class DedicatedDevicesComponent(UserDevicesComponent, Pageable, ShowMessageMixin):
    """ UserDevicesComponent that handles its own paging. """
    __subject_events__ = ('page_name', )

    def __init__(self, manager, dev_class_names, dev_ins_names, page_names, enc_mapping, btn_mapping=None, param_dict=None, targets_comp=None, page_button_led_values=('DefaultButton.Off', 'DefaultButton.On'), page_nav_led_values=('DefaultButton.Off', 'DefaultButton.On'), name='Dedicated_Device_Control', *a, **k):
        assert isinstance(page_names, tuple)
        self._page_names = page_names
        self._page_selector = PageSelector(self, (page_button_led_values[0],) + page_button_led_values, page_nav_led_values)
        super(DedicatedDevicesComponent, self).__init__(manager, dev_class_names, dev_ins_names, enc_mapping, btn_mapping=btn_mapping, param_dict=param_dict, targets_comp=targets_comp, name=name, *a, **k)
        self._num_pages = len(page_names)

    def disconnect(self):
        self._page_selector.disconnect()
        super(DedicatedDevicesComponent, self).disconnect()
        self._page_names = None
        self._page_selector = None
        return

    @property
    def page_index(self):
        return self._page_index

    @property
    def page_name(self):
        return self._page_names[self._page_index]

    @property
    def num_pages(self):
        return len(self._page_names)

    def on_enabled_changed(self):
        super(DedicatedDevicesComponent, self).on_enabled_changed()
        self._page_selector.set_enabled(self.is_enabled())

    def can_select_pages(self):
        return self.is_enabled() and any(self._current_devices)

    def set_page_buttons(self, buttons):
        """ Sets the button to use for directly selecting parameter pages. """
        self._page_selector.set_page_buttons(buttons)

    def set_prev_page_button(self, button):
        """ Sets the button to use for navigating to the previous parameter page. """
        self._page_selector.set_prev_page_button(button)

    def set_next_page_button(self, button):
        """ Sets the button to use for navigating to the next parameter page. """
        self._page_selector.set_next_page_button(button)

    def set_page_index(self, index):
        """ Sets the page index to use, updates all connections/LEDs and shows page
        info in the status bar. """
        if index in xrange(self.num_pages):
            super(DedicatedDevicesComponent, self).set_page_index(index)
            allow_paging = any(self._current_devices)
            self._page_selector.set_enabled(allow_paging)
            if allow_paging:
                self.component_message('Page %d' % (self._page_index + 1), self._page_names[self._page_index])
                self.notify_page_index()
                self.notify_page_name()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/UserDevicesComponent.pyc
