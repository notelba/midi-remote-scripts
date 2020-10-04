# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialSessionZoomingComponent.py
# Compiled at: 2017-10-03 15:47:47
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.SessionComponent import SessionComponent
from ControlUtils import skin_scroll_component

class SpecialSessionZoomingComponent(SessionZoomingComponent):
    """ Specialized SessionZoomingComponent that provides skinning for scroll buttons
    and also makes this component private by default. """

    def __init__(self, *a, **k):
        super(SpecialSessionZoomingComponent, self).__init__(enable_skinning=True, *a, **k)
        self.is_private = True
        skin_scroll_component(self._vertical_scroll, color='Navigation.SessionEnabled')
        skin_scroll_component(self._horizontal_scroll, color='Navigation.SessionEnabled')

    def on_enabled_changed(self):
        """ Overrides standard to not mess with session highlight. """
        super(SessionZoomingComponent, self).on_enabled_changed()

    def register_component(self, component):
        """ Overrides standard to not register session component to prevent the component
        for being disabled when this component is disabled. """
        if isinstance(component, SessionComponent):
            return component
        return super(SpecialSessionZoomingComponent, self).register_component(component)

    def _on_session_offset_changes(self):
        """ Extends standard to properly update scroll components. """
        super(SpecialSessionZoomingComponent, self)._on_session_offset_changes()
        self._vertical_scroll.update()
        self._horizontal_scroll.update()

    def _can_scroll_up(self):
        return self._session._can_scroll_page_up()

    def _can_scroll_down(self):
        return self._session._can_scroll_page_down()

    def _can_scroll_left(self):
        return self._session._can_scroll_page_left()

    def _can_scroll_right(self):
        return self._session._can_scroll_page_right()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialSessionZoomingComponent.pyc
