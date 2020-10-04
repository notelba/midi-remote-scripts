# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\touch_strip.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import math
from functools import partial
from itertools import chain, repeat
from ableton.v2.base import depends, listens
from ableton.v2.control_surface.elements import TouchEncoderElement

class TouchStripElement(TouchEncoderElement):

    def __init__(self, leds=None, *a, **k):
        assert leds is not None
        self.map_value_to_led_states = partial(map_value_to_led_states, 127, 0, len(leds))
        assert self.map_value_to_led_states(0)
        super(TouchStripElement, self).__init__(*a, **k)
        self._leds = leds
        return

    def connect_to(self, parameter):
        super(TouchStripElement, self).connect_to(parameter)
        self._update_feedback_leds(force=True)
        self.__on_parameter_value.subject = self.mapped_parameter()

    def release_parameter(self):
        super(TouchStripElement, self).release_parameter()
        self.__on_parameter_value.subject = None
        return

    @listens(b'value')
    def __on_parameter_value(self):
        self._update_feedback_leds()

    def _update_feedback_leds(self, force=False):
        for led, state in zip(self._leds, self.map_value_to_led_states(self._parameter_to_map_to.value)):
            led.send_value(state, force)


def map_value_to_led_states(on, off, num_leds, value):
    """
    Given `value` in the range [-1, 1], return an iterator
    that provides `num_leds` led states.

    Assuming that we have a strip of evenly spaced leds indexed from
    left to right, an led has state `on` if its offset from the center is in
    the same direction as `value` and the normalized magnitude of the offset
    is less than or equal to the magnitude of `value`.

    Otherwise it is `off`
    """
    assert -1.0 <= value <= 1, b'The input value must be in the range [-1, 1]'
    assert num_leds % 2 != 0, b'There must be an odd number of leds'
    assert num_leds >= 3, b'There must be at least 3 leds'
    mid_index = int(math.floor(num_leds / 2))
    active_length = mid_index + 1
    active_led_states = map(lambda i: on if i / active_length <= abs(value) else off, map(float, range(active_length)))
    inactive_led_states = repeat(0, num_leds - active_length)
    if value < 0:
        return chain(reversed(active_led_states), inactive_led_states)
    return chain(inactive_led_states, active_led_states)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/touch_strip.pyc
