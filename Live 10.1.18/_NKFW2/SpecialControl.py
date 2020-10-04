# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialControl.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.Control import ButtonControl, ControlManager
from _Framework.SubjectSlot import Subject, subject_slot, subject_slot_group
from _Framework.Dependency import depends
from _Framework.Util import lazy_attribute
from _Framework import Task
from ParameterSmoother import ParameterSmoother
from Utils import live_object_is_valid
from ControlUtils import set_group_button_lights, get_smoothing_speed_for_velocity

class SpecialButtonControl(ButtonControl):
    """ Extends ButtonControl to allow for an on_color and is_on property so can
    be used to properly provide feedback for parameter control. """

    class State(ButtonControl.State):

        def __init__(self, control=None, manager=None, color=None, on_color=None, pressed_color=None, disabled_color=None, enabled=True, *a, **k):
            self._on_color = on_color
            self._is_on = False
            super(SpecialButtonControl.State, self).__init__(control, manager, color, pressed_color, disabled_color, enabled=enabled, *a, **k)

        def _get_is_on(self):
            return self._is_on

        def _set_is_on(self, value):
            self._is_on = bool(value)
            self._send_current_color()

        is_on = property(_get_is_on, _set_is_on)

        def _get_on_color(self):
            return self._on_color

        def _set_on_color(self, value):
            self._on_color = value
            self._send_current_color()

        on_color = property(_get_on_color, _set_on_color)

        def _send_current_color(self):
            """ Overrides standard to use on_color and not deal with pressed_color at
            all. """
            if self._control_element:
                if not self._enabled:
                    self._control_element.set_light(self._disabled_color)
                elif self.is_on:
                    self._control_element.set_light(self._on_color)
                else:
                    self._control_element.set_light(self._color)


class RadioButtonGroup(ControlManager, Subject):
    """ RadioButtonGroup utilizes a fixed number of buttons to select items of some sort.
    Only one index/item can be selected at a time and no notifications are triggered if
    the index/item is already selected.  This module includes an alternate form
    (ReselectableRadioButtonGroup) that always triggers notifications.

    This is essentially equivalent to the RadioButtonGroup in _Framework, but isn't
    resizeable and works properly in unit tests. """
    __subject_events__ = ('checked_index', )

    def __init__(self, num_buttons=2, default_index=0, enabled=True, checked_color='DefaultButton.On', unchecked_color='DefaultButton.Off', disabled_color='DefaultButton.Disabled', *a, **k):
        super(RadioButtonGroup, self).__init__(*a, **k)
        assert num_buttons > 1
        assert default_index < num_buttons
        self._num_buttons = num_buttons
        self._current_index = default_index
        self._checked_color = checked_color
        self._unchecked_color = unchecked_color
        self._disabled_color = disabled_color
        self._is_enabled = bool(enabled)
        self._buttons = None
        return

    @property
    def checked_index(self):
        """ Returns the current checked index. """
        return self._current_index

    def set_buttons(self, buttons):
        """ Sets the buttons to use. """
        assert buttons is None or len(buttons) == self._num_buttons
        self._buttons = list(buttons) if buttons else None
        self._on_button_value.replace_subjects(buttons or [])
        self.update()
        return

    def set_enabled(self, enable):
        """ Sets the enabled state of the group. """
        self._is_enabled = bool(enable)
        self.update()

    def set_checked_index(self, index):
        """ Sets the checked index.  This does NOT notify listeners. """
        if index != self._current_index:
            self._current_index = index
            if self._is_enabled:
                self.update()

    @subject_slot_group('value')
    def _on_button_value(self, value, button):
        """ Sets the checked index and notifies listeners. """
        if self._is_enabled and value:
            index = self._buttons.index(button)
            if index != self._current_index:
                self._current_index = index
                self.notify_checked_index(index)
                self.update()

    def update(self):
        """ Update LEDs to reflect current state/selection. """
        if self._buttons:
            if self._is_enabled:
                for index, button in enumerate(self._buttons):
                    if button:
                        if index == self._current_index:
                            button.set_light(self._checked_color)
                        else:
                            button.set_light(self._unchecked_color)

            else:
                for button in self._buttons:
                    if button:
                        button.set_light(self._disabled_color)


class ReselectableRadioButtonGroup(RadioButtonGroup):
    """ ReselectableRadioButtonGroup is the same as RadioButtonGroup, but always triggers
    notifications. """

    @subject_slot_group('value')
    def _on_button_value(self, value, button):
        """ Sets/resets the checked index and notifies listeners. """
        if self._is_enabled and value:
            index = self._buttons.index(button)
            self._current_index = index
            self.notify_checked_index(index)
            self.update()


class MatrixXYControl(ControlManager, Subject):
    """ MatrixXYControl sets up a matrix to function as an X/Y pad with smoothing that
    can be assigned to control two parameters. """
    _has_task_group = False

    def __init__(self, default_smoothing_speed=2, is_velocity_sensitive=False, x_color='XY.X', y_color='XY.Y', point_color='XY.Point', *a, **k):
        super(MatrixXYControl, self).__init__(*a, **k)
        self._is_velocity_sensitive = bool(is_velocity_sensitive)
        self._is_enabled = True
        self._x_color = x_color
        self._y_color = y_color
        self._point_color = point_color
        self._matrix = None
        self._width = -1
        self._height = -1
        self._last_x_value = None
        self._last_y_value = None
        self._x_parameter = None
        self._y_parameter = None
        self._x_smoother = ParameterSmoother(self._tasks, default_smoothing_speed)
        self._y_smoother = ParameterSmoother(self._tasks, default_smoothing_speed)
        return

    def disconnect(self):
        super(MatrixXYControl, self).disconnect()
        if self._has_task_group:
            self._tasks.kill()
            self._tasks.clear()
        self._x_smoother.disconnect()
        self._y_smoother.disconnect()
        self._matrix = None
        self._x_parameter = None
        self._y_parameter = None
        return

    def set_matrix(self, matrix):
        """ Sets the matrix to use. """
        self.reset()
        self._width = -1
        self._height = -1
        self._last_x_value = None
        self._last_y_value = None
        self._matrix = matrix
        if matrix:
            self._width = self._matrix.width()
            self._height = self._matrix.height()
        self._on_matrix_value.subject = self._matrix
        self.update()
        return

    @property
    def x_parameter(self):
        """ The parameter assigned to X. """
        return self._x_parameter

    @property
    def y_parameter(self):
        """ The parameter assigned to Y. """
        return self._y_parameter

    def set_parameters(self, x_param, y_param):
        """ Sets the parameters for X and Y to control. """
        self.set_x_parameter(x_param)
        self.set_y_parameter(y_param)

    def set_x_parameter(self, param):
        """ Sets the parameter for X to control. """
        self._last_x_value = None
        self._x_parameter = param
        self._on_x_parameter_value.subject = param
        self._x_smoother.set_parameter(param)
        self._update_matrix(True)
        return

    def set_y_parameter(self, param):
        """ Sets the parameter for Y to control. """
        self._last_y_value = None
        self._y_parameter = param
        self._on_y_parameter_value.subject = param
        self._y_smoother.set_parameter(param)
        self._update_matrix(update_y=True)
        return

    def _set_enabled_recursive(self, enable):
        """ Sets the control's enabled state for use with CompoundComponents. """
        self.set_enabled(enable)

    def set_enabled(self, enable):
        """ Sets the enabled state of the control. """
        self._is_enabled = bool(enable)
        if self._is_enabled:
            self.update()
        else:
            self.reset()

    def reset(self):
        """ Resets the properties of this control. """
        self._last_x_value = None
        self._last_y_value = None
        self._x_smoother.stop_smoothing()
        self._y_smoother.stop_smoothing()
        return

    @subject_slot('value')
    def _on_matrix_value(self, value, x, y, _):
        if self._is_enabled and value:
            if self._is_velocity_sensitive:
                s = get_smoothing_speed_for_velocity(value)
                self._x_smoother.set_smoothing_speed(s)
                self._y_smoother.set_smoothing_speed(s)
            y = self._height - 1 - y
            if live_object_is_valid(self._x_parameter):
                target = self._get_target_value(self._x_parameter, self._width, x)
                self._x_smoother.set_parameter_value(target)
            else:
                self._update_matrix(update_x=True)
            if live_object_is_valid(self._y_parameter):
                target = self._get_target_value(self._y_parameter, self._height, y)
                self._y_smoother.set_parameter_value(target)
            else:
                self._update_matrix(update_y=True)

    @staticmethod
    def _get_target_value(param, num_buttons, button_id):
        param_range = float(param.max - param.min)
        return param_range / (num_buttons - 1) * button_id + param.min

    @staticmethod
    def _get_scaled_parameter_value(param, num_buttons):
        return min(num_buttons - 1, int((param.value - param.min) / (param.max - param.min) * num_buttons))

    @subject_slot('value')
    def _on_x_parameter_value(self):
        self._update_matrix(True)

    @subject_slot('value')
    def _on_y_parameter_value(self):
        self._update_matrix(update_y=True)

    def update(self):
        super(MatrixXYControl, self).update()
        self._update_matrix(True, True)

    def _update_matrix(self, update_x=False, update_y=False):
        if self._is_enabled and self._matrix:
            if live_object_is_valid(self._x_parameter) or live_object_is_valid(self._y_parameter):
                should_update = False
                x_value = self._last_x_value
                y_value = self._last_y_value
                if live_object_is_valid(self._x_parameter) and update_x:
                    x_value = self._get_scaled_parameter_value(self._x_parameter, self._width)
                    if x_value != self._last_x_value:
                        self._last_x_value = x_value
                        should_update = True
                if live_object_is_valid(self._y_parameter) and update_y:
                    y_value = self._height - 1 - self._get_scaled_parameter_value(self._y_parameter, self._height)
                    if y_value != self._last_y_value:
                        self._last_y_value = y_value
                        should_update = True
                if should_update:
                    self._handle_matrix_update(x_value, y_value)
            else:
                set_group_button_lights(self._matrix, 'DefaultButton.Off')

    def _handle_matrix_update(self, x_value, y_value):
        row_to_light = 0
        col_to_light = 0
        if x_value is not None:
            col_to_light = x_value
        if y_value is not None:
            row_to_light = y_value
        for btn, (col, row) in self._matrix.iterbuttons():
            if btn:
                if row == row_to_light and col != col_to_light:
                    btn.set_light('XY.X')
                elif col == col_to_light:
                    btn.set_light('XY.Y')
                else:
                    btn.set_light('DefaultButton.Off')

        self._matrix.get_button(col_to_light, row_to_light).set_light('XY.Point')
        return

    @lazy_attribute
    @depends(parent_task_group=None)
    def _tasks(self, parent_task_group=None):
        self._has_task_group = True
        return parent_task_group.add(Task.TaskGroup())
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialControl.pyc
