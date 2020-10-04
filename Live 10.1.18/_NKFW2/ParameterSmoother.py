# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ParameterSmoother.py
# Compiled at: 2017-03-07 13:28:52
import _Framework.Task
from ControlUtils import parameter_is_quantized, get_parameter_value_to_set

class ParameterSmoother(object):
    """ ParameterSmoother handles smoothly changing a parameter's value via a
    task.

    Users of this object must call its disconnect method on disconnect."""

    def __init__(self, tasks, default_smoothing_speed=2, smoothing_complete_callback=None):
        self._parameter = None
        self._smoothing_speed = default_smoothing_speed
        self._smoothing_range = []
        self._smooth_task = _Framework.Task.loop(_Framework.Task.delay(1), self._handle_smoothing)
        self._smooth_task.pause()
        tasks.add(self._smooth_task)
        self._smoothing_complete_callback = smoothing_complete_callback
        return

    def disconnect(self):
        self._smoothing_range = None
        self._smooth_task = None
        return

    def set_parameter(self, param):
        """ Sets the parameter to control. """
        self.stop_smoothing()
        self._parameter = param

    def set_smoothing_speed(self, speed):
        """ Sets the smoothing speed to use.  1 is the slowest possible setting and is
        equivalent to no smoothing. """
        assert isinstance(speed, int)
        assert speed >= 1
        self._smoothing_speed = speed

    def set_parameter_value(self, value, no_smoothing=False):
        """ Initializes smoothing or just directly sets the parameter value if
        no_smoothing or the parameter is quantized. """
        assert value is None or isinstance(value, float)
        if self._parameter is not None and value is not None:
            value = get_parameter_value_to_set(self._parameter, value)
            if parameter_is_quantized(self._parameter) or no_smoothing:
                self._parameter.value = value
            else:
                self._smoothing_range = []
                difference = value - self._parameter.value
                if self._smoothing_speed > 1 and abs(difference) > 0.1:
                    self._smoothing_range = [abs(difference) / self._smoothing_speed, value]
                    if difference < 0.0:
                        self._smoothing_range[0] *= -1
                    self._parameter.begin_gesture()
                    self._smooth_task.restart()
                else:
                    self._parameter.value = value
        return

    def stop_smoothing(self):
        """ Stop the smoothing task and clears the range. """
        if self._smooth_task:
            self._smooth_task.pause()
        self._smoothing_range = []

    def _handle_smoothing(self, _=None):
        """ Handles smoothly changing the parameter's value by making small changes that
        are each triggered by a task. """
        if self._parameter is not None and self._smoothing_range:
            param = self._parameter
            target = self._smoothing_range[1]
            factor = self._smoothing_range[0]
            new_value = param.value + factor
            if factor > 0.0 and new_value < target and new_value < param.max or factor < 0.0 and new_value > target and new_value > param.min:
                param.value = get_parameter_value_to_set(param, new_value)
            else:
                if self._smoothing_complete_callback:
                    self._smoothing_complete_callback()
                param.value = target
                param.end_gesture()
                self._smoothing_range = []
                self._smooth_task.pause()
        else:
            self._smooth_task.pause()
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ParameterSmoother.pyc
