# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\PluginLoaderComponent.py
# Compiled at: 2017-04-24 12:52:35
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot_group
from _Framework.Util import lazy_attribute
from ControlUtils import set_group_button_lights
from ShowMessageMixin import ShowMessageMixin

class PluginLoaderComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ PluginLoaderComponent allows for user-specified plugin devices to be loaded
    directly via buttons. """

    def __init__(self, num_load_buttons, color_class=None, name='Plugin_Loader', *a, **k):
        self._color_names = color_class.__dict__.keys() if color_class else None
        self._color_class_name = str(color_class).split('.')[(-1)] if color_class else ''
        self._load_buttons = None
        self._load_button_colors = [ 'DefaultButton.On' for _ in xrange(num_load_buttons) ]
        self._plugin_list = [ None for _ in xrange(num_load_buttons) ]
        super(PluginLoaderComponent, self).__init__(name=name, *a, **k)
        return

    def disconnect(self):
        super(PluginLoaderComponent, self).disconnect()
        self._color_names = None
        self._color_class_name = None
        self._load_buttons = None
        self._load_button_colors = None
        self._plugin_list = None
        return

    def set_load_buttons(self, buttons):
        """ Sets the buttons to use for loading plugins. If the number of buttons
        passed is not equal to the number of button colors, the list of colors will
        be set to None. """
        self._load_buttons = list(buttons) if buttons else None
        if buttons and self._load_button_colors:
            if len(buttons) != len(self._load_button_colors):
                self._load_button_colors = None
        self._on_load_buttons_value.replace_subjects(buttons or [])
        self._update_load_buttons()
        return

    def parse_settings(self, settings):
        """ Parses the given dict of settings for plugin and (if applicable) color
        settings. """
        if settings:
            try:
                for k, v in settings.iteritems():
                    if k.startswith('PLUGIN_'):
                        self._plugin_list[int(k.replace('PLUGIN_', '')) - 1] = v
                    elif k.startswith('BUTTON_'):
                        index = int(k.replace('BUTTON_', '').replace('_COLOR', '')) - 1
                        self._load_button_colors[index] = self._parse_color_value(v)

            except:
                self._load_button_colors = None
                self._plugin_list = None

            if self._plugin_list:
                browser_items = []
                for p in self._plugin_list:
                    browser_items.append(self._available_plugins.get(p, None))

                self._plugin_list = browser_items
        return

    def _parse_color_value(self, color):
        if self._color_names:
            if color in self._color_names:
                return '%s.%s' % (self._color_class_name, color)
        return

    @lazy_attribute
    def _available_plugins(self):
        d = {}
        self._add_plugins_for_item_list(self.application().browser.plugins.children, d)
        return d

    def _add_plugins_for_item_list(self, item_list, plugin_dict):
        for i in item_list:
            if i.is_folder:
                self._add_plugins_for_item_list(i.iter_children, plugin_dict)
            else:
                plugin_dict[i.name.upper()] = i

    @subject_slot_group('value')
    def _on_load_buttons_value(self, value, button):
        if value and self._plugin_list:
            btn_index = self._load_buttons.index(button)
            if btn_index < len(self._plugin_list):
                item = self._plugin_list[btn_index]
                if item:
                    self.component_message('Loading Plugin', item.name)
                    task = partial(self.application().browser.load_item, item)
                    self.canonical_parent.schedule_message(2, task)

    def update(self):
        super(PluginLoaderComponent, self).update()
        self._update_load_buttons()

    def _update_load_buttons(self):
        if self.is_enabled() and self._load_buttons:
            if self._load_button_colors and self._plugin_list:
                for index, button in enumerate(self._load_buttons):
                    if button:
                        color = None
                        item = None
                        if index < len(self._load_button_colors) and index < len(self._plugin_list):
                            color = self._load_button_colors[index]
                            item = self._plugin_list[index]
                        button.set_light(color if color and item else 'DefaultButton.Off')

            else:
                set_group_button_lights(self._load_buttons, 'DefaultButton.Off')
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/PluginLoaderComponent.pyc
