# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\PluginPresetComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from SpecialControl import SpecialButtonControl
from ControlUtils import set_group_button_lights
from ShowMessageMixin import ShowMessageMixin, DisplayType

class PluginPresetComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ PluginPresetComponent allows for selecting a plugin's presets via prev and next
    buttons. An implementation for use with a matrix (MatrixPluginPresetComponent) is
    also provided in this module. """
    color_dict = dict(color='Navigation.Disabled', on_color='Navigation.PresetEnabled')
    prev_preset_button = SpecialButtonControl(**color_dict)
    next_preset_button = SpecialButtonControl(**color_dict)

    def __init__(self, targets_comp=None, name='Plugin_Preset_Control', *a, **k):
        super(PluginPresetComponent, self).__init__(name=name, *a, **k)
        self._device = None
        self._num_presets = 0
        self._on_target_plugin_changed.subject = targets_comp
        return

    def disconnect(self):
        super(PluginPresetComponent, self).disconnect()
        self._device = None
        return

    def set_plugin(self, device):
        """ Sets the plugin to control. """
        self._device = device
        self._on_presets_changed.subject = self._device
        self._on_selected_preset_index_changed.subject = self._device
        self._on_presets_changed()

    def select_preset_index(self, index):
        """ Selects the given preset index if possible. """
        if self._device and index in xrange(self._num_presets):
            self._device.selected_preset_index = index
            self.component_message('Loading %s Preset %s' % (
             self._device.name, index + 1), self._device.presets[index], display_type=DisplayType.STATUS)
            self.component_message(self._device.name, '%s: %s' % (index + 1, self._device.presets[index]), display_type=DisplayType.PHYSICAL)

    @prev_preset_button.pressed
    def prev_preset_button(self, _):
        self._increment_preset_index(-1)

    @next_preset_button.pressed
    def next_preset_button(self, _):
        self._increment_preset_index(1)

    def _increment_preset_index(self, factor):
        if self._device:
            should_reset = self.prev_preset_button.is_pressed and self.next_preset_button.is_pressed
            index = 0 if should_reset else self._device.selected_preset_index + factor
            self.select_preset_index(index)

    @subject_slot('target_plugin')
    def _on_target_plugin_changed(self, device):
        self.set_plugin(device)

    @subject_slot('presets')
    def _on_presets_changed(self):
        if self._device:
            self._num_presets = len(self._device.presets)
        self.update()

    @subject_slot('selected_preset_index')
    def _on_selected_preset_index_changed(self):
        self.update()

    def update(self):
        super(PluginPresetComponent, self).update()
        self._update_preset_nav_buttons()

    def _update_preset_nav_buttons(self):
        if self.is_enabled():
            can_enable = self._device is not None
            self.prev_preset_button.is_on = can_enable and self._device.selected_preset_index > 0
            self.next_preset_button.is_on = can_enable and self._device.selected_preset_index < self._num_presets - 1
        return


class MatrixPluginPresetComponent(PluginPresetComponent):
    """ MatrixPluginPresetComponent is a PluginPresetComponent that allows presets to
    be selected from a matrix. """
    color_dict = dict(color='Navigation.Disabled', on_color='Navigation.PageEnabled')
    prev_page_button = SpecialButtonControl(**color_dict)
    next_page_button = SpecialButtonControl(**color_dict)

    def __init__(self, *a, **k):
        self._selection_buttons = None
        self._num_selection_buttons = 0
        self._page_offset = 0
        super(MatrixPluginPresetComponent, self).__init__(*a, **k)
        return

    def disconnect(self):
        super(MatrixPluginPresetComponent, self).disconnect()
        self._selection_buttons = None
        return

    def set_selection_buttons(self, buttons):
        """ Sets the button to use for selecting presets. """
        self._selection_buttons = list(buttons) if buttons else None
        self._num_selection_buttons = len(self._selection_buttons) if buttons else 0
        self._on_selection_buttons_value.replace_subjects(buttons or [])
        self.update()
        return

    @subject_slot_group('value')
    def _on_selection_buttons_value(self, value, button):
        if value:
            index = self._selection_buttons.index(button) + self._page_offset
            self.select_preset_index(index)

    @prev_page_button.pressed
    def prev_page_button(self, _):
        if self._page_offset != 0:
            self._handle_page_change(-self._num_selection_buttons)

    @next_page_button.pressed
    def next_page_button(self, _):
        if self._can_move_to_next_page():
            self._handle_page_change(self._num_selection_buttons)

    def _handle_page_change(self, factor):
        should_reset = self.prev_page_button.is_pressed and self.next_page_button.is_pressed
        if should_reset:
            self._page_offset = 0
        else:
            self._page_offset += factor
        self.update()
        page_range = '%s - %s' % (self._page_offset + 1,
         self._page_offset + self._num_selection_buttons)
        self.component_message('Navigating Presets', page_range)

    def _can_move_to_next_page(self):
        if self._device and self._num_presets and self._num_selection_buttons:
            return self._page_offset + self._num_selection_buttons < self._num_presets
        return False

    def update(self):
        super(MatrixPluginPresetComponent, self).update()
        self._update_selection_buttons()
        self._update_page_buttons()

    def _update_selection_buttons(self):
        if self.is_enabled() and self._selection_buttons:
            if self._device and self._num_presets:
                for index, button in enumerate(self._selection_buttons):
                    preset_index = index + self._page_offset
                    if preset_index == self._device.selected_preset_index:
                        button.set_light('Preset.Selected')
                    elif preset_index < self._num_presets:
                        button.set_light('Preset.NotSelected')
                    else:
                        button.set_light('DefaultButton.Off')

            else:
                set_group_button_lights(self._selection_buttons, 'DefaultButton.Off')

    def _update_page_buttons(self):
        if self.is_enabled():
            can_enable = self._device and self._num_presets and self._num_selection_buttons
            self.prev_page_button.is_on = can_enable and self._page_offset != 0
            self.next_page_button.is_on = can_enable and self._can_move_to_next_page()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/PluginPresetComponent.pyc
