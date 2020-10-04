# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\note_pad.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import PlayableControl

class NotePadMixin(object):

    def set_matrix(self, matrix):
        super(NotePadMixin, self).set_matrix(matrix)
        for button in self.matrix:
            button.set_mode(PlayableControl.Mode.playable_and_listenable)
            button.pressed_color = b'NotePad.Pressed'

    def _on_matrix_pressed(self, _):
        pass

    def _on_matrix_released(self, button):
        self._update_button_color(button)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/note_pad.pyc
