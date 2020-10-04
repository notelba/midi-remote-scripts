# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\UndoComponent.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Control import ButtonControl
from ShowMessageMixin import ShowMessageMixin

class UndoComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ Simple component that provide buttons for undo and redo. """
    undo_button = ButtonControl(**dict(color='Undo.Undo', pressed_color='Undo.UndoPressed', disabled_color='DefaultButton.Disabled'))
    redo_button = ButtonControl(**dict(color='Undo.Redo', pressed_color='Undo.RedoPressed', disabled_color='DefaultButton.Disabled'))

    def __init__(self, name='Undo_Control', *a, **k):
        super(UndoComponent, self).__init__(name=name, *a, **k)

    @undo_button.pressed
    def undo_button(self, _):
        if self.song().can_undo:
            self.component_message('Undo', 'Reverted last action')
            self.song().undo()

    @redo_button.pressed
    def redo_button(self, _):
        if self.song().can_redo:
            self.component_message('Redo', 'Re-performed last undone action')
            self.song().redo()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/UndoComponent.pyc
