# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialChannelStripComponent.py
# Compiled at: 2017-10-15 19:14:32
from _Framework.ChannelStripComponent import ChannelStripComponent, chain, release_control, nop
from _Framework.SubjectSlot import subject_slot
from ShowMessageMixin import ShowMessageMixin
from SpecialControl import SpecialButtonControl
from PropertyControl import ParameterControl
from ControlUtils import is_button_pressed
from Utils import delete_track, duplicate_track, live_object_is_valid
from consts import ZERO_DB_VALUE, PARAM_REL_STEP

class SpecialChannelStripComponent(ChannelStripComponent, ShowMessageMixin):
    """ SpecialChannelStripComponent extends standard to add skin handling for all used
    buttons, mty/tgl mute, more modifiers, multi-function select, special send
    handling and support for 0db volume control. """
    __subject_events__ = ('track_name', )
    alt_mute_button = SpecialButtonControl(color='Track.NotMuted', on_color='Track.Muted', disabled_color='Track.Empty')
    alt_solo_button = SpecialButtonControl(color='Track.NotSoloed', on_color='Track.Soloed', disabled_color='Track.Empty')
    alt_select_button = SpecialButtonControl(color='Track.NotSelected', on_color='Track.Selected', disabled_color='Track.Empty')

    def __init__(self, alt_select_arms=True, use_0_db_volume=False, *a, **k):
        self._alt_select_should_arm = bool(alt_select_arms)
        self._use_0_db_volume = bool(use_0_db_volume)
        self._delete_button = None
        self._duplicate_button = None
        super(SpecialChannelStripComponent, self).__init__(*a, **k)
        self._indexed_send_controls = [ None for _ in xrange(12) ]
        self._0_db_volume_property = ParameterControl('volume', None, (
         0.0, ZERO_DB_VALUE), default_value=ZERO_DB_VALUE, rel_thresh=0, rel_step=PARAM_REL_STEP, quantized=False)
        sel_track = self.song().view.selected_track
        self._last_selected_track = sel_track if sel_track != self.song().master_track else self.song().tracks[0]
        self._track_was_selected = False
        return

    def disconnect(self):
        self._0_db_volume_property.disconnect()
        super(SpecialChannelStripComponent, self).disconnect()
        self._delete_button = None
        self._duplicate_button = None
        self._indexed_send_controls = None
        self._last_selected_track = None
        return

    @property
    def is_selected(self):
        """ Returns whether the controlled track is selected. """
        return live_object_is_valid(self._track) and self._track == self.song().view.selected_track

    def set_track(self, track):
        """ Extends standard to set parent of 0db property. """
        super(SpecialChannelStripComponent, self).set_track(track)
        self._0_db_volume_property.set_parent(track.mixer_device.volume if live_object_is_valid(track) else None)
        return

    def set_volume_control(self, control):
        """ Extends standard to use 0db volume if specified. """
        if self._use_0_db_volume:
            self._0_db_volume_property.set_control(control)
        else:
            super(SpecialChannelStripComponent, self).set_volume_control(control)

    def set_indexed_send_control(self, control, index):
        """ Set the send controls of this strip by index. """
        if self._indexed_send_controls and index < len(self._indexed_send_controls):
            release_control(self._indexed_send_controls[index])
            self._indexed_send_controls[index] = control
            self.update()

    def set_delete_button(self, button):
        """ Sets the button to use for modifying the function of alt_select to delete
        the track. """
        self._delete_button = button

    def set_duplicate_button(self, button):
        """ Sets the button to use for modifying the function of alt_select to duplicate
        the track. """
        self._duplicate_button = button

    @alt_mute_button.pressed
    def alt_mute_button(self, _):
        self._toggle_mute()

    @alt_mute_button.released_delayed
    def alt_mute_button(self, _):
        self._toggle_mute(True)

    @alt_mute_button.pressed_delayed
    def alt_mute_button(self, _):
        pass

    @alt_mute_button.released_immediately
    def alt_mute_button(self, _):
        pass

    def _toggle_mute(self, is_release=False):
        if self.is_enabled() and live_object_is_valid(self._track):
            if self._track != self.song().master_track:
                if not is_release or self._track.mute:
                    self._track.mute = not self._track.mute

    @alt_solo_button.pressed
    def alt_solo_button(self, _):
        self._toggle_solo()

    @alt_solo_button.released_delayed
    def alt_solo_button(self, _):
        self._toggle_solo(True)

    @alt_solo_button.pressed_delayed
    def alt_solo_button(self, _):
        pass

    @alt_solo_button.released_immediately
    def alt_solo_button(self, _):
        pass

    def _toggle_solo(self, is_release=False):
        if self.is_enabled() and live_object_is_valid(self._track):
            if self._track != self.song().master_track:
                if not is_release or self._track.solo:
                    exclusive = self.song().exclusive_solo != is_button_pressed(self._shift_button)
                    if exclusive:
                        for track in chain(self.song().tracks, self.song().return_tracks):
                            if track != self._track:
                                track.solo = False

                    self._track.solo = not self._track.solo

    @alt_select_button.pressed
    def alt_select_button(self, _):
        """ Handles delete, duplicating or plain selecting with optional playing clip
        selection. """
        if self.is_enabled() and live_object_is_valid(self._track):
            t = self._track
            if is_button_pressed(self._delete_button):
                delete_track(self.song(), t, self.component_message)
            elif is_button_pressed(self._duplicate_button):
                duplicate_track(self.song(), t, self.component_message)
            else:
                reg_track = t in self.song().tracks
                select_track = self.song().view.selected_track != t
                select_clip = reg_track and is_button_pressed(self._shift_button)
                self._track_was_selected = not (select_track or select_clip)
                if not self._track_was_selected:
                    self.song().view.selected_track = t
                    if select_clip and t.is_visible and t.playing_slot_index >= 0:
                        self._song.view.highlighted_clip_slot = list(t.clip_slots)[t.playing_slot_index]

    @alt_select_button.released_immediately
    def alt_select_button(self, _):
        """ Handles toggling the arm state of the track if it was already selected. """
        if self.is_enabled() and self.is_selected and self._track_was_selected:
            if self._alt_select_should_arm and self._track.can_be_armed:
                exclusive = self.song().exclusive_arm
                if exclusive:
                    for track in self.song().tracks:
                        if track != self._track and track.can_be_armed:
                            track.arm = False

                self._track.arm = not self._track.arm

    @alt_select_button.pressed_delayed
    def alt_select_button(self, _):
        """ Handles toggling the fold state of the track if the button is held. """
        if self.is_enabled() and self.is_selected:
            if self._track.is_foldable:
                self._track.fold_state = not self._track.fold_state
            elif self._track.can_show_chains:
                self._track.is_showing_chains = not self._track.is_showing_chains

    @alt_select_button.released_delayed
    def alt_select_button(self, _):
        pass

    def _select_value(self, value):
        """ Overrides standard to handle reselecting last selected track for master
        track selection. """
        if self.is_enabled() and live_object_is_valid(self._track) and value:
            if self._track == self.song().master_track:
                if self.song().view.selected_track == self._track:
                    self.song().view.selected_track = self._last_selected_track
                    return
            self.song().view.selected_track = self._track

    def _connect_parameters(self):
        """ Extends standard to connect/release indexed send controls. """
        super(SpecialChannelStripComponent, self)._connect_parameters()
        if self._indexed_send_controls:
            for index, send_control in enumerate(self._indexed_send_controls):
                if send_control:
                    if index < len(self._track.mixer_device.sends):
                        send_control.connect_to(self._track.mixer_device.sends[index])
                    else:
                        send_control.release_parameter()
                        self._empty_control_slots.register_slot(send_control, nop, 'value')

    def _all_controls(self):
        """ Extends standard to include indexed send controls. """
        return [
         self._pan_control, self._volume_control] + list(self._send_controls or []) + list(self._indexed_send_controls or [])

    def update(self):
        """ Extends standard to set enabled state of ButtonControls, update 0db
        property and set up implicit listener. """
        super(SpecialChannelStripComponent, self).update()
        can_mute_or_solo = live_object_is_valid(self._track) and self._track != self.song().master_track
        self.alt_mute_button.enabled = can_mute_or_solo
        self.alt_solo_button.enabled = can_mute_or_solo
        self.alt_select_button.enabled = live_object_is_valid(self._track)
        self._on_implicit_arm_changed.subject = self._track
        if self.is_enabled():
            self._0_db_volume_property.update()
            self._on_arm_changed()

    def _on_mute_changed(self):
        """ Overrides standard to update alt_mute_button and allow for skinning. """
        if self.is_enabled():
            has_track = live_object_is_valid(self._track) and self._track != self.song().master_track
            if has_track:
                self.alt_mute_button.is_on = self._track.mute
            if self._mute_button is not None:
                if has_track:
                    self._mute_button.set_light('Track.Muted' if self._track.mute else 'Track.NotMuted')
                else:
                    self._mute_button.set_light('Track.Empty')
        return

    def _on_solo_changed(self):
        """ Overrides standard to update alt_solo_button and allow for skinning. """
        if self.is_enabled():
            has_track = live_object_is_valid(self._track) and self._track != self.song().master_track
            if has_track:
                self.alt_solo_button.is_on = self._track.solo
            if self._solo_button is not None:
                if has_track:
                    self._solo_button.set_light('Track.Soloed' if self._track.solo else 'Track.NotSoloed')
                else:
                    self._solo_button.set_light('Track.Empty')
        return

    @subject_slot('implicit_arm')
    def _on_implicit_arm_changed(self):
        self._on_arm_changed()

    def _on_arm_changed(self):
        """ Overrides standard to allow for skinning, implicit arm handling and update
        alt_select. """
        self._update_alt_select_button()
        if self.is_enabled() and self._arm_button is not None:
            if live_object_is_valid(self._track) and self._track in self.song().tracks and self._track.can_be_armed:
                is_armed = self._track.arm or self._track.implicit_arm
                self._arm_button.set_light('Track.Armed' if is_armed else 'Track.NotArmed')
            else:
                self._arm_button.set_light('Track.Empty')
        return

    def on_selected_track_changed(self):
        """ Overrides standard to allow for skinning, update alt_select and track name
        and store last selected track. """
        self._update_alt_select_button()
        self._update_track_name_data_source()
        if self.is_enabled():
            if self._select_button is not None:
                if live_object_is_valid(self._track):
                    self._select_button.set_light('Track.Selected' if self._track == self.song().view.selected_track else 'Track.NotSelected')
                else:
                    self._select_button.set_light('Track.Empty')
        if self.song().view.selected_track != self.song().master_track:
            self._last_selected_track = self.song().view.selected_track
        return

    def _update_alt_select_button(self):
        """ Updates alt_select on arm and select changes. """
        if self.is_enabled():
            value = 'Track.Empty'
            if live_object_is_valid(self._track):
                t = self._track
                value = 'Track.NotSelected'
                is_selected = t and t == self.song().view.selected_track
                is_armed = self._alt_select_should_arm and t.can_be_armed and (t.arm or t.implicit_arm)
                if is_selected and is_armed:
                    value = 'Track.SelectedAndArmed'
                elif is_selected:
                    value = 'Track.Selected'
                elif is_armed:
                    value = 'Track.NotSelectedAndArmed'
            self.alt_select_button.color = value

    def update_track_name_data_source(self):
        """ Non-private method for notifying subjects of track name. """
        self._update_track_name_data_source()

    def _update_track_name_data_source(self):
        """ Extends standard to notify track name subjects. """
        if self.track_name_data_source():
            super(SpecialChannelStripComponent, self)._update_track_name_data_source()
        self.notify_track_name(self._track.name if live_object_is_valid(self._track) else '', self.is_selected)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialChannelStripComponent.pyc
