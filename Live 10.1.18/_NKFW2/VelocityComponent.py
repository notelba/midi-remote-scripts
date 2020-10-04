# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\VelocityComponent.py
# Compiled at: 2017-03-07 13:28:53
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from SpecialControl import ReselectableRadioButtonGroup, SpecialButtonControl
from ShowMessageMixin import ShowMessageMixin
FIXED_VELOCITIES = (127, 100, 73, 46)
VELO_FIXED = 0
VELO_RANDOM_FULL_RANGE = 4
VELO_RANDOM_HI_RANGE = 5
VELO_RANDOM_LOW_RANGE = 6
VELO_INPUT = 7
DEFAULT_VELO_INDEX = 1
VELO_TYPE_NAMES = ('Fixed (127)', 'Fixed (100)', 'Fixed (73)', 'Fixed (46)', 'Random (1-127)',
                   'Random (63-127)', 'Random (10-63)', 'Input')

class VelocityComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ VelocityComponent determines the velocity to be used for sequencing
    components and also allows for enabling full velocity for note input controls.
    This needs to be extended to add controls for controlling the velocity. A
    standard implementation (StandardVelocityComponent) is provided in this module. """
    __subject_events__ = ('velocity', 'full_velocity')
    full_velocity_button = SpecialButtonControl(color='Instrument.FullVelocity.Off', on_color='Instrument.FullVelocity.On', disabled_color='Instrument.FullVelocity.Inactive')

    def __init__(self, name='Velocity_Control', from_test=False, *a, **k):
        super(VelocityComponent, self).__init__(name, *a, **k)
        self._full_velocity = None
        if not from_test:
            self._full_velocity = self.canonical_parent._c_instance.full_velocity
        self._fixed_velocity = 100
        self._velocity_type = VELO_FIXED
        return

    def get_velocity(self, input_velocity):
        """ Returns the velocity to use for step sequencing. This will return
        the given input_velocity if the velocity type is input or a fixed/random
        velocity otherwise. """
        if self._velocity_type == VELO_INPUT:
            return input_velocity
        if self._velocity_type == VELO_FIXED:
            return self._fixed_velocity
        if self._velocity_type == VELO_RANDOM_LOW_RANGE:
            return Live.Application.get_random_int(10, 54)
        if self._velocity_type == VELO_RANDOM_HI_RANGE:
            return Live.Application.get_random_int(63, 65)
        if self._velocity_type == VELO_RANDOM_FULL_RANGE:
            return Live.Application.get_random_int(1, 128)

    @full_velocity_button.pressed
    def full_velocity_button(self, _):
        self._toggle_full_velocity()

    @full_velocity_button.released_delayed
    def full_velocity_button(self, _):
        self._toggle_full_velocity(True)

    @full_velocity_button.pressed_delayed
    def full_velocity_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    @full_velocity_button.released_immediately
    def full_velocity_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    def _toggle_full_velocity(self, is_release=False):
        """ Toggles full velocity, notifies listeners and shows info
        in status bar. """
        if not is_release or self._full_velocity.enabled:
            self._full_velocity.enabled = not self._full_velocity.enabled
            self.full_velocity_button.is_on = self._full_velocity.enabled
            self.notify_full_velocity(self._full_velocity.enabled)
            self.component_message('Full Velocity', 'On' if self._full_velocity.enabled else 'Off')


class StandardVelocityComponent(VelocityComponent):
    """ StandardVelocityComponent is a VelocityComponent set up for a group of
    8 buttons for controlling sequence velocity. """

    def __init__(self, num_buttons=8, include_input=False, *a, **k):
        super(StandardVelocityComponent, self).__init__(*a, **k)
        self._include_input = False
        self._toggle_random = False
        if num_buttons > 4 and num_buttons < 8:
            self._include_input = bool(include_input)
            self._toggle_random = not self._include_input
        self._velocity_buttons = ReselectableRadioButtonGroup(num_buttons, DEFAULT_VELO_INDEX, checked_color='Sequence.Velocity.Selected', unchecked_color='Sequence.Velocity.NotSelected')
        self._on_velocity_button_value.subject = self._velocity_buttons

    def set_velocity_buttons(self, buttons):
        self._velocity_buttons.set_buttons(buttons)

    @subject_slot('checked_index')
    def _on_velocity_button_value(self, index):
        if self.is_enabled():
            if index < VELO_RANDOM_FULL_RANGE:
                self._fixed_velocity = FIXED_VELOCITIES[index]
                self._velocity_type = VELO_FIXED
            else:
                if self._include_input:
                    self._velocity_type = VELO_INPUT
                elif self._toggle_random:
                    current = self._velocity_type
                    if current < VELO_RANDOM_FULL_RANGE or current == VELO_RANDOM_LOW_RANGE:
                        self._velocity_type = VELO_RANDOM_FULL_RANGE
                    else:
                        self._velocity_type += 1
                else:
                    self._velocity_type = index
                index = self._velocity_type
            self.notify_velocity()
            self.component_message('Sequence Velocity', VELO_TYPE_NAMES[index])
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/VelocityComponent.pyc
