# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\BlinkingButtonElement.py
# Compiled at: 2017-03-07 13:28:52
import _Framework.Task
from SpecialButtonElement import SpecialButtonElement, DummyUndoStepHandler, Skin
from consts import MIDI_RANGE
SLOW_BLINK = 4
FAST_BLINK = 2

class BlinkingButtonElement(SpecialButtonElement):
    """ BlinkingButtonElement is an extended SpecialButtonElement that provides
    blinking LED states.  A variant (OverridingBlinkingButtonElement) for use with
    buttons that have locally controlled LEDs is available in this module. """

    def __init__(self, is_momentary, msg_type, channel, identifier, skin=Skin(), undo_step_handler=DummyUndoStepHandler(), *a, **k):
        self._blinking_active = False
        self._blink_on = False
        self._blink_speed = 0
        self._timer_count = 0
        self._blink_on_color = int(skin['DefaultButton.On'])
        self._blink_off_color = int(skin['DefaultButton.Off'])
        super(BlinkingButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin, undo_step_handler, *a, **k)

        def wrapper(_):
            self._on_timer()
            return _Framework.Task.RUNNING

        self._tasks.add(_Framework.Task.FuncTask(wrapper, self._on_timer))

    def send_value(self, value, force=False, channel=None):
        """ Extends standard to deactivate blinking. """
        self._blinking_active = False
        super(BlinkingButtonElement, self).send_value(value, force, channel)

    def blink(self, blink_on_color, slow_blink):
        """ Initiates blinking that will cause the button to flash between the given color
        and the button's off value either slowly or quickly. """
        assert blink_on_color in MIDI_RANGE
        self._blink_on_color = blink_on_color
        self._blink_speed = SLOW_BLINK if bool(slow_blink) else FAST_BLINK
        self._blink_on = True
        self._blinking_active = True

    def _on_timer(self):
        """ Handles blinking the LED in a way that will be in sync with other buttons
        blinking. """
        if self._blinking_active:
            if not self._blink_on:
                self._do_send_value(self._blink_on_color)
                self._blink_on = True
            elif self._timer_count % self._blink_speed == 0:
                self._do_send_value(self._blink_off_color)
                self._blink_on = False
        self._timer_count += 1


class OverridingBlinkingButtonElement(BlinkingButtonElement):
    """ Specialized BlinkingButtonElement that overrides the local LED control of a
    button to prevent the button turning itself off when it should not. """

    def __init__(self, *a, **k):
        self._last_value_to_button = 0
        super(OverridingBlinkingButtonElement, self).__init__(*a, **k)

    def send_value(self, value, **k):
        self._last_value_to_button = value
        super(OverridingBlinkingButtonElement, self).send_value(value, **k)

    def receive_value(self, value):
        super(OverridingBlinkingButtonElement, self).receive_value(value)
        if value is 0 and self._last_value_to_button and not self._blinking_active:
            self.send_value(self._last_value_to_button, force=True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/BlinkingButtonElement.pyc
