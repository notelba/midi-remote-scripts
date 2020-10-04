# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\GlobalEncoderComponent.py
# Compiled at: 2017-04-24 12:52:35
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from PropertyControl import PropertyControl, ParameterControl
from ShowMessageMixin import ShowMessageMixin
from Utils import live_object_is_valid, resolve_path_name_for_parameter
from ControlUtils import release_parameters
from consts import RECORD_QUANTIZE_NAMES, GLOBAL_QUANTIZE_NAMES, ZERO_DB_VALUE, PARAM_REL_STEP

class GlobalEncoderComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ GlobalEncoderComponent provides control over global properties via encoders. """

    def __init__(self, use_0_db_volume=False, name='Global_Encoder_Control', *a, **k):
        super(GlobalEncoderComponent, self).__init__(name=name, *a, **k)
        self._use_0_db_volume = bool(use_0_db_volume)
        groove_transform = lambda x: '%s%%' % int(round(x * 100))
        gq_transform = lambda x: GLOBAL_QUANTIZE_NAMES[x]
        rq_names = list(RECORD_QUANTIZE_NAMES)
        rq_names.insert(0, 'None')
        self._wrapper_dict = {'tempo': PropertyControl('tempo', self.song(), (20.0, 999.0), (60.0, 187.0), rel_thresh=2, display_name='Tempo', display_value_transform=lambda x: '%.2f' % x), 
           'groove_amount': PropertyControl('groove_amount', self.song(), (0.0, 1.3125), rel_thresh=0, rel_step=0.01, quantized=False, display_name='Groove', display_callback=self._display_groove_amount, display_value_transform=groove_transform), 
           'clip_trigger_quantization': PropertyControl('clip_trigger_quantization', self.song(), (0, 13), cast_value_to_int=True, value_items=GLOBAL_QUANTIZE_NAMES, display_name='G Qntz', display_value_transform=gq_transform), 
           'midi_recording_quantization': PropertyControl('midi_recording_quantization', self.song(), (0, 8), cast_value_to_int=True, value_items=rq_names, display_name='Rec Qntz', display_callback=self._display_record_quantization_value, display_value_transform=lambda x: rq_names[x]), 
           'master_volume': ParameterControl('volume', self.song().master_track.mixer_device.volume, (
                           0.0, ZERO_DB_VALUE), default_value=ZERO_DB_VALUE, rel_thresh=0, rel_step=PARAM_REL_STEP, quantized=False)}
        self._current_selected_parameter = None
        self._selected_parameter_is_locked = False
        self._selected_parameter_control = None
        self._selected_parameter_lock_button = None
        self._master_volume_control = None
        self._cue_volume_control = None
        self._crossfader_control = None
        self._on_selected_parameter_changed.subject = self.song().view
        return

    def disconnect(self):
        for w in self._wrapper_dict.values():
            w.disconnect()

        super(GlobalEncoderComponent, self).disconnect()
        self._current_selected_parameter = None
        self._selected_parameter_control = None
        self._selected_parameter_lock_button = None
        self._master_volume_control = None
        self._cue_volume_control = None
        self._crossfader_control = None
        return

    def set_selected_parameter_control(self, control):
        """ Sets the control to use for controlling the selected parameter. """
        release_parameters((self._selected_parameter_control,))
        self._selected_parameter_control = control
        self._on_selected_parameter_changed(False)

    def set_selected_parameter_lock_button(self, button):
        """ Sets the button to use for locking the selected parameter control to the
        current parameter. """
        self._selected_parameter_lock_button = button
        self._on_selected_parameter_lock_button_value.subject = button
        self._update_selected_parameter_lock_button()

    def set_master_volume_control(self, control):
        """ Sets the control to use for controlling master volume. """
        if self._use_0_db_volume:
            self._wrapper_dict['master_volume'].set_control(control)
        else:
            release_parameters((self._master_volume_control,))
            self._master_volume_control = control
            self._update_master_volume_connection()

    def set_cue_volume_control(self, control):
        """ Sets the control to use for controlling cue volume. """
        release_parameters((self._cue_volume_control,))
        self._cue_volume_control = control
        self._update_cue_volume_connection()

    def set_crossfader_control(self, control):
        """ Sets the control to use for controlling the crossfader. """
        release_parameters((self._crossfader_control,))
        self._crossfader_control = control
        self._display_crossfader_value.subject = None
        if control:
            self._display_crossfader_value.subject = self.song().master_track.mixer_device.crossfader
        self._update_crossfader_connection()
        return

    def __getattr__(self, name):
        """ Overrides standard to handle setters for PropertyControls. """
        if len(name) > 4 and name[:4] == 'set_':
            return partial(self._set_control, name[4:].replace('_control', ''))

    def _set_control(self, name, control):
        self._wrapper_dict[name].set_control(control)

    @subject_slot('value')
    def _on_selected_parameter_lock_button_value(self, value):
        if value and self._selected_parameter_control:
            if self._selected_parameter_is_locked:
                self._selected_parameter_is_locked = False
                self._on_selected_parameter_changed()
            elif live_object_is_valid(self._current_selected_parameter):
                self._selected_parameter_is_locked = True
                p_info = resolve_path_name_for_parameter(self.song(), self._current_selected_parameter)
                self.component_message('Selected Parameter Control locked to', p_info)
            else:
                self._on_selected_parameter_changed()
            self._update_selected_parameter_lock_button()

    def update(self):
        super(GlobalEncoderComponent, self).update()
        self._on_selected_parameter_changed(False)
        self._update_master_volume_connection()
        self._update_cue_volume_connection()
        self._update_crossfader_connection()
        self._update_selected_parameter_lock_button()
        if self.is_enabled():
            for w in self._wrapper_dict.values():
                w.update()

    def _update_master_volume_connection(self):
        if not self._use_0_db_volume:
            release_parameters((self._master_volume_control,))
            if self.is_enabled() and self._master_volume_control:
                control = self._master_volume_control
                control.connect_to(self.song().master_track.mixer_device.volume)

    def _update_cue_volume_connection(self):
        release_parameters((self._cue_volume_control,))
        if self._is_enabled and self._cue_volume_control:
            control = self._cue_volume_control
            control.connect_to(self.song().master_track.mixer_device.cue_volume)

    def _update_crossfader_connection(self):
        release_parameters((self._crossfader_control,))
        if self.is_enabled() and self._crossfader_control:
            control = self._crossfader_control
            control.connect_to(self.song().master_track.mixer_device.crossfader)

    def _update_selected_parameter_lock_button(self):
        if self.is_enabled() and self._selected_parameter_lock_button:
            if self._selected_parameter_is_locked:
                self._selected_parameter_lock_button.set_light('Global.LockOn')
            else:
                self._selected_parameter_lock_button.set_light('Global.LockOff')

    @subject_slot('selected_parameter')
    def _on_selected_parameter_changed(self, display=True):
        if self._selected_parameter_control:
            release_parameters((self._selected_parameter_control,))
            if self.is_enabled():
                is_locked = False
                if self._selected_parameter_is_locked:
                    if live_object_is_valid(self._current_selected_parameter):
                        is_locked = True
                    else:
                        self._selected_parameter_is_locked = False
                        self._update_selected_parameter_lock_button()
                param = self._current_selected_parameter if is_locked else self.song().view.selected_parameter
                if live_object_is_valid(param):
                    self._current_selected_parameter = param
                    self._selected_parameter_control.connect_to(param)
                    if display and not is_locked:
                        p_info = resolve_path_name_for_parameter(self.song(), param)
                        self.component_message('Selected Parameter Control assigned to', p_info)

    def _display_record_quantization_value(self, _):
        self.component_message('Record Quantize', str(self._wrapper_dict['midi_recording_quantization']))

    def _display_groove_amount(self, _):
        self.component_message('Groove Amount', str(self._wrapper_dict['groove_amount']))

    @subject_slot('value')
    def _display_crossfader_value(self):
        self.component_message('Crossfader', self.song().master_track.mixer_device.crossfader)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/GlobalEncoderComponent.pyc
