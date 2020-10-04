# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\view_toggle.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ToggleButtonControl

class ViewToggleComponent(Component):
    detail_view_toggle_button = ToggleButtonControl()
    main_view_toggle_button = ToggleButtonControl()

    def __init__(self, *a, **k):
        super(ViewToggleComponent, self).__init__(*a, **k)
        self.__on_detail_view_visibility_changed.subject = self.application.view
        self.__on_main_view_visibility_changed.subject = self.application.view
        self.__on_detail_view_visibility_changed()
        self.__on_main_view_visibility_changed()

    @detail_view_toggle_button.toggled
    def detail_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, b'Detail')

    @main_view_toggle_button.toggled
    def main_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, b'Session')

    def _show_or_hide_view(self, show_view, view_name):
        if show_view:
            self.application.view.show_view(view_name)
        else:
            self.application.view.hide_view(view_name)

    @listens(b'is_view_visible', b'Detail')
    def __on_detail_view_visibility_changed(self):
        self.detail_view_toggle_button.is_toggled = self.application.view.is_view_visible(b'Detail')

    @listens(b'is_view_visible', b'Session')
    def __on_main_view_visibility_changed(self):
        self.main_view_toggle_button.is_toggled = self.application.view.is_view_visible(b'Session')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/view_toggle.pyc
