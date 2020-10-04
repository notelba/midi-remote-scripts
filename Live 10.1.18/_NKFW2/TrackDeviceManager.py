# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackDeviceManager.py
# Compiled at: 2017-05-19 13:42:17
import Live
from _Framework.SubjectSlot import SlotManager, Subject, subject_slot_group, subject_slot
from TrackMixerWrapper import TrackMixerWrapper, SENDS_OFFSET
from Utils import CHAIN_PARAM_DICT, get_device, get_device_instance_name, get_mixer_parameter, get_device_parameter, live_object_is_valid
MAX_NESTED_DEPTH = 5

def get_track_based_path(path):
    """ Returns a formatted path for a track-based mapping. """
    p_slice = path[-2:]
    if p_slice[0][0] == 'mixer':
        p_info = p_slice[1][1]
        if p_slice[1][0] == 'send_parameter':
            p_info = p_slice[1][1] + SENDS_OFFSET
        return {'class_name': 'MixerDevice', 'instance_name': None, 
           'chain': None, 
           'return_chain': None, 
           'parameter': p_info}
    else:
        if p_slice[0][0] == 'chain_mixer':
            dev = path[(-4)][1]
            is_return = path[(-3)][0] == 'return_chain'
            chain_index = path[(-3)][1]
            param_info = (p_slice[1][0],
             CHAIN_PARAM_DICT.get(p_slice[1][1], p_slice[1][1]))
            return {'class_name': dev.class_name, 'instance_name': get_device_instance_name(dev), 
               'chain': chain_index if not is_return else None, 
               'return_chain': chain_index if is_return else None, 
               'parameter': param_info}
        dev = p_slice[0][1]
        return {'class_name': dev.class_name, 'instance_name': get_device_instance_name(dev), 
           'chain': None, 
           'return_chain': None, 
           'parameter': p_slice[1][1]}


def get_track_based_path_name(path_name):
    """ Returns the friendly track-based name for the given path name. """
    p_split = path_name.split('|')
    if 'Chain' in p_split[(-2)] and 'Mixer:' in p_split[(-1)]:
        return (' | ').join(p_split[-3:]).strip()
    return p_split[(-1)].strip()


class TrackDeviceManager(SlotManager, Subject):
    """ TrackDeviceManager observes the devices on a track and notifies interested
    subjects on changes.  This supports one level of nesting and also (optionally)
    includes a wrapper class for the track's mixer so it can be treated like any other
    device. """
    __subject_events__ = ('devices', )

    def __init__(self, targets_comp=None, use_wrapper=False, *a, **k):
        super(TrackDeviceManager, self).__init__(*a, **k)
        self._device_list = []
        self._track = None
        self._wrapper = TrackMixerWrapper() if use_wrapper else None
        self._on_track_changed.subject = targets_comp
        return

    def disconnect(self):
        super(TrackDeviceManager, self).disconnect()
        self._device_list = None
        self._track = None
        self._wrapper = None
        return

    @property
    def devices(self):
        if live_object_is_valid(self._track):
            return self._device_list
        return ()

    @subject_slot('target_track')
    def _on_track_changed(self, track):
        self.set_track(track)

    def set_track(self, track):
        """ Sets the track this component will operate on. """
        assert track is None or isinstance(track, Live.Track.Track)
        self._track = track if live_object_is_valid(track) else None
        if self._wrapper:
            self._wrapper.set_track(track)
        self.update(True)
        return

    @subject_slot_group('devices')
    def _on_devices_changed(self, _):
        self.update()

    @subject_slot_group('chains')
    def _on_chains_changed(self, _):
        self.update()

    @subject_slot_group('return_chains')
    def _on_return_chains_changed(self, _):
        self.update()

    @subject_slot_group('parameters')
    def _on_parameters_changed(self, _):
        self.update(True)

    def update(self, track_changed=False):
        """ Sets up listeners for devices and chains on the track and notifies
        listeners. """
        chain_containers = []
        device_containers = []
        return_chain_containers = []
        self._device_list = []
        if self._track:
            self._device_list = [self._wrapper] if self._wrapper else []
            device_containers = [self._track]
            for device in self._track.devices:
                self._device_list.append(device)
                if device.can_have_chains:
                    chain_containers.append(device)
                    return_chain_containers.append(device)
                    for c in device.chains + device.return_chains:
                        device_containers.append(c)
                        for cd in c.devices:
                            self._device_list.append(cd)

        self._on_return_chains_changed.replace_subjects(return_chain_containers)
        self._on_chains_changed.replace_subjects(chain_containers)
        self._on_devices_changed.replace_subjects(device_containers)
        self._on_parameters_changed.replace_subjects(self._device_list)
        self.notify_devices(track_changed=track_changed)

    def get_device_by_class_name(self, class_name, instance_name=None):
        """ Returns the device in the device list associated with the
        given class name. Can optionally specify an instance_name, which will
        only retrieve the device in the list that match the class and instance name.
        Note, this can't be used in place of function in Utils as this class contains
        the mixer wrapper. """
        return get_device(self, name=instance_name, class_name=class_name)

    def get_assigned_track_parameter(self, a):
        """ Returns the track-based parameter for the given assignment. """
        if a:
            dev = self.get_device_by_class_name(a['class_name'], a['instance_name'])
            if live_object_is_valid(dev):
                if a['chain'] is not None:
                    return get_mixer_parameter(dev.chains[a['chain']], a['parameter'])
                if a['return_chain'] is not None:
                    return get_mixer_parameter(dev.return_chains[a['return_chain']], a['parameter'])
                return get_device_parameter(dev, a['parameter'])
        return

    def get_multi_device_track_parameter(self, dev_dict, param_index, page_index=None):
        """ Returns the track-based parameter from the given dev_dict at the given index.
        The dict should be in the form (used OrderedDict to preserve key order):
        {dev1_class_name: {'instance_name': name, 'parameters': param_list},
         dev2_class_name: {'instance_name': name, 'parameters': param_list}, etc}
        If passing page_index, param_lists should be nested. """
        for k, v in dev_dict.iteritems():
            dev = get_device(self, name=v['instance_name'], class_name=k)
            if live_object_is_valid(dev):
                if page_index is not None:
                    return get_device_parameter(dev, v['parameters'][page_index][param_index])
                return get_device_parameter(dev, v['parameters'][param_index])

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackDeviceManager.pyc
