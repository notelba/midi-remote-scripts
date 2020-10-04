# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\HazMapChainComponent.py
# Compiled at: 2017-09-30 15:26:22
import Live
from HazMapTrackComponent import HazMapTrackComponent, subject_slot
from TrackDeviceManager import CHAIN_PARAM_DICT
from SpecialControl import SpecialButtonControl
from Utils import get_nested_device_parameter, get_mixer_parameter, get_device_instance_name, num_chains, selected_chain_index, increment_selected_chain
TRANSLATED_RACK_NAMES = {'DrumGroupDevice': 'Drum Rack', 'InstrumentGroupDevice': 'Instrument Rack', 
   'AudioEffectGroupDevice': 'Audio Effect Rack', 
   'MidiEffectGroupDevice': 'MIDI Effect Rack'}

def get_chain_based_path(path):
    """ Returns a formatted path for a chain-based mapping for use with
TrackDeviceManager. """
    p_slice = path[-4:]
    if p_slice[2][0] == 'chain_mixer':
        param_info = (
         p_slice[3][0],
         CHAIN_PARAM_DICT.get(p_slice[3][1], p_slice[3][1]))
        return {'rack': p_slice[0][1].class_name, 'mixer': True, 
           'device_class_name': None, 
           'device_instance_name': None, 
           'parameter': param_info}
    else:
        return {'rack': p_slice[0][1].class_name, 'mixer': False, 
           'device_class_name': p_slice[2][1].class_name, 
           'device_instance_name': get_device_instance_name(p_slice[2][1], False), 
           'parameter': p_slice[3][1]}


class HazMapChainComponent(HazMapTrackComponent):
    """ HazMapChainComponent is a specialized HazMapTrackComponent that assigns controls
    to parameters on the selected chain of a rack. It also includes buttons for muting,
    soloing and showing devices of the selected chain as well as navigating between
    chains. """
    __subject_events__ = ('current_rack', )
    mute_button = SpecialButtonControl(color='Track.NotMuted', on_color='Track.Muted', disabled_color='Chain.Empty')
    solo_button = SpecialButtonControl(color='Track.NotSoloed', on_color='Track.Soloed', disabled_color='Chain.Empty')
    prev_chain_button = SpecialButtonControl(color='Chain.CannotSelectChain', on_color='Chain.CanSelectChain', disabled_color='Chain.Empty')
    next_chain_button = SpecialButtonControl(color='Chain.CannotSelectChain', on_color='Chain.CanSelectChain', disabled_color='Chain.Empty')
    show_chain_button = SpecialButtonControl(color='Chain.DevicesNotVisible', on_color='Chain.DevicesVisible', disabled_color='Chain.Empty')

    def __init__(self, *a, **k):
        n = k.pop('name', 'HazMap_Chain_Control')
        super(HazMapChainComponent, self).__init__(*a, **k)
        self.name = n
        self._rack_class = None
        self._current_rack = None
        self._current_chain = None
        self.set_mapping_predicate(self._chain_mapping_predicate)
        self.set_path_resolver(get_chain_based_path)
        self.set_path_name_resolver(self._get_chain_based_path_name)
        self.set_get_parameter_method(self._get_assigned_chain_parameter)
        self.set_on_update_connections_method(self._on_update_connections)
        self.set_on_delete_assignments_method(self._on_delete_assignments)
        return

    def disconnect(self):
        super(HazMapChainComponent, self).disconnect()
        self._rack_class = None
        self._current_rack = None
        self._current_chain = None
        return

    @property
    def current_rack(self):
        """ Returns the rack currently being controlled or None. """
        return self._current_rack

    @show_chain_button.pressed
    def show_chain_button(self, _):
        if self._current_rack:
            self._current_rack.view.is_showing_chain_devices = not self._current_rack.view.is_showing_chain_devices

    @mute_button.pressed
    def mute_button(self, _):
        self._toggle_mute()

    @mute_button.released_delayed
    def mute_button(self, _):
        self._toggle_mute(True)

    @mute_button.pressed_delayed
    def mute_button(self, _):
        pass

    @mute_button.released_immediately
    def mute_button(self, _):
        pass

    def _toggle_mute(self, is_release=False):
        if self.is_enabled() and self._current_chain:
            if not is_release or self._current_chain.mute:
                self._current_chain.mute = not self._current_chain.mute

    @solo_button.pressed
    def solo_button(self, _):
        self._toggle_solo()

    @solo_button.released_delayed
    def solo_button(self, _):
        self._toggle_solo(True)

    @solo_button.pressed_delayed
    def solo_button(self, _):
        pass

    @solo_button.released_immediately
    def solo_button(self, _):
        pass

    def _toggle_solo(self, is_release=False):
        if self.is_enabled() and self._current_chain:
            if not is_release or self._current_chain.solo:
                self._current_chain.solo = not self._current_chain.solo

    @prev_chain_button.pressed
    def prev_chain_button(self, _):
        self._increment_selected_chain(-1)

    @next_chain_button.pressed
    def next_chain_button(self, _):
        self._increment_selected_chain(1)

    def _increment_selected_chain(self, factor):
        if self.is_enabled() and self._current_rack:
            increment_selected_chain(self._current_rack, factor, show_msg=self.component_message)

    def _on_update_connections(self):
        self._current_rack = None
        self._current_chain = None
        if self._rack_class is None:
            for a in self._assignments:
                if a:
                    self._rack_class = a['rack']
                    break

        if self._rack_class:
            self._current_rack = self._manager.get_device_by_class_name(self._rack_class)
            if self._current_rack:
                self._current_chain = self._current_rack.view.selected_chain
        self._on_mute_changed.subject = self._current_chain
        self._on_solo_changed.subject = self._current_chain
        r_view = self._current_rack.view if self._current_rack else None
        self._on_device_visibility_changed.subject = r_view
        self._on_selected_chain_changed.subject = r_view
        self._on_mute_changed()
        self._on_solo_changed()
        self._on_device_visibility_changed()
        self._update_chain_navigation_buttons()
        self.notify_current_rack()
        return

    def _on_delete_assignments(self):
        self._rack_class = None
        self._current_rack = None
        self._current_chain = None
        self._on_selected_chain_changed.subject = None
        return

    @subject_slot('selected_chain')
    def _on_selected_chain_changed(self):
        self._update_control_connections()

    @subject_slot('mute')
    def _on_mute_changed(self):
        if self.is_enabled():
            self.mute_button.enabled = self._current_chain is not None
            if self._current_chain:
                self.mute_button.is_on = self._current_chain.mute
        return

    @subject_slot('solo')
    def _on_solo_changed(self):
        if self.is_enabled():
            self.solo_button.enabled = self._current_chain is not None
            if self._current_chain:
                self.solo_button.is_on = self._current_chain.solo
        return

    @subject_slot('is_showing_chain_devices')
    def _on_device_visibility_changed(self):
        if self.is_enabled():
            self.show_chain_button.enabled = self._current_rack is not None
            if self._current_rack:
                self.show_chain_button.is_on = self._current_rack.view.is_showing_chain_devices
        return

    def _update_chain_navigation_buttons(self):
        if self.is_enabled():
            chains = num_chains(self._current_rack)
            can_enable = chains > 1
            self.prev_chain_button.enabled = can_enable
            self.next_chain_button.enabled = can_enable
            if can_enable:
                chain_index = selected_chain_index(self._current_rack)
                self.prev_chain_button.is_on = chain_index > 0
                self.next_chain_button.is_on = chain_index < chains - 1

    def _get_chain_based_path_name(self, path_name):
        """ Returns the friendly chain-based name for the given path name. """
        return '%s  |  %s' % (TRANSLATED_RACK_NAMES[self._rack_class],
         path_name.split('|')[(-1)].strip())

    def _get_assigned_chain_parameter(self, a):
        if a:
            rack = self._manager.get_device_by_class_name(a['rack'])
            if rack:
                chain = rack.view.selected_chain
                if chain:
                    if a['device_class_name']:
                        dev_name = a['device_class_name']
                        has_inst_name = a['device_instance_name'] is not None
                        if has_inst_name:
                            dev_name = a['device_instance_name']
                        path = (
                         (
                          'device', dev_name), ('parameter', a['parameter']))
                        return get_nested_device_parameter(chain, path, by_class=not has_inst_name, by_og_name=True)
                    else:
                        return get_mixer_parameter(rack.view.selected_chain, a['parameter'])

        return

    def _chain_mapping_predicate(self, path):
        if len(path) < 4:
            return False
        else:
            p_slice = path[-4:]
            dev = p_slice[0][1]
            if isinstance(dev, Live.RackDevice.RackDevice):
                if any(self._assignments) and self._rack_class is not None and self._rack_class != dev.class_name:
                    return False
                self._rack_class = dev.class_name
            return True
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/HazMapChainComponent.pyc
