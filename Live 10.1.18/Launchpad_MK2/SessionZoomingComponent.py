# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\SessionZoomingComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SessionZoomingComponent import SessionZoomingComponent as SessionZoomingComponentBase
from .ComponentUtils import skin_scroll_component
from _Framework.SessionComponent import SessionComponent

class SessionZoomingComponent(SessionZoomingComponentBase):

    def _enable_skinning(self):
        super(SessionZoomingComponent, self)._enable_skinning()
        map(skin_scroll_component, (self._horizontal_scroll, self._vertical_scroll))

    def register_component(self, component):
        assert component != None
        assert component not in self._sub_components
        self._sub_components.append(component)
        return component

    def on_enabled_changed(self):
        self.update()

    def set_enabled(self, enable):
        self._explicit_is_enabled = bool(enable)
        self._update_is_enabled()
        for component in self._sub_components:
            if not isinstance(component, SessionComponent):
                component._set_enabled_recursive(self.is_enabled())
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_MK2/SessionZoomingComponent.pyc
