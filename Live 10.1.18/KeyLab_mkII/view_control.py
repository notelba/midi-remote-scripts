# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\view_control.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import find_if, listens, liveobj_valid
from ableton.v2.control_surface.control import ButtonControl
from KeyLab_Essential.view_control import ViewControlComponent as ViewControlComponentBase
MAIN_VIEWS = ('Session', 'Arranger')

class ViewControlComponent(ViewControlComponentBase):
    document_view_toggle_button = ButtonControl()

    def __init__(self, *a, **k):
        super(ViewControlComponent, self).__init__(*a, **k)
        self.__on_focused_document_view_changed.subject = self.application.view
        self.__on_focused_document_view_changed()

    @document_view_toggle_button.pressed
    def document_view_toggle_button(self, _):
        is_session_visible = self.application.view.is_view_visible(b'Session', main_window_only=True)
        self.show_view(b'Arranger' if is_session_visible else b'Session')

    @listens(b'focused_document_view')
    def __on_focused_document_view_changed(self):
        self.document_view_toggle_button.color = (b'View.{}').format(self.application.view.focused_document_view)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_mkII/view_control.pyc
