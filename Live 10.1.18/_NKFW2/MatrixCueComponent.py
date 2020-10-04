# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\MatrixCueComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.Util import nop
from SessionSnap import SessionSnap
from ShowMessageMixin import ShowMessageMixin
from ControlUtils import set_group_button_lights, is_button_pressed
from Utils import format_absolute_time

class MatrixCueComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ MatrixCueComponent allows a matrix or group of buttons to be used for
    triggering cues (aka locators) and includes a button for adding/removing cues. An
    extended version (MatrixCueSnapComponent) is also included in this module. """

    def __init__(self, name='Matrix_Cue_Control', cue_reached_method=nop, *a, **k):
        super(MatrixCueComponent, self).__init__(name=name, *a, **k)
        self._cue_reached_method = cue_reached_method
        self._cue_buttons = None
        self._add_cue_button = None
        self._shift_button = None
        self._num_buttons = 0
        self._cues = {}
        self._cue_times = []
        self._cue_times_reversed = []
        self._current_cue_index = -1
        self._on_song_time_changed.subject = self.song()
        self._on_playing_state_changed.subject = self.song()
        self._on_cue_added_or_removed.subject = self.song()
        self._on_cue_added_or_removed()
        return

    def disconnect(self):
        super(MatrixCueComponent, self).disconnect()
        self._cue_buttons = None
        self._add_cue_button = None
        self._shift_button = None
        self._cues = None
        self._cue_times = None
        self._cue_times_reversed = None
        return

    def set_cue_buttons(self, buttons):
        """ Sets the group of buttons to use for triggering cues with or
        (if shift pressed) without quantization. """
        self._cue_buttons = list(buttons) if buttons else []
        self._num_buttons = len(self._cue_buttons)
        self._on_cue_button_value.replace_subjects(self._cue_buttons)
        self.update()

    def set_shift_button(self, button):
        """ Sets the shift button that changes the functionality of other controls. """
        self._shift_button = button
        self._on_shift_button_value.subject = button

    def set_add_cue_button(self, button):
        """ Sets the button to use for adding or (if shift pressed) removing cues. """
        self._add_cue_button = button
        self._on_add_cue_button_value.subject = button
        self._update_add_cue_button()

    @subject_slot_group('value')
    def _on_cue_button_value(self, value, button):
        if self.is_enabled() and value:
            btn_index = self._cue_buttons.index(button)
            if btn_index < len(self._cues):
                cues = list(self.song().cue_points)
                cue_time = self._cue_times[btn_index]
                cue = None
                for c in cues:
                    if c.time == cue_time:
                        cue = c
                        break

                if cue:
                    if self._handle_extra_cue_button_function(button, cue_time):
                        return
                    self.component_message('Triggered Cue', cue.name, header_2=format_absolute_time(self.song(), cue.time))
                    if is_button_pressed(self._shift_button):
                        self.song().current_song_time = cue.time
                    else:
                        if self.song().is_playing and btn_index != self._current_cue_index:
                            self._update_cue_buttons()
                            button.set_light('CuePoint.Triggered')
                        else:
                            self._current_cue_index = -1
                        cue.jump()
        return

    def _handle_extra_cue_button_function(self, button, cue_time):
        """ Returns whether any extra functionality was performed. """
        return False

    @subject_slot('value')
    def _on_shift_button_value(self, _):
        self._update_add_cue_button()

    @subject_slot('value')
    def _on_add_cue_button_value(self, value):
        if value:
            has_cue = self.song().current_song_time in self._cue_times
            if is_button_pressed(self._shift_button):
                if not self.song().is_playing and has_cue:
                    for k, v in self._cues.iteritems():
                        if v['time'] == self.song().current_song_time:
                            self.component_message('Deleted Cue', k.name)
                            break

                    self.song().set_or_delete_cue()
            elif not has_cue:
                self.song().set_or_delete_cue()

    @subject_slot('cue_points')
    def _on_cue_added_or_removed(self):
        self._on_cue_time_changed.replace_subjects(self.song().cue_points)
        self._refresh_cues()

    @subject_slot_group('time')
    def _on_cue_time_changed(self, _):
        self._refresh_cues()

    def update(self):
        super(MatrixCueComponent, self).update()
        self._refresh_cues()

    def _refresh_cues(self):
        if self.is_enabled() and self._cues is not None:
            self._cue_times = []
            self._cue_times_reversed = []
            self._current_cue_index = -1
            self._remove_unneeded_cues()
            current_cues = self._cues.keys()
            for cue in self.song().cue_points:
                self._cue_times.append(cue.time)
                if cue in current_cues:
                    continue
                else:
                    self._cues[cue] = {'time': cue.time, 'snap': None}

            self._cue_times = sorted(self._cue_times)
            self._cue_times_reversed = list(reversed(self._cue_times))
            self._update_cue_buttons()
            self._on_song_time_changed()
        return

    @subject_slot('current_song_time')
    def _on_song_time_changed(self, skip_extra_functionality=False):
        if self.is_enabled():
            if self._cue_buttons and self._cue_times_reversed:
                current_time = self.song().current_song_time
                current_cue_time = -1
                for cue_time in self._cue_times_reversed:
                    if cue_time <= current_time:
                        current_cue_time = cue_time
                        break

                if current_cue_time > -1:
                    cue_index = self._cue_times.index(current_cue_time)
                    if cue_index != self._current_cue_index:
                        self._current_cue_index = cue_index
                        if cue_index < self._num_buttons:
                            if not skip_extra_functionality and self.song().is_playing:
                                self._cue_reached_method(current_cue_time)
                            self._update_cue_buttons()
                            button = self._cue_buttons[cue_index]
                            if button:
                                button.set_light('CuePoint.Selected')
                else:
                    self._clear_last_cue_button()
            if not self.song().is_playing:
                self._update_add_cue_button()

    @subject_slot('is_playing')
    def _on_playing_state_changed(self):
        """ This is needed for cases where a cue point is triggered and transport is
        stopped before the cue point is reached. """
        if self.is_enabled():
            self._current_cue_index = -1
            if not self.song().is_playing:
                self._update_cue_buttons()
                self._on_song_time_changed(True)
            self._update_add_cue_button()

    def _update_cue_buttons(self):
        if self.is_enabled() and self._cue_buttons:
            if self._cue_times:
                num_cues = len(self._cue_times)
                for index, button in enumerate(self._cue_buttons):
                    if button:
                        if index < num_cues:
                            self._update_cue_button(button, self._cue_times[index])
                        else:
                            button.set_light('DefaultButton.Off')

            else:
                set_group_button_lights(self._cue_buttons, 'DefaultButton.Off')

    def _update_cue_button(self, button, _):
        """ Updates the given button, which contains a cue. This can be overriden. """
        button.set_light('CuePoint.Present')

    def _update_add_cue_button(self):
        if self.is_enabled() and self._add_cue_button:
            has_cue = self.song().current_song_time in self._cue_times
            if is_button_pressed(self._shift_button):
                turn_on = not self.song().is_playing and has_cue
                self._add_cue_button.set_light('Global.CanDelete' if turn_on else 'Global.CannotDelete')
            else:
                turn_on = self.song().is_playing or not has_cue
                self._add_cue_button.set_light('Global.CanAdd' if turn_on else 'Global.CannotAdd')

    def _clear_last_cue_button(self):
        if self.is_enabled() and self._current_cue_index in xrange(self._num_buttons):
            button = self._cue_buttons[self._current_cue_index]
            if button:
                if self._current_cue_index < len(self._cue_times):
                    cue_time = self._cue_times[self._current_cue_index]
                    self._update_cue_button(button, cue_time)
                else:
                    button.set_light('DefaultButton.Off')

    def _remove_unneeded_cues(self):
        """ Removes non-existent cues and replaces cue references, which is needed since
        references of cues can change slightly in the API. """
        cues = list(self.song().cue_points)
        new_cues = {}
        for cue in self._cues.keys():
            if cue in cues:
                new_obj = self._find_cue_by_reference(cues, cue)
                if new_obj is not None:
                    current_settings = self._cues[cue]
                    new_cues[new_obj] = current_settings
                    new_cues[new_obj]['time'] = cue.time

        self._cues = new_cues
        return

    @staticmethod
    def _find_cue_by_reference(cues, cue_to_find):
        """ Returns the cue in cues that represents the given cue_to_find. This will
        always return a cue, the None is just for completeness. """
        for cue in cues:
            if cue == cue_to_find:
                return cue

        return


class MatrixCueSnapComponent(MatrixCueComponent):
    """ MatrixCueSnapComponent extends standard to allow cues to store/recall
    session snaps. """
    __subject_events__ = ('snap_data', )

    def __init__(self, name='Matrix_Cue_Snap_Control', *a, **k):
        self._store_button = None
        self._delete_button = None
        self._rebuild_data = None
        self._last_data = None
        super(MatrixCueSnapComponent, self).__init__(name=name, cue_reached_method=self._handle_cue_reached, *a, **k)
        return

    def disconnect(self):
        for cue in self._cues.values():
            if cue['snap']:
                cue['snap'].disconnect()

        super(MatrixCueSnapComponent, self).disconnect()
        self._rebuild_data = None
        self._last_data = None
        self._store_button = None
        self._delete_button = None
        return

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
        """ Rebuilds snap data based on the given data dict. """
        if self.is_enabled():
            self._last_data = None
            for k, v in data.iteritems():
                cue = self._find_cue_by_time(k)
                if cue:
                    snap = SessionSnap(self.song())
                    snap.rebuild(v)
                    cue['snap'] = snap

            self._update_cue_buttons()
            self._rebuild_data = None
        else:
            self._rebuild_data = data
        return

    @subject_slot('value')
    def _on_store_button_value(self, value):
        if self.is_enabled():
            self._store_button.set_light('Modifiers.Pressed' if value else 'Modifiers.Store')

    @subject_slot('value')
    def _on_delete_button_value(self, value):
        if self.is_enabled():
            if value:
                self._update_cue_buttons()
            else:
                self._current_cue_index = -1
                self._on_song_time_changed(True)
            self._delete_button.set_light('Modifiers.Pressed' if value else 'Modifiers.Delete')

    def _handle_extra_cue_button_function(self, button, cue_time):
        """ Handles storing or deleting snaps if possible. """
        cue = self._find_cue_by_time(cue_time)
        if cue:
            if is_button_pressed(self._store_button):
                if cue['snap'] is None:
                    cue['snap'] = SessionSnap(self.song())
                cue['snap'].store()
                self._update_cue_button(button, cue_time)
                self._notify_snap_data()
                return True
            if is_button_pressed(self._delete_button):
                cue['snap'] = None
                self._update_cue_button(button, cue_time)
                self._notify_snap_data()
                return True
        return False

    def _notify_snap_data(self):
        if self._cues is not None:
            data = {}
            for cue in self._cues.values():
                if cue['snap']:
                    data[cue['time']] = cue['snap'].data

            if self._last_data is None or self._last_data == data:
                self._last_data = data
                return
            self._last_data = data
            self.notify_snap_data(data)
        return

    def _handle_cue_reached(self, cue_time):
        """ Handles triggering the snap associated with the cue if there is one. """
        cue = self._find_cue_by_time(cue_time)
        if cue and cue['snap'] is not None:
            cue['snap'].recall()
        return

    def update(self):
        super(MatrixCueSnapComponent, self).update()
        self._update_store_and_delete_buttons()
        if self.is_enabled() and self._rebuild_data:
            self.rebuild(self._rebuild_data)

    def _refresh_cues(self):
        if self.is_enabled():
            super(MatrixCueSnapComponent, self)._refresh_cues()
        else:
            self._is_enabled = True
            super(MatrixCueSnapComponent, self)._refresh_cues()
            self._is_enabled = False
        if self.canonical_parent:
            self.canonical_parent.schedule_message(1, self._notify_snap_data)

    def _update_cue_button(self, button, cue_time):
        """ Overrides standard to indicate if button has an associated snap or if can
        delete snap. """
        if self.is_enabled():
            cue = self._find_cue_by_time(cue_time)
            if cue:
                if cue['snap'] is None:
                    button.set_light('CuePoint.Present')
                else:
                    button.set_light('Global.CanDelete' if is_button_pressed(self._delete_button) else 'Global.HasSnap')
        return

    def _update_store_and_delete_buttons(self):
        if self.is_enabled():
            if self._store_button:
                self._store_button.set_light('Modifiers.Store')
            if self._delete_button:
                self._delete_button.set_light('Modifiers.Delete')

    def _find_cue_by_time(self, cue_time):
        """ Returns the cue associated with the given cue time. """
        for cue in self._cues.values():
            if cue['time'] == cue_time:
                return cue

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/MatrixCueComponent.pyc
