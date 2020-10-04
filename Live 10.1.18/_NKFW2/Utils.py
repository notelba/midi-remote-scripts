# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\Utils.py
# Compiled at: 2018-01-15 18:16:49
import Live, datetime
from _Framework.Util import find_if
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
MIXER_PARAM_DICT = {'Track Volume': 'volume', 'Track Panning': 'panning', 
   'Speaker On': 'track_activator', 
   'X-Fade Assign': 'crossface_assign', 
   'Preview Volume': 'cue_volume', 
   'Song Tempo': 'song_tempo'}
CHAIN_PARAM_DICT = {'Chain Volume': 'volume', 'Chain Panorama': 'panning', 
   'Speaker On': 'chain_activator'}

def date_has_passed(date):
    """ Returns whether the date in the form of (month, year) has passed. """
    now = datetime.datetime.now()
    current_date = (now.month, now.year)
    year_comp = current_date[1] > date[1]
    year_equal = current_date[1] == date[1]
    month_comp = current_date[0] > date[0]
    if year_comp or year_equal and month_comp:
        return True
    return False


def format_absolute_time(element, time, base_is_one=True):
    """ Returns a string representing the given absolute time as bars.beats.sixteenths.
        Can specify whether the base for displaying is one or zero."""
    assert isinstance(element, (Live.Clip.Clip, Live.Song.Song))
    assert isinstance(time, float)
    base = int(base_is_one)
    beat_length = 4.0 / element.signature_denominator
    bar_length = beat_length * element.signature_numerator
    bar = int(time / bar_length) + base
    beat = int(time / beat_length % element.signature_numerator) + base
    teenth_as_float = time % beat_length / 0.25 + base
    teenth_as_int = int(teenth_as_float)
    teenth_plus = ''
    if teenth_as_float % 1.0 != 0.0:
        teenth_plus = '+'
    return '%s.%s.%s%s' % (bar, beat, teenth_as_int, teenth_plus)


def calculate_bar_length(obj):
    """ Returns the length of a bar at the current time signature. """
    return 4.0 / obj.signature_denominator * obj.signature_numerator


def calculate_beat_length(obj):
    """ Returns the length of a beat at the current time signature. """
    return 4.0 / obj.signature_denominator


def parse_file(file_name, file_path, logger=None, to_upper=True):
    """ Reads the given file name from the given path and returns a dict of
    the keys and values it contains. """
    file_to_read = file_path + '/' + file_name
    try:
        with open(file_to_read) as (f):
            if logger:
                logger('Attempting to read %s' % file_to_read)
            file_data = {}
            for line in f:
                if '=' in line and not line.startswith('#'):
                    data = line.split('=')
                    if len(data) == 2:
                        if logger:
                            logger(str(line))
                        file_data[data[0].strip()] = data[1].upper().strip() if to_upper else data[1].strip()

            return file_data
    except IOError:
        if logger:
            logger('%s is missing!' % file_to_read)


def parse_int(int_as_string, default_value=None, min_value=None, max_value=None):
    """ Parses the given string containing an int and returns the parsed int. If a parse
    error occurs, the default_value will be returned. If a min_value or max_value i
    given, the default_value will be returned if the parsed_value is not within range. """
    ret_value = default_value
    try:
        parsed_value = int(int_as_string)
        if min_value is not None and parsed_value < min_value:
            return ret_value
        if max_value is not None and parsed_value > max_value:
            return ret_value
        ret_value = parsed_value
    except:
        pass

    return ret_value


def floats_equal(a, b, rel_tol=1e-09, abs_tol=0.0):
    """ Returns whether or not the given floats are close to being equal. """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def live_object_is_valid(obj):
    """ Returns whether or not the given object is still present and not a lost
    weak reference. """
    if isinstance(obj, ControlSurfaceComponent) and obj.name == 'Track_Mixer_Device':
        return obj.track != None
    else:
        return obj != None


def get_name(obj):
    """" Returns the name of the given object or unnamed if the object has no name.  This
    is only useful in cases where it's possible that the object is not named such as with
    clips and scenes. """
    name = ''
    if obj:
        name = 'unnamed'
        if obj.name:
            name = obj.name
    return name


def get_track_by_name(song, name):
    """ Returns the track associated with the given name or None. """
    if name == 'Master':
        return song.master_track
    else:
        for track in song.return_tracks:
            if track.name == name:
                return track

        for track in song.tracks:
            if track.name == name:
                return track

        return


def delete_track(song, track, show_message=None):
    """ Deletes the given track/return track. """
    try:
        name = track.name
        if track in song.tracks:
            song.delete_track(list(song.tracks).index(track))
        elif track in song.return_tracks:
            song.delete_return_track(list(song.return_tracks).index(track))
        if show_message:
            show_message('Track Deleted', name)
    except:
        pass


def duplicate_track(song, track, show_message=None):
    """ Duplicate the given track. """
    if track in song.tracks:
        try:
            name = track.name
            song.duplicate_track(list(song.tracks).index(track))
            if show_message:
                show_message('Track Duplicated', name)
        except:
            pass


def right_justify_track_components(song, tracks_to_use, offset, components):
    """ Assigns the given components to tracks by right justifying return tracks if
    possible. """
    tracks_len = len(tracks_to_use)
    returns = song.return_tracks
    num_strips = len(components)
    empty_tracks = max(0, num_strips + offset - tracks_len)
    num_tracks = max(0, tracks_len - len(returns) - offset)
    num_returns = num_strips - empty_tracks - num_tracks
    for index in xrange(num_strips):
        track_index = offset + index
        if tracks_len > track_index:
            track = tracks_to_use[track_index]
            if track in returns:
                components[(index + empty_tracks)].set_track(track)
            else:
                components[index].set_track(track)
        else:
            components[(index - num_returns)].set_track(None)

    return


def get_device(track_or_chain, name=None, class_name=None):
    """ Returns the device on the given track or chain with the given name, class_name or
    both. """
    if live_object_is_valid(track_or_chain):
        if name is not None and class_name is not None:
            return find_if(lambda x: x.class_name == class_name and x.name == name, track_or_chain.devices)
        if name is not None:
            return find_if(lambda x: x.name == name, track_or_chain.devices)
        return find_if(lambda x: x.class_name == class_name, track_or_chain.devices)
    else:
        return


def get_device_instance_name(dev, apply_to_builtin=True):
    """ For plugins for M4L devices, returns the instance name of the device.  If
    specified will return the instance of name of built in devices.  Returns None
    otherwise. """
    if 'PluginDevice' in dev.class_name or dev.class_name.startswith('MxD'):
        return dev.name
    else:
        if apply_to_builtin and dev.name != dev.class_display_name:
            return dev.name
        return


def get_enclosing_rack(device):
    """ Returns the device if it's a rack itself, the rack that contans the device if
    it's in a rack or None. """
    if live_object_is_valid(device):
        if isinstance(device, Live.RackDevice.RackDevice):
            return device
        if isinstance(device.canonical_parent, Live.Chain.Chain):
            return device.canonical_parent.canonical_parent
    return


def num_chains(rack):
    """ Returns the number of chains and return chains in the given rack. """
    if live_object_is_valid(rack) and isinstance(rack, Live.RackDevice.RackDevice):
        return len(rack.chains) + len(rack.return_chains)
    return 0


def selected_chain_index(rack):
    """ Returns the index of selected chain or return chain in the given rack. """
    if live_object_is_valid(rack) and isinstance(rack, Live.RackDevice.RackDevice):
        try:
            return list(rack.chains).index(rack.view.selected_chain)
        except:
            try:
                return list(rack.return_chains).index(rack.view.selected_chain) + len(rack.chains)
            except:
                pass

    return -1


def increment_selected_chain(rack, factor, wrap=False, show_msg=None):
    """ Incremets the selected chain index by the given factor with optional wrapping.
    Can also show msg in status bar if passed a show msg method. """
    if live_object_is_valid(rack) and isinstance(rack, Live.RackDevice.RackDevice):
        current = selected_chain_index(rack)
        new_selection = current + factor
        num_reg_chains = len(rack.chains)
        in_range = new_selection in xrange(num_chains(rack))
        if in_range or wrap:
            if not in_range:
                new_selection = 0
            chain_to_select = None
            is_rtn = False
            if new_selection >= num_reg_chains:
                chain_to_select = rack.return_chains[(new_selection - num_reg_chains)]
                is_rtn = True
            else:
                chain_to_select = rack.chains[new_selection]
            if chain_to_select:
                rack.view.selected_chain = chain_to_select
                if show_msg:
                    show_msg('Selected %sChain' % ('Return ' if is_rtn else ''), chain_to_select.name)
    return


def get_device_parameter(device, name, by_og_name=False):
    """ Returns the device's parameter of the given name (which can be its index) or
    original name if specified. """
    if live_object_is_valid(device):
        if isinstance(name, int):
            if name in xrange(len(device.parameters)) and device.parameters[name].is_enabled:
                return device.parameters[name]
            return
        if isinstance(device, Live.RackDevice.RackDevice):
            by_og_name = False
        if by_og_name:
            return find_if(lambda x: x.original_name == name and x.is_enabled, device.parameters)
        return find_if(lambda x: x.name == name and x.is_enabled, device.parameters)
    else:
        return


def get_nested_device_parameter(chain, path, by_class=False, by_og_name=False):
    """ Returns the parameter at the given path on the chain. """
    if live_object_is_valid(chain):
        current_obj = chain
        for p in path:
            if p[0] == 'device':
                if by_class:
                    current_obj = get_device(current_obj, class_name=p[1])
                else:
                    current_obj = get_device(current_obj, name=p[1])
            elif p[0] == 'chain':
                current_obj = current_obj.chains[p[1]]
            else:
                return get_device_parameter(current_obj, p[1], by_og_name=by_og_name)

    return


def get_mixer_parameter(track_or_chain, param_path):
    """ Returns the mixer parameter at the given path on the track or chain or None. """
    if live_object_is_valid(track_or_chain):
        is_send_param = param_path[0] == 'send_parameter'
        if is_send_param:
            if param_path[1] in xrange(len(track_or_chain.mixer_device.sends)):
                return track_or_chain.mixer_device.sends[param_path[1]]
            return
        return getattr(track_or_chain.mixer_device, param_path[1], None)
    else:
        return


def resolve_path_for_parameter(param, by_name=True):
    """ Returns a list of tuples that indicate the path to use to access a
    parameter. By default this will use strings to indicate the path, but can optionally
    use actual objects (where necessary). """
    path = []
    current_obj = param if live_object_is_valid(param) else None
    while True:
        if current_obj is not None:
            if isinstance(current_obj, Live.DeviceParameter.DeviceParameter):
                path.append(_get_parameter_type(param, by_name))
            elif isinstance(current_obj, Live.ChainMixerDevice.ChainMixerDevice):
                path.append(('chain_mixer', None))
            elif isinstance(current_obj, Live.Chain.Chain):
                try:
                    chains = list(current_obj.canonical_parent.chains)
                    path.append(('chain', chains.index(current_obj)))
                except:
                    chains = list(current_obj.canonical_parent.return_chains)
                    path.append(('return_chain', chains.index(current_obj)))

            elif isinstance(current_obj, Live.Device.Device):
                path.append(('device', current_obj.name if by_name else current_obj))
            elif isinstance(current_obj, Live.MixerDevice.MixerDevice):
                path.append(('mixer', None))
            elif isinstance(current_obj, Live.Track.Track):
                path.append(('track', current_obj.name if by_name else current_obj))
        if hasattr(current_obj, 'canonical_parent'):
            current_obj = current_obj.canonical_parent
        else:
            break

    path.reverse()
    return path


def resolve_name_for_path(song, path, param):
    """ Returns a friendly name for the given path for display purposes. """
    if path and param is not None:
        name = '%s | ' % _get_name_of_object(path[0][1])
        if path[1][0] == 'mixer':
            name += 'Mixer: '
            if path[2][0] == 'send_parameter':
                name += '%s' % song.return_tracks[path[2][1]].name
            else:
                name += '%s' % param.name
        elif path[1][0] == 'device':
            name += _get_name_of_object(path[1][1])
            if path[2][0] == 'parameter':
                name += ': %s' % param.name
            else:
                for p in path[2:]:
                    if p[0].endswith('chain'):
                        name += ' | %sChain %s' % (
                         'Return ' if p[0] == 'return_chain' else '', p[1] + 1)
                    elif p[0] == 'device':
                        name += ' | %s' % _get_name_of_object(p[1])
                    elif p[0].endswith('mixer'):
                        name += ' | Mixer'
                    elif p[0].endswith('parameter'):
                        name += ': %s' % param.name

        return name
    return ''


def resolve_path_name_for_parameter(song, param):
    """ Convenience function that returns a friendly name for the path of the given
    parameters.  This is only useful in cases where the path to the parameter is not
    already known. """
    return resolve_name_for_path(song, resolve_path_for_parameter(param), param)


def _get_name_of_object(obj):
    """ Returns the name of the object if it's not already a name itself. """
    if isinstance(obj, (str, unicode)):
        return obj
    return obj.name


def resolve_parameter_for_path(song, path):
    """ Returns the parameter at the given path or None. """
    try:
        track = get_track_by_name(song, path[0][1])
        if track:
            if path[1][0] == 'mixer':
                return get_mixer_parameter(track, path[2])
            device = get_device(track, name=path[1][1])
            if device:
                if path[2][0] == 'chain':
                    chain = device.chains[path[2][1]]
                    if path[3][0] == 'chain_mixer':
                        return get_mixer_parameter(chain, path[4])
                    return get_nested_device_parameter(chain, path[3:])
                if path[2][0] == 'return_chain':
                    return_chain = device.return_chains[path[2][1]]
                    if path[3][0] == 'chain_mixer':
                        return get_mixer_parameter(return_chain, path[4])
                    return get_nested_device_parameter(return_chain, path[3:])
                return get_device_parameter(device, path[2][1])
    except:
        return

    return


def _get_parameter_type(param, by_name=True):
    parent = param.canonical_parent
    if isinstance(parent, Live.MixerDevice.MixerDevice):
        track_send_names = [ s.name for s in parent.sends ]
        if param.name in track_send_names:
            return ('send_parameter', track_send_names.index(param.name))
        return (
         'parameter', MIXER_PARAM_DICT[param.name] if by_name else param.name)
    if isinstance(parent, Live.ChainMixerDevice.ChainMixerDevice):
        if param.name == 'Send' or 'Chain Send' in param.name:
            return ('send_parameter', list(parent.sends).index(param))
        return (
         'parameter', CHAIN_PARAM_DICT[param.name] if by_name else param.name)
    return (
     'parameter', _get_device_parameter_name_or_index(parent, param, by_name))


def _get_device_parameter_name_or_index(device, param, by_name):
    """ This is needed for cases where duplicate same named parameters exist. The
    parameter's index will be used in such cases. """
    if isinstance(device, Live.RackDevice.RackDevice):
        by_name = True
    p_name = param.name if by_name else param.original_name
    p_list = list(device.parameters)
    param_names = [ p.name if by_name else p.original_name for p in p_list ]
    num_count = param_names.count(p_name)
    if num_count > 1:
        return p_list.index(param)
    return p_name
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/Utils.pyc
