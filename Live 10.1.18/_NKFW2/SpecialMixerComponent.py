# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialMixerComponent.py
# Compiled at: 2017-10-15 19:25:17
from functools import partial
from itertools import izip_longest
from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import release_control
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.Control import ButtonControl
from SpecialChannelStripComponent import SpecialChannelStripComponent
from ModifierMixin import ModifierMixin
from ShowMessageMixin import ShowMessageMixin
from consts import ASCII_A
from Utils import right_justify_track_components
justify_function = right_justify_track_components

class SpecialMixerComponent(MixerComponent, ModifierMixin, ShowMessageMixin):
    """ SpecialMixerComponent extends standard to add convenience methods for several
    features of the SpecialChannelStripComponent.  It also allows for easily including
    or excluding returns. And also provides an offset listener similar to the
    SessionComponent. """
    __subject_events__ = ('offset', 'send_index', 'tracks')
    send_toggle_button = ButtonControl()

    def __init__(self, num_tracks, include_returns=True, alt_select_arms=True, targets_comp=None, right_just_returns=True, handle_modifier_leds=True, limit_send_index=True, display_send_index=False, use_0_db_volume=False, *a, **k):
        self._width = num_tracks
        self._include_returns = bool(include_returns)
        self._right_justify_returns = bool(right_just_returns)
        self._alt_select_arms = bool(alt_select_arms)
        self._limit_send_index = bool(limit_send_index)
        self._display_send_index = bool(display_send_index)
        self._use_0_db_volume = bool(use_0_db_volume)
        self._cue_volume_control = None
        self._has_targets_comp = targets_comp is not None
        self._send_select_buttons = None
        self._send_index = 0
        self._is_return_mixer = num_tracks == 0
        super(SpecialMixerComponent, self).__init__(num_tracks, auto_name=True, invert_mute_feedback=True, handle_modifier_leds=handle_modifier_leds, *a, **k)
        self.name = 'Mixer_Control'
        self._on_target_track_changed.subject = targets_comp
        if self._is_return_mixer:
            self._channel_strips = self._return_strips
        self._empty_send_controls = [ None for _ in xrange(len(self._channel_strips)) ]
        return

    def disconnect(self):
        release_control(self._cue_volume_control)
        super(SpecialMixerComponent, self).disconnect()
        self._cue_volume_control = None
        self._send_select_buttons = None
        return

    @property
    def is_return_mixer(self):
        """ Returns whether this is a returns-only mixer. """
        return self._is_return_mixer

    def track_offset(self):
        """ Added for proper slave/link handling. """
        return self._track_offset

    @staticmethod
    def scene_offset():
        """ Added for proper slave/link handling. """
        return 0

    def width(self):
        """ Added for proper slave/link handling. """
        return self._width

    @staticmethod
    def height():
        """ Added for proper slave/link handling. """
        return 0

    def set_offsets(self, track_offset, _):
        """ Added for proper slave/link handling. """
        self.set_track_offset(track_offset)

    def channel_strips(self):
        """ Returns all of this component's channel strips. """
        return self._channel_strips

    def set_physical_display_element(self, element):
        """ Extends standard to set display element of channel strips. """
        super(SpecialMixerComponent, self).set_physical_display_element(element)
        for strip in self._channel_strips or []:
            strip.set_physical_display_element(element)

    def set_send_select_buttons(self, buttons):
        """ Sets the buttons to use for directly selecting the send index to use. """
        self._send_select_buttons = list(buttons) if buttons else []
        self._on_send_select_button_value.replace_subjects(self._send_select_buttons)
        self._update_send_select_buttons()

    def set_alt_mute_buttons(self, buttons):
        """ Set buttons to use for momentary/toggle muting. """
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.alt_mute_button.set_control_element(button)

    def set_alt_solo_buttons(self, buttons):
        """ Set buttons to use for momentary/toggle soloing. """
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.alt_solo_button.set_control_element(button)

    def set_alt_select_buttons(self, buttons):
        """ Sets buttons to use for multi-function (delete, duplicate, fold, arm,
        show playing clip) select. """
        for strip, button in izip_longest(self._channel_strips, buttons or []):
            strip.alt_select_button.set_control_element(button)

    def __getattribute__(self, name):
        """ Extends standard to set send controls by index (like send_index_00_controls)
        to make it easier to assign controls to sends without dealing with the base
        class's send index. """
        if name.startswith('set_send_index_'):
            send_index = int(name[15:17])
            return partial(self._set_send_controls, send_index)
        return object.__getattribute__(self, name)

    def _set_send_controls(self, send_index, controls):
        """ Sets send controls for the given send_index. """
        controls = list(controls) if controls else self._empty_send_controls
        for index, strip in enumerate(self._channel_strips):
            strip.set_indexed_send_control(controls[index], send_index)

    def set_master_volume_control(self, control):
        """ Convenience method for setting master volume control in a layer. """
        self.master_strip().set_volume_control(control)

    def set_master_select_button(self, button):
        """ Convenience method for setting master select button in a layer. """
        self.master_strip().set_select_button(button)

    def set_cue_volume_control(self, control):
        """ Sets the control to use for controlling cue volume. """
        if control != self._cue_volume_control:
            release_control(self._cue_volume_control)
            self._cue_volume_control = control
            self._update_cue_volume_connection()

    def set_unmute_all_button(self, button):
        """ Sets the button to use for unmuting all tracks. """
        self._on_unmute_all_button_value.subject = button
        self._update_unall_buttons()

    def set_unsolo_all_button(self, button):
        """ Sets the button to use for unsoloing all tracks. """
        self._on_unsolo_all_button_value.subject = button
        self._update_unall_buttons()

    def set_unarm_all_button(self, button):
        """ Sets the button to use for unarming all tracks. """
        self._on_unarm_all_button_value.subject = button
        self._update_unall_buttons()

    def set_bank_down_button(self, button):
        """ Sets the button to use for banking down. This is added so bank buttons can
        be used in layers. """
        self.set_bank_buttons(self._bank_up_button, button)

    def set_bank_up_button(self, button):
        """ Sets the button to use for banking up. This is added so bank buttons can
        be used in layers. """
        self.set_bank_buttons(button, self._bank_down_button)

    def set_track_offset(self, new_offset):
        """ Extends standard to notify offset listeners. """
        super(SpecialMixerComponent, self).set_track_offset(new_offset)
        self.notify_offset()

    def set_shift_button(self, button):
        """ Overrides standard to use ModifierMixin's methods. """
        self._set_modifier(button, 'shift')

    def _set_modifier(self, button, modifier_name):
        """ Extends standard to set up modifiers for sub-components. """
        for strip in self._channel_strips or []:
            getattr(strip, 'set_%s_button' % modifier_name)(button)

        super(SpecialMixerComponent, self)._set_modifier(button, modifier_name)

    @send_toggle_button.pressed
    def send_toggle_button(self, _):
        if self.num_sends:
            self.send_index = (self.send_index + 1) % self.num_sends

    @subject_slot_group('value')
    def _on_send_select_button_value(self, value, button):
        if value:
            index = self._send_select_buttons.index(button)
            if index < self.num_sends:
                self.send_index = index

    def _get_send_index(self):
        """ Same as standard, needed to properly override. """
        return self._send_index

    def _set_send_index(self, index):
        """ Overrides standard to allow index to be greater than num_sends if flag set
        by init. """
        if index is None or 0 <= index and (index < self.num_sends or not self._limit_send_index):
            if self._send_index != index:
                self._send_index = index
                self.notify_send_index()
                self.set_send_controls(self._send_controls)
                self.on_send_index_changed()
        else:
            raise IndexError
        return

    send_index = property(_get_send_index, _set_send_index)

    def on_send_index_changed(self, force=False):
        """ Displays the send being controlled if elected. """
        if self._display_send_index and (self._send_controls or force):
            self.component_message('Controlling Send', chr(ASCII_A + self.send_index))
        self._update_send_select_buttons()

    def on_num_sends_changed(self):
        self._update_send_select_buttons()

    @subject_slot('value')
    def _on_unmute_all_button_value(self, value):
        if self.is_enabled():
            if value:
                tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
                for track in tracks:
                    track.mute = False

            button = self._on_unmute_all_button_value.subject
            button.set_light('Track.NotMuted' if value else 'Track.Muted')

    @subject_slot('value')
    def _on_unsolo_all_button_value(self, value):
        if self.is_enabled():
            if value:
                tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
                for track in tracks:
                    track.solo = False

            button = self._on_unsolo_all_button_value.subject
            button.set_light('Track.Soloed' if value else 'Track.NotSoloed')

    @subject_slot('value')
    def _on_unarm_all_button_value(self, value):
        if self.is_enabled():
            if value:
                tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks)
                for track in tracks:
                    if track.can_be_armed:
                        track.arm = False

            button = self._on_unarm_all_button_value.subject
            button.set_light('Track.Armed' if value else 'Track.NotArmed')

    def update(self):
        super(SpecialMixerComponent, self).update()
        self.update_modifier_leds()
        self._update_send_select_buttons()
        self._update_bank_buttons()
        self._update_unall_buttons()
        self._update_cue_volume_connection()

    def _reassign_tracks(self):
        """ Extended standard to right justify returns if elected, properly update
        bank buttons and notify. """
        if self._right_justify_returns:
            justify_function(self.song(), self.tracks_to_use(), self._track_offset, self._channel_strips)
        else:
            if self._is_return_mixer:
                self._track_offset = 1 if len(self.song().return_tracks) == 0 else 0
            super(SpecialMixerComponent, self)._reassign_tracks()
        self._update_bank_buttons()
        self.notify_tracks()

    def _update_cue_volume_connection(self):
        release_control(self._cue_volume_control)
        if self.is_enabled() and self._cue_volume_control:
            control = self._cue_volume_control
            control.connect_to(self.song().master_track.mixer_device.cue_volume)

    def _update_send_select_buttons(self):
        if self.is_enabled() and self._send_select_buttons:
            for i, button in enumerate(self._send_select_buttons):
                if button:
                    if i < self.num_sends:
                        button.set_light('Sends.Selected%s' % i if i == self.send_index else 'Sends.NotSelected%s' % i)
                    else:
                        button.set_light('DefaultButton.Off')

    def _update_bank_buttons(self):
        if self.is_enabled():
            colors = ('Navigation.SessionEnabled', 'Navigation.Disabled')
            if self._bank_up_button:
                tracks = self.tracks_to_use()
                num_strips = len(self._channel_strips)
                turn_on = len(tracks) > self._track_offset + num_strips
                self._bank_up_button.set_light(colors[0] if turn_on else colors[1])
            if self._bank_down_button:
                self._bank_down_button.set_light(colors[0] if self._track_offset > 0 else colors[1])

    def _update_unall_buttons(self):
        if self.is_enabled():
            mute = self._on_unmute_all_button_value.subject
            if mute:
                mute.set_light('Track.Muted')
            solo = self._on_unsolo_all_button_value.subject
            if solo:
                solo.set_light('Track.NotSoloed')
            arm = self._on_unarm_all_button_value.subject
            if arm:
                arm.set_light('Track.NotArmed')

    @subject_slot('target_track')
    def _on_target_track_changed(self, track):
        if self._selected_strip is not None:
            self._selected_strip.set_track(track)
        return

    def on_selected_track_changed(self):
        """ Overrides standard to not set track of selected strip if has a
        TargetsComponent. """
        if self._has_targets_comp:
            return
        super(SpecialMixerComponent, self).on_selected_track_changed()

    def tracks_to_use(self):
        """ Overrides standard so that returns will be included in tracks to control if
        specified or only returns will be returned if specified. """
        if self._is_return_mixer:
            return self.song().return_tracks
        if self._include_returns:
            return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)
        return self.song().visible_tracks

    def _create_strip(self):
        """ Overrides standard to return specialized version. """
        return SpecialChannelStripComponent(self._alt_select_arms, use_0_db_volume=self._use_0_db_volume)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialMixerComponent.pyc
