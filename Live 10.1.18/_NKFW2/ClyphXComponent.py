# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClyphXComponent.py
# Compiled at: 2018-01-15 18:16:49
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot_group
from ControlUtils import set_group_button_lights
from consts import HAS_CX_PRO

class ClyphXComponent(ControlSurfaceComponent):
    """ Component that allows a matrix or group of buttons to trigger ClyphX/ClyphX Pro
    actions that are defined in a file.  The settings for each buttons in the file should
    take one of the following forms:

        For a matrix:
            CX_ROW_x_BTN_x = color_name, on_action_list, off_action_list
        For a button group:
            CX_BTN_x = color_name, on_action_list, off_action_list

    Note that the separator for on/off action lists in ClyphX Pro is a colon. """

    def __init__(self, color_class=None, is_matrix=True, name='ClyphX_Control', *a, **k):
        super(ClyphXComponent, self).__init__(name=name, *a, **k)
        self._color_dict = color_class.__dict__.keys() if color_class else None
        self._color_class_name = str(color_class).split('.')[(-1)] if color_class else ''
        self._is_matrix = bool(is_matrix)
        self._buttons = []
        self._cx_instance = None
        self._cx_settings = {}
        self._parse_method = self._parse_colored_setting if color_class else self._parse_non_colored_setting
        return

    def disconnect(self):
        super(ClyphXComponent, self).disconnect()
        self._color_dict = None
        self._color_class_name = None
        self._buttons = None
        self._cx_instance = None
        self._cx_settings = None
        self._parse_method = None
        return

    def set_buttons(self, buttons):
        """ Sets the group of button to use for triggering ClyphX actions. """
        self._buttons = list(buttons) if buttons else []
        self._on_button_value.replace_subjects(self._buttons)
        self._update_button_leds()

    def set_clyphx_instance(self, instance):
        """ Sets the ClyphX/ClyphX Pro instance to use (or None). """
        self._cx_instance = instance
        self._update_button_leds()

    def parse_settings(self, settings):
        """ Parses the given dict of settings for ClyphX settings. """
        if settings:
            for k, v in settings.iteritems():
                self._parse_method(k, v)

    def _parse_colored_setting(self, setting_key, setting_value):
        """ Parses a setting that includes an LED color. """
        button_index = self._parse_button_index(setting_key)
        if button_index >= 0:
            data = setting_value.split(',')
            if len(data) < 2:
                return
            color_name = data[0].upper().strip()
            if color_name not in self._color_dict:
                color_name = 'DefaultButton.On'
            else:
                color_name = '%s.%s' % (self._color_class_name, color_name)
            self._parse_action_settings(data, button_index, color_name, offset=1)
        return

    def _parse_non_colored_setting(self, setting_key, setting_value):
        """ Parses a setting that does not include an LED color. """
        button_index = self._parse_button_index(setting_key)
        if button_index >= 0:
            data = setting_value.split(',')
            if data:
                self._parse_action_settings(data, button_index, 'DefaultButton.Off')

    def _parse_action_settings(self, data, button_index, color, offset=0):
        """ Parses the given data for ClyphX action lists. """
        if HAS_CX_PRO:
            self._parse_pro_action_sttings(data, button_index, color, offset)
        else:
            on_action = data[offset].strip()
            off_action = None
            if len(data) > 1 + offset:
                off_action = data[(1 + offset)].strip()
            self._cx_settings[button_index] = {'name': NamedControl(on_action), 'color': color, 'on_action': on_action, 
               'off_action': off_action}
        return

    def _parse_pro_action_sttings(self, data, button_index, color, offset):
        """ Parses the given data for ClyphX Pro action lists. """
        actions = (',').join(data[offset:]).split(':')
        on_action = actions[0].strip()
        off_action = actions[1].strip() if len(actions) > 1 else None
        self._cx_settings[button_index] = {'name': NamedControl(on_action), 'color': color, 
           'on_action': on_action, 
           'off_action': off_action}
        return

    def _parse_button_index(self, setting_key):
        """ Parses the given key for the index of the button that the settings
        relate to. """
        try:
            if self._is_matrix:
                row = int(setting_key[7:8]) - 1
                column = int(setting_key[13:]) - 1
                return row * 8 + column
            else:
                return int(setting_key[7:]) - 1

        except ValueError:
            self.canonical_parent.log_message('ValueError when parsing ClyphX settings.')
            return -1

    @subject_slot_group('value')
    def _on_button_value(self, value, button):
        if self.is_enabled() and self._cx_instance and self._cx_settings:
            setting = self._cx_settings.get(self._buttons.index(button))
            if setting:
                if value:
                    if setting['on_action']:
                        setting['name'].name = setting['on_action']
                        self._cx_instance.handle_external_trigger(setting['name'])
                    button.set_light('DefaultButton.Off' if self._color_dict else 'DefaultButton.On')
                else:
                    if setting['off_action']:
                        setting['name'].name = setting['off_action']
                        self._cx_instance.handle_external_trigger(setting['name'])
                    button.set_light(setting['color'])

    def update(self):
        super(ClyphXComponent, self).update()
        self._update_button_leds()

    def _update_button_leds(self):
        if self.is_enabled() and self._buttons:
            if self._cx_instance and self._cx_settings:
                for index, button in enumerate(self._buttons):
                    if button:
                        setting = self._cx_settings.get(index)
                        button.set_light(setting['color'] if setting else 'DefaultButton.Off')

            else:
                set_group_button_lights(self._buttons, 'DefaultButton.Off')


class NamedControl(object):
    """ Simple class that allows controls to have names for use with ClyphX. """

    def __init__(self, name='none'):
        self.name = name
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClyphXComponent.pyc
