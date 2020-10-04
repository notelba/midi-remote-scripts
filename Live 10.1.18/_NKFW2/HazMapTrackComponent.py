# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\HazMapTrackComponent.py
# Compiled at: 2017-05-19 14:00:42
import Live
ABS_MODES = (
 Live.MidiMap.MapMode.absolute,
 Live.MidiMap.MapMode.absolute_14_bit)
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from HazMapBaseComponent import HazMapBaseComponent
from TrackDeviceManager import MAX_NESTED_DEPTH, get_track_based_path, get_track_based_path_name
from ShowMessageMixin import ShowMessageMixin, DisplayType
from ControlUtils import release_parameters, is_button_pressed, format_control_name
from Utils import resolve_path_for_parameter, resolve_name_for_path
from SpecialButtonSliderElement import SpecialButtonSliderElement

class HazMapTrackComponent(HazMapBaseComponent, ShowMessageMixin):
    """ HazMapTrackComponent extends HazMapBaseComponent and is the standard HazMap class
    that includes all of the functionality needed for assigning track-based parameters
    to control. This works in conjunction with a TrackDeviceManager and can be extended
    to allow for sub-sets of track-based parameter assignments. This module also includes
    a variant (HazMapPagedTrackComponent) that allows for paged assignments. """

    def __init__(self, manager, targets_comp=None, num_controls_or_pages=8, handle_shift_led=False, name='HazMap_Track_Control', *a, **k):
        super(HazMapTrackComponent, self).__init__(manager, num_controls_or_pages=num_controls_or_pages, name=name, *a, **k)
        self._display_header = 'Page'
        self._mapping_predicate = lambda x: True
        self._path_resolver = get_track_based_path
        self._path_name_resolver = get_track_based_path_name
        self._on_delete_assignments_method = lambda : None
        self._handle_shift_led = bool(handle_shift_led)
        self._is_button_slider = False
        self._is_mapping = False
        self._is_deleting = False
        self._can_map = True
        self._track = None
        self._current_parameter = None
        self._current_path = None
        self._current_path_name = None
        self._shift_button = None
        self._controls_name = ''
        self._controls_are_absolute = True
        if targets_comp:
            self._on_track_changed.subject = targets_comp
            self._on_track_changed(targets_comp.target_track)
        self._on_selected_parameter_changed.subject = self.song().view
        return

    def disconnect(self):
        super(HazMapTrackComponent, self).disconnect()
        self._mapping_predicate = None
        self._path_resolver = None
        self._on_delete_assignments_method = None
        self._track = None
        self._current_parameter = None
        self._current_path = None
        self._current_path_name = None
        self._shift_button = None
        return

    def set_shift_button(self, button):
        """ Sets the button to use to deactivate all assignments and allow for mapping
        activation/de-activation and assignment deletion. """
        self._shift_button = button
        self._on_shift_button_value.subject = button
        if button and self._handle_shift_led:
            button.set_light('HazMap.Modifier')

    def set_control(self, control):
        """ Overrides standard to set the control to use for controlling assigned
        parameters, for activating/de-activating and for deleting assignments.  This
        is only meant for use in components such as the HazMapMixerComponent. """
        self.set_controls((control,) if control else None)
        return

    def set_controls(self, controls):
        """ Sets the group of controls to use for controlling assigned parameters.  This
        will also store the name of the group of controls for displaying purposes and
        determine the type of controls (absolute or relative) being used. """
        self._set_is_mapping(False, display=False)
        self._can_map = True
        release_parameters(self._controls)
        self._on_control_value.replace_subjects([])
        self._controls = list(controls) if controls else []
        if self._controls:
            first = self._controls[0]
            if len(self._controls) == 1:
                self._controls_name = format_control_name(first)
            else:
                self._controls_name = controls.name.replace('_', ' ')
            self._controls_are_absolute = first.message_map_mode() in ABS_MODES
            self._is_button_slider = isinstance(first, SpecialButtonSliderElement)
        self._update_control_connections()

    def set_mapping_predicate(self, predicate):
        """ Sets the predicate function to use for discerning if an assignment is
        allowable. """
        self._mapping_predicate = predicate

    def set_path_resolver(self, resolver):
        """ Sets the function to use for resolving paths to parameters for use with the
        TrackDeviceManager. """
        self._path_resolver = resolver

    def set_path_name_resolver(self, resolver):
        """ Sets the function to use for resolving friendly path names to parameters. """
        self._path_name_resolver = resolver

    def set_on_delete_assignments_method(self, method):
        """ Sets the method to call upon assignments being deleted. """
        self._on_delete_assignments_method = method

    def set_page_index(self, index):
        """ Extends standard to update button sliders. """
        super(HazMapTrackComponent, self).set_page_index(index)
        self._update_button_sliders()

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        self._can_map = True
        self._clear_current()
        if self.is_enabled() and self._controls:
            if not self._is_mapping:
                if value:
                    c_name = format_control_name(self._controls[0])
                    self.component_message(c_name, 'Inc toggles mapping, Dec deletes all', revert=False)
                    release_parameters(self._controls)
                    self._on_control_value.replace_subjects(self._controls)
                else:
                    self.component_message('', display_type=DisplayType.PHYSICAL)
                    self._on_control_value.replace_subjects([])
                    self._update_control_connections()
            self._update_shift_button()
            self._update_button_sliders()

    @subject_slot_group('value')
    def _on_control_value(self, value, control):
        ctrl_index = self._controls.index(control)
        if not self._controls_are_absolute:
            value = control.get_adjustment_factor(value, threshold=40)
        if self._is_assignment_delete_gesture(ctrl_index, value):
            self._handle_assignment_deletion()
            self._can_map = False
        elif self._can_map and self._is_assignment_toggle_gesture(ctrl_index, value):
            self._set_is_mapping(not self._is_mapping)
            self._can_map = False
        elif self._is_mapping and self._current_path:
            p_id = ctrl_index + self._page_index
            self._assignments[p_id] = self._current_path
            self._page_names[p_id] = self._current_path_name
            c_name = format_control_name(control)
            self.component_message('%s mapped to' % c_name, self._current_path_name, display_type=DisplayType.STATUS)
            p = self.song().view.selected_parameter
            if p is not None:
                self.component_message('%s mapped to %s' % (c_name, p.name), display_type=DisplayType.PHYSICAL)
        self._update_button_sliders()
        return

    def _is_assignment_toggle_gesture(self, ctrl_index, value):
        def_criteria = ctrl_index == 0 and is_button_pressed(self._shift_button)
        if def_criteria:
            if self._controls_are_absolute:
                return value == 127
            return value == 1
        return False

    def _is_assignment_delete_gesture(self, ctrl_index, value):
        def_criteria = ctrl_index == 0 and is_button_pressed(self._shift_button)
        if def_criteria:
            if self._controls_are_absolute:
                if self._is_deleting:
                    return value == 127
                return value == 0
            if self._is_deleting:
                return value == 1
            return value == -1
        return False

    def _set_is_mapping(self, is_mapping, display=True):
        self._clear_current()
        if self.is_enabled() and self._controls and self._is_mapping != is_mapping:
            self._is_mapping = is_mapping
            if not is_mapping:
                self._update_control_connections()
                self.notify_assignments()
                self.notify_page_names()
            if display:
                state = 'On' if self._is_mapping else 'Off'
                self.component_message('%s Mapping Mode' % self.name, state, display_type=DisplayType.STATUS)
                self.component_message('Mapping Mode', state, display_type=DisplayType.PHYSICAL)
            self._update_shift_button()

    def _handle_assignment_deletion(self):
        if self._is_deleting:
            self._assignments = [ None for _ in self._assignments ]
            self._page_names = [ None for _ in self._page_names ]
            self._set_is_mapping(False, display=False)
            self.notify_assignments()
            self.notify_page_names()
            self._on_delete_assignments_method()
            self.component_message('%s mappings were successfully deleted.' % self.name, display_type=DisplayType.STATUS)
            self.component_message('Mappings were successfully deleted.', display_type=DisplayType.PHYSICAL)
        else:
            self._is_deleting = True
            self.component_message('Are you sure that you want to delete all ' + '%s mappings?' % self.name, display_type=DisplayType.STATUS)
            self.component_message('Are you sure that you want to delete all mappings?', display_type=DisplayType.PHYSICAL, revert=False)
        return

    @subject_slot('target_track')
    def _on_track_changed(self, track):
        self._set_is_mapping(False)
        self._track = track

    @subject_slot('selected_parameter')
    def _on_selected_parameter_changed(self):
        self._clear_current()
        if self.is_enabled() and self._is_mapping:
            param, path = self._get_parameter_to_assign()
            if param and path:
                self._current_path = self._path_resolver(path)
                if self._current_path in self._assignments:
                    self._clear_current()
                else:
                    self._current_parameter = param
                    rnfp = resolve_name_for_path(self.song(), path, param)
                    self._current_path_name = self._path_name_resolver(rnfp)
                    msg = 'Move one of the %s to map it to'
                    if len(self._controls) == 1:
                        msg = 'Move %s to map it to'
                    self.component_message(msg % self._controls_name, self._current_path_name, display_type=DisplayType.STATUS)
                    self.component_message(msg % self._controls_name + ' ' + param.name, display_type=DisplayType.PHYSICAL, revert=False)

    def _get_parameter_to_assign(self):
        param = self.song().view.selected_parameter
        if param:
            if param.name == 'Global Groove Amount':
                return (None, None)
            path = resolve_path_for_parameter(param, by_name=False)
            if len(path) <= MAX_NESTED_DEPTH and path[0][1] == self._track and self._mapping_predicate(path):
                return (param, path)
        return (None, None)

    def _clear_current(self):
        self._current_parameter = None
        self._current_path = None
        self._current_path_name = None
        self._is_deleting = False
        return

    def update(self):
        super(HazMapTrackComponent, self).update()
        self._update_shift_button()

    @subject_slot('devices')
    def _update_control_connections(self, track_changed=False):
        """ Extends standard to not update if mapping. """
        if self._is_mapping:
            return
        super(HazMapTrackComponent, self)._update_control_connections(False)

    def _update_shift_button(self):
        if self.is_enabled() and self._shift_button and self._handle_shift_led:
            value = 'HazMap.Modifier'
            if is_button_pressed(self._shift_button):
                value = 'HazMap.ModifierPressed'
            elif self._is_mapping:
                value = 'HazMap.ModifierMapping'
            self._shift_button.set_light(value)

    def _update_button_sliders(self):
        if self.is_enabled() and self._controls and self._is_button_slider:
            height = self._controls[0].height() - 1
            delete_btn = self._controls[0].get_button(0)
            assign_btn = self._controls[0].get_button(height)
            shift_pressed = is_button_pressed(self._shift_button)
            if shift_pressed:
                delete_btn.set_light('DefaultButton.Off' if self._is_deleting else 'HazMap.DeleteButton')
                assign_value = 'HazMap.IsMapping' if self._is_mapping else 'HazMap.MapButton'
                assign_btn.set_light('HazMap.IsDeleting' if self._is_deleting else assign_value)
            elif self._is_mapping:
                delete_btn.set_light('DefaultButton.Off')
                for i, c in enumerate(self._controls):
                    btn = c.get_button(height)
                    if btn:
                        a = self._assignments[(i + self._page_index)]
                        btn.set_light('HazMap.HasAssign' if a else 'HazMap.NoAssign')


class HazMapPagedTrackComponent(HazMapTrackComponent):
    """ HazMapTrackComponent capable of multiple pages of assignments.  This is only
    meant for use with static assignments, so dev_dict needs to be set.  Also, this
    is not currently compatible with button sliders. """

    def _set_display_header(self, header):
        """ Sets the header that will be used when displaying page info in the status
        bar. """
        self._display_header = header

    def _get_display_header(self):
        """ Returns the header to use when displaying page info. """
        return self._display_header

    display_header = property(_get_display_header, _set_display_header)

    def _get_parameter(self, i):
        return self._manager.get_multi_device_track_parameter(self._dev_dict, i, self._page_index)

    @subject_slot('page_index')
    def _on_page_changed(self):
        super(HazMapPagedTrackComponent, self)._on_page_changed()
        self.component_message(self._display_header, self.page_names[self._page_index])
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/HazMapTrackComponent.pyc
