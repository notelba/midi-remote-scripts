# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TargetsComponent.py
# Compiled at: 2017-03-07 13:28:53
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.Util import find_if, nop
from ShowMessageMixin import ShowMessageMixin
from SpecialControl import SpecialButtonControl

class TargetTrackComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ TargetTrackComponent handles determining the track that other components should
    control and provides locking capabilities. """
    __subject_events__ = ('target_track', 'toggle_lock_to_item')
    _target_track = None
    lock_button = SpecialButtonControl(color='Global.LockOff', on_color='Global.LockOn', disabled_color='DefaultButton.Off')

    def __init__(self, name='Targets_Component', track_change_method=nop, is_private=True, *a, **k):
        super(TargetTrackComponent, self).__init__(name=name, *a, **k)
        self.is_private = bool(is_private)
        self._is_locked = False
        self._track_change_method = track_change_method
        self.on_selected_track_changed()

    @property
    def target_track(self):
        """ The track to control. """
        return self._target_track

    @lock_button.released_immediately
    def lock_button(self, _):
        """ Short press toggles lock status. """
        self.toggle_lock()

    @lock_button.pressed_delayed
    def lock_button(self, _):
        """ Long press notifies subjects to toggle their locks and also toggles LED
        for visual feedback. """
        self.lock_button.is_on = not self.lock_button.is_on
        self.toggle_mode_specific_lock()

    @lock_button.pressed
    def lock_button(self, _):
        """ Unused, but needed when using pressed_delayed. """
        pass

    @lock_button.released_delayed
    def lock_button(self, _):
        """ Resets LED state after change made by press_delayed. """
        self._update_lock_button()

    def set_lock(self, state):
        """ Sets locked state and updates. """
        if state == self._is_locked:
            return
        self._show_lock_info(state)
        self._is_locked = state
        self.on_selected_track_changed()
        self._update_lock_button()

    def toggle_lock(self):
        """ Toggles lock state. """
        self.set_lock(not self._is_locked)

    def toggle_mode_specific_lock(self):
        """ Toggle mode specific locks. """
        self.notify_toggle_lock_to_item()

    def update(self):
        """ Call to update all targets. """
        super(TargetTrackComponent, self).update()
        self.on_selected_track_changed()

    def on_selected_track_changed(self):
        """ Sets the track to control if not locked. """
        if self._is_locked and self._target_track:
            pass
        else:
            if self._is_locked:
                self._show_lock_info(False)
            self._is_locked = False
            self._target_track = self.song().view.selected_track
            self._track_change_method()
            self.notify_target_track(self._target_track)
        self._update_lock_button()

    def _show_lock_info(self, intend_to_lock):
        """ Shows lock status info in status bar. """
        if intend_to_lock:
            self.component_message('Locked To Track', self.song().view.selected_track.name)
        else:
            self.component_message('Unlocked From Track')

    def _update_lock_button(self):
        if self.is_enabled():
            self.lock_button.is_on = self._is_locked


class TargetTrackAndClipComponent(TargetTrackComponent):
    """ TargetTrackAndClipComponent extends TargetTrackComponent to also handle
    a clip. """
    __subject_events__ = ('target_clip', )
    _target_clip = None

    def __init__(self, *a, **k):
        super(TargetTrackAndClipComponent, self).__init__(track_change_method=self._on_track_changed, *a, **k)

    @property
    def target_clip(self):
        """ The clip to control """
        return self._target_clip

    def _on_track_changed(self):
        self.on_selected_scene_changed()

    def on_selected_scene_changed(self):
        """ Sets the clip on the target_track to control. """
        clip = None
        self._on_selected_clip_slot_has_clip_changed.subject = None
        if self._target_track in self.song().tracks:
            slot_index = list(self.song().scenes).index(self.song().view.selected_scene)
            clip_slot = self._target_track.clip_slots[slot_index]
            if clip_slot.has_clip:
                clip = clip_slot.clip
            self._on_selected_clip_slot_has_clip_changed.subject = clip_slot
        if self._target_clip is not clip:
            self._target_clip = clip
            self.notify_target_clip(self._target_clip)
        return

    @subject_slot('has_clip')
    def _on_selected_clip_slot_has_clip_changed(self):
        self.on_selected_scene_changed()


class TargetsComponent(TargetTrackAndClipComponent):
    """ TargetsComponent extends TargetTrackAndClipComponent to also handle
    a Drum Rack, Simpler and plugin. """
    __subject_events__ = ('target_drum_rack', 'target_simpler', 'target_plugin')
    _target_drum_rack = None
    _target_simpler = None
    _target_plugin = None

    @property
    def target_drum_rack(self):
        """ The Drum Rack to control. """
        return self._target_drum_rack

    @property
    def target_simpler(self):
        """ The Simpler instance to control. """
        return self._target_simpler

    @property
    def target_plugin(self):
        """ The plugin instance to control. """
        return self._target_plugin

    def _on_track_changed(self):
        super(TargetsComponent, self)._on_track_changed()
        self._on_devices_changed.subject = self._target_track
        self._on_devices_changed()

    @subject_slot('devices')
    def _on_devices_changed(self):
        """ Sets the Drum Rack and Simpler on the target_track to control. """
        self._on_chains_changed.subject = None
        self._on_chain_devices_changed.replace_subjects([])
        drum_rack = self._find_drum_rack()
        simpler = self._find_simpler()
        plugin = self._find_plugin()
        if drum_rack is None or simpler is None or plugin is None:
            instrument_rack = self._find_instrument_rack()
            if instrument_rack:
                self._on_chains_changed.subject = instrument_rack
                self._on_chain_devices_changed.replace_subjects([ c for c in instrument_rack.chains
                                                                ])
                if drum_rack is None:
                    drum_rack = self._find_nested_drum_rack(instrument_rack)
                if simpler is None:
                    simpler = self._find_nested_simpler(instrument_rack)
                if plugin is None:
                    plugin = self._find_nested_plugin(instrument_rack)
        notify_drum_rack = False
        notify_simpler = False
        if self._target_drum_rack is not drum_rack:
            self._target_drum_rack = drum_rack
            notify_drum_rack = True
        if self._target_simpler is not simpler:
            self._target_simpler = simpler
            notify_simpler = True
        if notify_drum_rack:
            self.notify_target_drum_rack(self._target_drum_rack)
        if notify_simpler:
            self.notify_target_simpler(self._target_simpler)
        if self._target_plugin is not plugin:
            self._target_plugin = plugin
            self.notify_target_plugin(self._target_plugin)
        return

    @subject_slot('chains')
    def _on_chains_changed(self):
        self._on_devices_changed()

    @subject_slot_group('devices')
    def _on_chain_devices_changed(self, _):
        self._on_devices_changed()

    def _find_drum_rack(self):
        """ Returns a top-level Drum Rack or None. """
        return find_if(lambda d: d.type == Live.Device.DeviceType.instrument and d.can_have_drum_pads, self._target_track.devices)

    def _find_simpler(self):
        """ Returns a top-level Simpler or None. """
        return find_if(lambda d: d.type == Live.Device.DeviceType.instrument and isinstance(d, Live.SimplerDevice.SimplerDevice), self._target_track.devices)

    def _find_plugin(self):
        """ Returns a top-level plugin or None. """
        return find_if(lambda d: isinstance(d, Live.PluginDevice.PluginDevice), self._target_track.devices)

    def _find_instrument_rack(self):
        """ Returns a top-level Instrument Rack or None. """
        return find_if(lambda d: d.type == Live.Device.DeviceType.instrument and d.can_have_chains, self._target_track.devices)

    @staticmethod
    def _find_nested_drum_rack(ins_rack):
        """ Returns a nested Drum Rack or None. """
        for chain in ins_rack.chains:
            for nested_device in chain.devices:
                if nested_device:
                    if nested_device.can_have_drum_pads:
                        return nested_device

        return

    @staticmethod
    def _find_nested_simpler(ins_rack):
        """ Returns a nested Simpler or None. """
        for chain in ins_rack.chains:
            for nested_device in chain.devices:
                if nested_device:
                    if isinstance(nested_device, Live.SimplerDevice.SimplerDevice):
                        return nested_device

        return

    @staticmethod
    def _find_nested_plugin(ins_rack):
        """ Returns a nested plugin or None. """
        for chain in ins_rack.chains:
            for nested_device in chain.devices:
                if nested_device:
                    if isinstance(nested_device, Live.PluginDevice.PluginDevice):
                        return nested_device

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TargetsComponent.pyc
