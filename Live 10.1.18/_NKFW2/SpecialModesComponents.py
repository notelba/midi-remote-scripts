# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialModesComponents.py
# Compiled at: 2017-10-19 12:46:57
from _Framework.ModesComponent import Mode, ModesComponent, ModeButtonBehaviour, LatchingBehaviour, subject_slot, partial
from ControlUtils import is_button_pressed

class CallMethodMode(Mode):
    """ CallMethodMode can call the method of an object upon entering the mode and
    optionally upon leaving the mode. Can also optionally pass an arg to the method or
    indicate when the mode is entered and left. """

    def __init__(self, obj, method_name, method_arg='not_an_arg', call_on_leave=False, indicate_on_leave=False):
        self._method = getattr(obj, method_name)
        self._method_arg = method_arg
        self._indicate_on_leave = bool(indicate_on_leave)
        self._call_on_leave = bool(call_on_leave) or self._indicate_on_leave

    def enter_mode(self):
        self._do_call(True)

    def leave_mode(self):
        if self._call_on_leave:
            self._do_call()

    def _do_call(self, mode_entered=False):
        if self._indicate_on_leave:
            self._method(mode_entered)
        elif self._method_arg is 'not_an_arg':
            self._method()
        else:
            self._method(self._method_arg)


class NonUpdatingBehaviour(ModeButtonBehaviour):
    """ Behaviour that wraps another behaviour and doesn't update button LEDs. """

    def __init__(self, behaviour):
        self._behaviour = behaviour
        self.press_immediate = self._behaviour.press_immediate
        self.release_immediate = self._behaviour.release_immediate
        self.press_delayed = self._behaviour.press_delayed
        self.release_delayed = self._behaviour.release_delayed
        self.update_button = lambda *a: None


class SkinnedLatchingBehaviour(LatchingBehaviour):
    """ Specialized LatchingBehaviour that works with skin values. """

    def __init__(self, selected_value='Modes.Selected', not_selected_value='Modes.NotSelected', *a, **k):
        super(SkinnedLatchingBehaviour, self).__init__(*a, **k)
        self._selected_value = selected_value
        self._not_selected_value = not_selected_value

    def update_button(self, component, mode, selected_mode):
        """ Overrides standard to handle skin values. """
        button = component.get_mode_button(mode)
        groups = component.get_mode_groups(mode)
        selected_groups = component.get_mode_groups(selected_mode)
        if mode == selected_mode or bool(groups & selected_groups):
            button.set_light(self._selected_value)
        else:
            button.set_light(self._not_selected_value)


class ReenteringLatchingBehaviour(SkinnedLatchingBehaviour):
    """ Specialized SkinnedLatchingBehaviour that calls a callback when the mode is
    selected and the associated mode select button is pressed again. """

    def __init__(self, reenter_callback, *a, **k):
        super(ReenteringLatchingBehaviour, self).__init__(*a, **k)
        self._reenter_callback = reenter_callback

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(ReenteringLatchingBehaviour, self).press_immediate(component, mode)
        if was_active:
            self._reenter_callback()


class ImmediateReenteringLatchingBehaviour(ReenteringLatchingBehaviour):
    """ Specialized ReenteringLatchingBehaviour that always calls the callback. """

    def press_immediate(self, component, mode):
        self._reenter_callback()
        super(ReenteringLatchingBehaviour, self).press_immediate(component, mode)


class ExitingLatchingBehaviour(SkinnedLatchingBehaviour):
    """ Specialized SkinnedLatchingBehaviour that exits all modes when the current mode
    is exited. """

    def press_immediate(self, component, mode):
        """ Overrides standard to exit all modes if the given mode is currently
        selected. """
        if mode == component.selected_mode:
            component.selected_mode = None
            component._last_selected_mode = None
        else:
            component.push_mode(mode)
        return

    def release_immediate(self, component, mode):
        """ Overrides standard to do nothing. """
        pass

    def release_delayed(self, component, _):
        """ Overrides standard to exit all modes. """
        component.selected_mode = None
        return


class ExitingBehaviour(ExitingLatchingBehaviour):
    """ Like ExitingLatchingBehaviour, but purely momentary. """

    def release_immediate(self, component, mode):
        """ Overrides standard to exit all modes. """
        component.selected_mode = None
        return


class SpecialModesComponent(ModesComponent):
    """ Specialized ModesComponent that uses a select button (in addition to a shift
    button) for muting mode selection buttons. """

    def __init__(self, *a, **k):
        super(SpecialModesComponent, self).__init__(*a, **k)
        self._select_button = None
        return

    def disconnect(self):
        super(SpecialModesComponent, self).disconnect()
        self._select_button = None
        return

    def set_select_button(self, button):
        """ Sets the select button to use fr muting mode selection buttons. """
        self._select_button = button

    def _on_mode_button_value(self, name, value, sender):
        if is_button_pressed(self._select_button):
            return
        super(SpecialModesComponent, self)._on_mode_button_value(name, value, sender)

    @subject_slot('value')
    def _on_toggle_value(self, value):
        if is_button_pressed(self._select_button):
            return
        super(SpecialModesComponent, self)._on_toggle_value(value)


class MomentaryModesComponent(ModesComponent):
    """ Specialized ModesComponent that uses the toggle_button purely as a momentary
    button for switching between two modes and does not update LEDs. """

    def set_toggle_button(self, button):
        """ Overrides standard to not reset button. """
        self._mode_toggle = button
        self._on_toggle_value.subject = button

    @subject_slot('value')
    def _on_toggle_value(self, value):
        """ Overrides standard to momentarily switch between modes. """
        if self.is_enabled():
            self.selected_mode = self._mode_list[(1 if value else 0)]

    def _update_buttons(self, selected):
        """ Overrides standard to not update LEDs. """
        pass


class IndexedModesComponent(ModesComponent):
    """ Specialized ModesComponent that uses mode indexes for setting buttons
    and for notifying other components. Also, uses SkinnedLatchingBehaviour
    as the default. """

    def __init__(self, enumerate_mode_names=False, *a, **k):
        self._enumerate_mode_names = bool(enumerate_mode_names)
        super(IndexedModesComponent, self).__init__(*a, **k)

    @property
    def num_modes(self):
        """ Returns the number of modes this component has. """
        return len(self._mode_list)

    def add_mode(self, name, mode_or_component, toggle_value=False, groups=set(), behaviour=None):
        """ Extends standard to create buttons settings for mode indexes
        (such as set_mode_0_button). """
        if self._enumerate_mode_names:
            name = '%s: %s' % (len(self._mode_list) + 1, name)
        behaviour = SkinnedLatchingBehaviour() if behaviour is None else behaviour
        super(IndexedModesComponent, self).add_mode(name, mode_or_component, toggle_value, groups, behaviour)
        mode_index = len(self._mode_list) - 1
        button_setter = 'set_mode_%s_button' % mode_index
        if not hasattr(self, button_setter):
            setattr(self, button_setter, partial(self.set_mode_button, mode_index))
        return

    def set_mode_button(self, mode_index, button):
        """ Overrides standard to set mode button by index. """
        if button and self.is_enabled():
            button.reset()
        self._mode_map[self._mode_list[mode_index]].subject_slot.subject = button
        self._update_buttons(self.selected_mode)

    def set_mode_buttons(self, buttons):
        """ Sets the group of buttons to use for selecting modes. """
        buttons = list(buttons) if buttons else []
        if buttons:
            for index, button in enumerate(buttons):
                if button:
                    button.reset()
                self._mode_map[self._mode_list[index]].subject_slot.subject = button

        else:
            for mode in self._mode_list:
                self._mode_map[mode].subject_slot.subject = None

        self._update_buttons(self.selected_mode)
        return

    def _do_enter_mode(self, name):
        """ Overrides standard to notify index too. """
        entry = self._mode_map[name]
        entry.mode.enter_mode()
        self._update_buttons(name)
        self.notify_selected_mode(name, self._mode_list.index(name))

    def get_mode_by_index(self, index):
        return self.get_mode(self._mode_list[index])

    def _get_selected_mode_index(self):
        if self.selected_mode is None:
            return
        else:
            return self._mode_list.index(self.selected_mode)

    def _set_selected_mode_index(self, index):
        self.selected_mode = self._mode_list[index]

    selected_mode_index = property(_get_selected_mode_index, _set_selected_mode_index)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialModesComponents.pyc
