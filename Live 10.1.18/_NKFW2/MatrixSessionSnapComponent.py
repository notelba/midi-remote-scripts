# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\MatrixSessionSnapComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot
from SessionSnap import SessionSnap
from ControlUtils import is_button_pressed

class MatrixSessionSnapComponent(ControlSurfaceComponent):
    """ MatrixSessionSnapComponent allows a matrix or group of buttons to be used for
    storing/recalling session snaps. """
    __subject_events__ = ('snap_data', )

    def __init__(self, num_buttons=64, name='Matrix_Session_Snap_Component', *a, **k):
        super(MatrixSessionSnapComponent, self).__init__(name=name, *a, **k)
        self._launch_buttons = None
        self._shift_button = None
        self._delete_button = None
        self._store_button = None
        self._snaps = [ None for _ in xrange(num_buttons) ]
        self._rebuild_data = None
        return

    def disconnect(self):
        for snap in self._snaps:
            if snap:
                snap.disconnect()

        super(MatrixSessionSnapComponent, self).disconnect()
        self._launch_buttons = None
        self._shift_button = None
        self._delete_button = None
        self._store_button = None
        self._snaps = None
        self._rebuild_data = None
        return

    def set_launch_buttons(self, buttons):
        """ Sets the buttons to use for triggering snaps. """
        self._launch_buttons = list(buttons) if buttons else []
        self._on_launch_button_value.replace_subjects(self._launch_buttons)
        self._update_launch_buttons()

    def set_shift_button(self, button):
        """ Sets the shift button that changes the functionality of other controls. """
        self._shift_button = button

    def set_store_button(self, button):
        """ Sets the button to use for storing snaps. """
        self._store_button = button
        self._on_store_button_value.subject = button
        self._update_store_and_delete_buttons()

    def set_delete_button(self, button):
        """ Sets the button to use for deleting snaps. """
        self._delete_button = button
        self._on_delete_button_value.subject = button
        self._update_store_and_delete_buttons()

    def rebuild(self, data):
        """ Rebuilds snap data based on the given data list. """
        if self.is_enabled():
            for i, s in enumerate(data):
                if s is not None:
                    snap = SessionSnap(self.song())
                    snap.rebuild(s)
                    self._snaps[i] = snap

            self._update_launch_buttons()
            self._rebuild_data = None
        else:
            self._rebuild_data = data
        return

    @subject_slot_group('value')
    def _on_launch_button_value(self, value, button):
        if self.is_enabled() and value:
            btn_index = self._launch_buttons.index(button)
            if is_button_pressed(self._store_button):
                self._snaps[btn_index] = SessionSnap(self.song())
                self._snaps[btn_index].store()
                self._update_launch_buttons()
                self._notify_snap_data()
            elif is_button_pressed(self._delete_button):
                self._snaps[btn_index] = None
                button.set_light('DefaultButton.Off')
                self._notify_snap_data()
            elif self._snaps[btn_index] is not None:
                quantized = not is_button_pressed(self._shift_button)
                self._snaps[btn_index].recall(quantized)
        return

    def _notify_snap_data(self):
        if self._snaps is not None:
            data = []
            for snap in self._snaps:
                data.append(snap.data if snap else None)

            self.notify_snap_data(data)
        return

    @subject_slot('value')
    def _on_store_button_value(self, value):
        if self.is_enabled():
            self._store_button.set_light('Modifiers.Pressed' if value else 'Modifiers.Store')

    @subject_slot('value')
    def _on_delete_button_value(self, value):
        if self.is_enabled():
            if value:
                if self._launch_buttons:
                    for index, button in enumerate(self._launch_buttons):
                        if button:
                            if self._snaps[index] is not None:
                                button.set_light('Global.CanDelete')

            else:
                self._update_launch_buttons()
            self._delete_button.set_light('Modifiers.Pressed' if value else 'Modifiers.Delete')
        return

    def update(self):
        super(MatrixSessionSnapComponent, self).update()
        self._update_launch_buttons()
        self._update_store_and_delete_buttons()
        if self.is_enabled() and self._rebuild_data:
            self.rebuild(self._rebuild_data)

    def _update_launch_buttons(self):
        if self.is_enabled() and self._launch_buttons:
            for index, button in enumerate(self._launch_buttons):
                if self._snaps[index] is not None:
                    button.set_light('Global.HasSnap')
                else:
                    button.set_light('DefaultButton.Off')

        return

    def _update_store_and_delete_buttons(self):
        if self.is_enabled():
            if self._store_button:
                self._store_button.set_light('Modifiers.Store')
            if self._delete_button:
                self._delete_button.set_light('Modifiers.Delete')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/MatrixSessionSnapComponent.pyc
