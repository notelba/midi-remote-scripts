# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\undo_redo.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .. import Component
from ..control import ButtonControl

class UndoRedoComponent(Component):
    undo_button = ButtonControl()
    redo_button = ButtonControl()

    @undo_button.pressed
    def undo_button(self, button):
        self._undo()

    @redo_button.pressed
    def redo_button(self, button):
        self._redo()

    def _redo(self):
        if self.song.can_redo:
            self.song.redo()

    def _undo(self):
        if self.song.can_undo:
            self.song.undo()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/components/undo_redo.pyc
