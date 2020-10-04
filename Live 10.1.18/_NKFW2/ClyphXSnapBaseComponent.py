# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClyphXSnapBaseComponent.py
# Compiled at: 2018-01-15 18:16:49
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot_group
from ShowMessageMixin import ShowMessageMixin
from ControlUtils import is_button_pressed

class TracksToSnap(object):
    """ Flag for the track(s) to include in snaps. """
    ALL = 0
    CURRENT = 1


class ClyphXSnapBaseComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ Base component that allows a matrix or group of buttons to trigger
    ClyphX/Clyphx Pro Snaps. """
    __subject_events__ = ('snap_data', )

    def __init__(self, num_buttons=8, snap_args='', recall_args='recall', header='', tracks_to_snap=TracksToSnap.ALL, targets_comp=None, name='ClyphX_Snap_Control', *a, **k):
        super(ClyphXSnapBaseComponent, self).__init__(name=name, *a, **k)
        self._header = header.lower()
        self._num_snaps = num_buttons
        self._snap_component = None
        self._snap_data = self.get_initial_snap_data(num_buttons)
        self._snap_args = snap_args
        self._recall_args = recall_args
        self._tracks_to_snap = tracks_to_snap
        self._targets_comp = targets_comp
        self._snap_buttons = None
        self._delete_button = None
        return

    def disconnect(self):
        super(ClyphXSnapBaseComponent, self).disconnect()
        self._header = None
        self._snap_component = None
        self._snap_data = None
        self._targets_comp = None
        self._snap_buttons = None
        self._delete_button = None
        return

    def set_clyphx_instance(self, instance):
        """ Sets the ClyphX instance to use (or None). """
        raise NotImplementedError

    def set_snap_buttons(self, buttons):
        """ Sets the buttons to use for storing/recalling snaps. """
        self._snap_buttons = list(buttons) if buttons else []
        self._on_button_value.replace_subjects(self._snap_buttons)
        self._update_snap_buttons()

    def set_delete_button(self, button):
        """ Sets the modifier button to use for deleting stored snaps. """
        self._delete_button = button

    def get_initial_snap_data(self, num_buttons):
        """ Returns the array of snap data to use for the given num_buttons. """
        raise NotImplementedError

    def rebuild(self, data):
        """ Rebuilds snap data based on the given data list. """
        pass

    def delete_snap(self, snap, btn_id):
        """ Handles deleting the given snap. """
        raise NotImplementedError

    def store_or_recall_snap(self, snap, btn_id):
        """ Handles storing or recalling a snap. """
        raise NotImplementedError

    def button_has_snap(self, btn_id):
        """ Returns whether the given button index has an associated snap. """
        raise NotImplementedError

    @subject_slot_group('value')
    def _on_button_value(self, value, button):
        if value and self._snap_component:
            btn_id = self._snap_buttons.index(button)
            snap = self._snap_data[btn_id]
            if is_button_pressed(self._delete_button):
                self.delete_snap(snap, btn_id)
                return
            self.store_or_recall_snap(snap, btn_id)

    def update(self):
        super(ClyphXSnapBaseComponent, self).update()
        self._update_snap_buttons()

    def _update_snap_buttons(self):
        if self.is_enabled() and self._snap_buttons:
            for i, b in enumerate(self._snap_buttons):
                if b:
                    if self.button_has_snap(i):
                        b.set_light('Global.HasSnap')
                    else:
                        b.set_light('DefaultButton.Off')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClyphXSnapBaseComponent.pyc
