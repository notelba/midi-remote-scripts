# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\MatrixXYComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from SpecialControl import MatrixXYControl
from TrackDeviceManager import MAX_NESTED_DEPTH, get_track_based_path, get_track_based_path_name
from ShowMessageMixin import ShowMessageMixin, DisplayType
from ControlUtils import format_control_name
from Utils import resolve_path_for_parameter, resolve_parameter_for_path, resolve_name_for_path
LEARN_START_MSG = 'Select the parameter for %s to control.  Press %s to exit learning.'
ASSIGN_MSG = 'Press %s to assign %s to %s'

class MatrixXYBaseComponent(CompoundComponent, ShowMessageMixin):
    """ MatrixXYBaseComponent ia the base class for a component that assigns a
    MatrixXYControl to parameters.  This module includes two ready to use classes:
    MatrixXYSetComponent and MatrixXYTrackComponent. """

    def __init__(self, default_smoothing_speed=2, is_velocity_sensitive=False, x_color='XY.X', y_color='XY.Y', point_color='XY.Point', *a, **k):
        super(MatrixXYBaseComponent, self).__init__(*a, **k)
        self._mapping_predicate = lambda x: True
        self._path_resolver = lambda x: x
        self._path_name_resolver = lambda x: x
        self._on_assignments_changed_method = lambda : None
        self._x_y_control = self.register_component(MatrixXYControl(default_smoothing_speed, is_velocity_sensitive, x_color, y_color, point_color))
        self._x_learn_button = None
        self._y_learn_button = None
        self._is_learning = False
        self._x_is_learning = False
        self._y_is_learning = False
        self._x_learn_button_name = ''
        self._y_learn_button_name = ''
        self._current_parameter = None
        self._current_path = None
        self._current_path_name = None
        self._on_selected_parameter_changed.subject = self.song().view
        return

    def disconnect(self):
        super(MatrixXYBaseComponent, self).disconnect()
        self._mapping_predicate = None
        self._path_resolver = None
        self._path_name_resolver = None
        self._on_assignments_changed_method = None
        self._x_learn_button = None
        self._y_learn_button = None
        self._x_learn_button_name = None
        self._y_learn_button_name = None
        self._current_parameter = None
        self._current_path = None
        self._current_path_name = None
        return

    def set_matrix(self, matrix):
        """ Sets the matrix for MatrixXYControl. """
        self._x_y_control.set_matrix(matrix)

    def set_x_learn_button(self, button):
        """ Sets the button to toggle learn state for the X parameter. """
        self._reset_learning_state()
        self._x_learn_button = button
        self._on_x_learn_button_value.subject = button
        self._x_learn_button_name = format_control_name(button)
        self._update_learn_buttons()

    def set_y_learn_button(self, button):
        """ Sets the button to toggle learn state for the Y parameter. """
        self._reset_learning_state()
        self._y_learn_button = button
        self._on_y_learn_button_value.subject = button
        self._y_learn_button_name = format_control_name(button)
        self._update_learn_buttons()

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

    def set_on_assignments_changed_method(self, method):
        """ Sets the method to call upon assignments being changed. """
        self._on_assignments_changed_method = method

    @subject_slot('value')
    def _on_x_learn_button_value(self, value):
        self._set_learning_state(value)

    @subject_slot('value')
    def _on_y_learn_button_value(self, value):
        self._set_learning_state(value, True)

    def _set_learning_state(self, value, is_y_learn=False):
        if self.is_enabled() and value:
            if is_y_learn:
                self._x_is_learning = False
                self._y_is_learning = not self._y_is_learning
                self._is_learning = self._y_is_learning
            else:
                self._y_is_learning = False
                self._x_is_learning = not self._x_is_learning
                self._is_learning = self._x_is_learning
            if self._is_learning:
                self._start_learning(is_y_learn)
            else:
                self._stop_learning(is_y_learn)

    def _start_learning(self, is_y):
        self._clear_current()
        if is_y:
            detail = (
             'Y', self._y_learn_button_name)
        else:
            detail = (
             'X', self._x_learn_button_name)
        self.component_message(LEARN_START_MSG % detail, display_type=DisplayType.STATUS)
        self.component_message('Select the parameter for %s to control.' % ('Y' if is_y else 'X'), display_type=DisplayType.PHYSICAL, revert=False)
        self._update_learn_buttons()

    def _stop_learning(self, is_y):
        if self._current_parameter and self._current_path_name:
            if is_y:
                self._x_y_control.set_y_parameter(self._current_parameter)
            else:
                self._x_y_control.set_x_parameter(self._current_parameter)
            axis = 'Y' if is_y else 'X'
            self.component_message('%s assigned to %s' % (axis, self._current_path_name), display_type=DisplayType.STATUS)
            self.component_message('%s assigned to %s' % (axis,
             self._current_parameter.name), display_type=DisplayType.PHYSICAL)
        self._update_learn_buttons()
        self._on_assignments_changed_method(is_y)
        self._clear_current()

    def _reset_learning_state(self):
        self._x_y_control.reset()
        self._clear_current()
        self._x_is_learning = False
        self._y_is_learning = False
        self._is_learning = False
        self._update_learn_buttons()

    @subject_slot('selected_parameter')
    def _on_selected_parameter_changed(self):
        self._clear_current()
        if self.is_enabled() and self._is_learning:
            param, path = self._get_parameter_to_assign(self._y_is_learning)
            if param and path:
                self._current_path = self._path_resolver(path)
                self._current_parameter = param
                rnfp = resolve_name_for_path(self.song(), path, param)
                self._current_path_name = self._path_name_resolver(rnfp)
                if self._y_is_learning:
                    detail = (
                     self._y_learn_button_name, 'Y')
                else:
                    detail = (
                     self._x_learn_button_name, 'X')
                status_detail = detail + (self._current_path_name,)
                physical_detail = detail + (self._current_parameter.name,)
                self.component_message(ASSIGN_MSG % status_detail, display_type=DisplayType.STATUS)
                self.component_message(ASSIGN_MSG % physical_detail, display_type=DisplayType.PHYSICAL, revert=False)

    def _get_parameter_to_assign(self, is_y):
        param = self.song().view.selected_parameter
        if param:
            if param.name == 'Global Groove Amount':
                return (None, None)
            if self._can_assign_parameter(param, is_y):
                path = resolve_path_for_parameter(param, by_name=False)
                if self._mapping_predicate(path):
                    return (param, path)
        return (None, None)

    def _can_assign_parameter(self, parameter, is_y):
        """ Returns whether the parameter can be assigned. This is needed to prevent both
        axes from being assigned to the same parameter. """
        if is_y:
            return parameter != self._x_y_control.x_parameter
        return parameter != self._x_y_control.y_parameter

    def _clear_current(self):
        self._current_parameter = None
        self._current_path = None
        self._current_path_name = None
        return

    def update(self):
        super(MatrixXYBaseComponent, self).update()
        self._update_learn_buttons()

    def _update_learn_buttons(self):
        if self.is_enabled():
            if self._x_learn_button:
                self._x_learn_button.set_light('XY.X_LearnOn' if self._x_is_learning else 'XY.X_LearnOff')
            if self._y_learn_button:
                self._y_learn_button.set_light('XY.Y_LearnOn' if self._y_is_learning else 'XY.Y_LearnOff')


class MatrixXYSetComponent(MatrixXYBaseComponent):
    """ MatrixXYSetComponent assigns a MatrixXYControl to arbitrary parameters within a
    set. """
    __subject_events__ = ('parameters', )

    def __init__(self, *a, **k):
        name = k.pop('name', 'Matrix_X_Y_Set_Control')
        super(MatrixXYSetComponent, self).__init__(*a, **k)
        self.name = name
        self.set_on_assignments_changed_method(self._on_assignments_changed)
        self._rebuild_data = None
        return

    def disconnect(self):
        super(MatrixXYSetComponent, self).disconnect()
        self._rebuild_data = None
        return

    def rebuild(self, data):
        """ Rebuilds parameter assignments based on the given data tuple. """
        if self.is_enabled():
            x = resolve_parameter_for_path(self.song(), data[0])
            y = resolve_parameter_for_path(self.song(), data[1])
            self._x_y_control.set_parameters(x, y)
            self._rebuild_data = None
        else:
            self._rebuild_data = data
        return

    def _on_assignments_changed(self, _):
        x = resolve_path_for_parameter(self._x_y_control.x_parameter)
        y = resolve_path_for_parameter(self._x_y_control.y_parameter)
        self.notify_parameters((x, y))

    def update(self):
        super(MatrixXYSetComponent, self).update()
        if self.is_enabled() and self._rebuild_data:
            self.rebuild(self._rebuild_data)


class MatrixXYTrackComponent(MatrixXYBaseComponent):
    """ MatrixXYTrackComponent assigns a MatrixXYControl to track-based parameters. """
    __subject_events__ = ('assignments', )

    def __init__(self, manager, targets_comp, *a, **k):
        name = k.pop('name', 'Matrix_X_Y_Track_Control')
        super(MatrixXYTrackComponent, self).__init__(*a, **k)
        self.name = name
        self._manager = manager
        self._track = None
        self._assignments = [None, None]
        self.set_mapping_predicate(self._track_based_predicate)
        self.set_path_resolver(get_track_based_path)
        self.set_path_name_resolver(get_track_based_path_name)
        self.set_on_assignments_changed_method(self._on_assignments_changed)
        self._update_control_connections.subject = manager
        self._on_track_changed.subject = targets_comp
        self._on_track_changed(targets_comp.target_track)
        return

    def disconnect(self):
        super(MatrixXYTrackComponent, self).disconnect()
        self._manager.disconnect()
        self._track = None
        self._assignments = None
        return

    def _set_assignments(self, assignments):
        """ Sets all the assignments to use. """
        self._assignments = assignments
        self._update_control_connections()

    def _get_assignments(self):
        """ Returns a list of the assignments to use. """
        return self._assignments

    assignments = property(_get_assignments, _set_assignments)

    def update(self):
        super(MatrixXYTrackComponent, self).update()
        self._update_control_connections()

    @subject_slot('devices')
    def _update_control_connections(self, track_changed=False):
        if self._is_learning:
            return
        if self.is_enabled():
            x = self._manager.get_assigned_track_parameter(self._assignments[0])
            y = self._manager.get_assigned_track_parameter(self._assignments[1])
            self._x_y_control.set_x_parameter(x)
            self._x_y_control.set_y_parameter(y)

    @subject_slot('target_track')
    def _on_track_changed(self, track):
        self._reset_learning_state()
        self._track = track

    def _track_based_predicate(self, path):
        return len(path) <= MAX_NESTED_DEPTH and path[0][1] == self._track

    def _on_assignments_changed(self, is_y):
        self._assignments[int(is_y)] = self._current_path
        self.notify_assignments()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/MatrixXYComponent.pyc
