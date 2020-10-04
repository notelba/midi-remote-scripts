# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TrackRoutingComponent.py
# Compiled at: 2017-04-24 12:52:36
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from PropertyControl import PropertyControl
from ShowMessageMixin import ShowMessageMixin, DisplayType
ROUTING_NAMES = ('input', 'input_sub', 'output', 'output_sub')
MONITOR_NAMES = ('In', 'Auto', 'Off')
XFADE_NAMES = ('A', 'Off', 'B')

class Routing(object):
    """ Routing handles a track's routing type. These are different from other sorts
    of properties as they are set by name and the available settings can change depending
    on other routings. """

    def __init__(self, route_name, is_type=False, *a, **k):
        super(Routing, self).__init__(*a, **k)
        self._route_name = route_name
        self._route_type = 'type' if is_type else 'channel'
        self._track = None
        self._routings = None
        self._num_routings = 0
        self._routing_listeners = []
        self._routing_list_listeners = []
        return

    def disconnect(self):
        self._remove_internal_listeners()
        self._track = None
        self._routings = None
        self._routing_listeners = None
        self._routing_list_listeners = None
        return

    def set_track(self, track, suppress_list_call=False):
        """ Sets the track to control and manages listeners. """
        self._remove_internal_listeners()
        self._track = None
        self._routings = None
        self._num_routings = 0
        if track and (track.has_audio_input or track.has_midi_input):
            self._track = track
            self._refresh_routings()
            self._add_internal_listeners(suppress_list_call)
        return

    def add_routing_listener(self, listener):
        """ Adds a listener that will be called when this routing changes. """
        self._routing_listeners.append(listener)

    def remove_routing_listener(self, listener):
        """ Removes a previously added listener. """
        if listener in self._routing_listeners:
            self._routing_listeners.remove(listener)

    def add_routing_list_listener(self, listener):
        """ Adds a listener that will be called when the routing destination list
        changes. """
        self._routing_list_listeners.append(listener)

    def remove_routing_list_listener(self, listener):
        """ Removes a previously added listener. """
        if listener in self._routing_list_listeners:
            self._routing_list_listeners.remove(listener)

    @property
    def route_name(self):
        """ Returns the name of the current routing target. """
        if self._track and self._routings:
            return self._routings[self.routing].display_name
        return ''

    @property
    def num_routings(self):
        """ Returns the number of available routings. """
        return self._num_routings

    def _get_routing(self):
        if self._track:
            current = getattr(self._track, '%s_routing_%s' % (self._route_name,
             self._route_type))
            if current in self._routings:
                return self._routings.index(current)
        return 0

    def _set_routing(self, index):
        if self._track and index in xrange(self._num_routings):
            new_route = self._routings[index]
            if new_route in self._routings:
                setattr(self._track, '%s_routing_%s' % (self._route_name, self._route_type), new_route)

    routing = property(_get_routing, _set_routing)

    def _refresh_routings(self):
        """ Refreshes the list of routings for the current track. """
        self._routings = None
        self._num_routings = 0
        if self._track:
            self._routings = list(getattr(self._track, 'available_%s_routing_%ss' % (
             self._route_name, self._route_type)))
            self._num_routings = len(self._routings)
        return

    def _on_routing_changed(self):
        for listener in self._routing_listeners:
            listener()

    def _on_routing_list_changed(self):
        self.set_track(self._track, suppress_list_call=True)
        for listener in self._routing_list_listeners:
            listener()

    def _add_internal_listeners(self, suppress_list_call=False):
        add_method = getattr(self._track, 'add_%s_routing_%s_listener' % (self._route_name,
         self._route_type))
        add_method(self._on_routing_changed)
        add_method = getattr(self._track, 'add_available_%s_routing_%ss_listener' % (
         self._route_name, self._route_type))
        add_method(self._on_routing_list_changed)
        if not suppress_list_call:
            self._on_routing_list_changed()
        self._on_routing_changed()

    def _remove_internal_listeners(self):
        if self._track:
            remove_method = getattr(self._track, 'remove_%s_routing_%s_listener' % (
             self._route_name, self._route_type))
            has_method = getattr(self._track, '%s_routing_%s_has_listener' % (
             self._route_name, self._route_type))
            if has_method(self._on_routing_changed):
                remove_method(self._on_routing_changed)
            remove_method = getattr(self._track, 'remove_available_%s_routing_%ss_listener' % (
             self._route_name, self._route_type))
            has_method = getattr(self._track, 'available_%s_routing_%ss_has_listener' % (
             self._route_name, self._route_type))
            if has_method(self._on_routing_list_changed):
                remove_method(self._on_routing_list_changed)


class TrackRoutingComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ TrackRoutingComponent provides control over a track's routing via encoders. """

    def __init__(self, targets_comp=None, name='Track_Routing_Control', *a, **k):
        super(TrackRoutingComponent, self).__init__(name=name, *a, **k)
        self._routing_objects = (Routing('input', True), Routing('input'),
         Routing('output', True), Routing('output'))
        in_transform = lambda x: self._routing_objects[0].route_name
        in_ch_transform = lambda x: self._routing_objects[1].route_name
        out_transform = lambda x: self._routing_objects[2].route_name
        out_ch_transform = lambda x: self._routing_objects[3].route_name
        self._wrapper_dict = {'input': PropertyControl('routing', self._routing_objects[0], (0, 1), can_enforce_takeover=False, display_name='In', display_callback=self._display_input, display_value_transform=in_transform), 
           'input_sub': PropertyControl('routing', self._routing_objects[1], (0, 1), can_enforce_takeover=False, display_name='In Ch', display_callback=self._display_input_sub, display_value_transform=in_ch_transform), 
           'output': PropertyControl('routing', self._routing_objects[2], (0, 1), can_enforce_takeover=False, display_name='Out', display_callback=self._display_output, display_value_transform=out_transform), 
           'output_sub': PropertyControl('routing', self._routing_objects[3], (0, 1), can_enforce_takeover=False, display_name='Out Ch', display_callback=self._display_output_sub, display_value_transform=out_ch_transform), 
           'monitor': PropertyControl('current_monitoring_state', None, (0, 2), rel_thresh=30, value_items=MONITOR_NAMES, display_name='Monitor', display_callback=self._display_monitoring, display_value_transform=lambda x: MONITOR_NAMES[x]), 
           'crossfade_assign': PropertyControl('crossfade_assign', None, (0, 2), rel_thresh=30, value_items=XFADE_NAMES, display_name='XFade', display_callback=self._display_crossfade_assign, display_value_transform=lambda x: XFADE_NAMES[x])}
        self._crossfade_assign_control = None
        self._on_target_track_changed.subject = targets_comp
        self._routing_objects[0].add_routing_list_listener(self._in_routings_changed)
        self._routing_objects[1].add_routing_list_listener(self._in_sub_routings_changed)
        self._routing_objects[2].add_routing_list_listener(self._out_routings_changed)
        self._routing_objects[3].add_routing_list_listener(self._out_sub_routings_changed)
        return

    def disconnect(self):
        for w in self._wrapper_dict.values():
            w.disconnect()

        for r in self._routing_objects:
            r.disconnect()

        super(TrackRoutingComponent, self).disconnect()
        self._crossfade_assign_control = None
        return

    def __getattr__(self, name):
        """ Overrides standard to handle setters for PropertyControls. """
        if len(name) > 4 and name[:4] == 'set_':
            return partial(self._set_control, name[4:].replace('_control', ''))

    def set_track(self, track):
        """ Sets the track to control. """
        routable_track = track in self.song().tracks and not track.is_foldable
        for i, r in enumerate(self._routing_objects):
            self._wrapper_dict[ROUTING_NAMES[i]].set_parent(self._routing_objects[i] if routable_track else None)
            r.set_track(track if routable_track else None)
            self._wrapper_dict[ROUTING_NAMES[i]].set_range((0,
             max(r.num_routings - 1, 1)))

        self._refresh_track_to_control(track)
        return

    def _set_control(self, name, control):
        self._wrapper_dict[name].set_control(control)

    @subject_slot('target_track')
    def _on_target_track_changed(self, track):
        self.set_track(track)

    def _refresh_track_to_control(self, track=None):
        if track is None:
            track = self._on_target_track_changed.subject.target_track
        self._wrapper_dict['monitor'].set_parent(track if track in self.song().tracks and not track.is_foldable else None)
        self._wrapper_dict['crossfade_assign'].set_parent(track.mixer_device if track in self.song().tracks or track in self.song().return_tracks else None)
        return

    def update(self):
        super(TrackRoutingComponent, self).update()
        for w in self._wrapper_dict.values():
            w.update()

    def _in_routings_changed(self):
        self._wrapper_dict['input'].set_range((
         0, max(self._routing_objects[0].num_routings - 1, 1)))

    def _in_sub_routings_changed(self):
        self._wrapper_dict['input_sub'].set_range((
         0, max(self._routing_objects[1].num_routings - 1, 1)))

    def _out_routings_changed(self):
        self._wrapper_dict['output'].set_range((
         0, max(self._routing_objects[2].num_routings - 1, 1)))

    def _out_sub_routings_changed(self):
        self._wrapper_dict['output_sub'].set_range((
         0, max(self._routing_objects[3].num_routings - 1, 1)))

    def _display_input(self, _):
        self.component_message('Input Type', str(self._wrapper_dict['input']))

    def _display_input_sub(self, _):
        self.component_message('Input Channel', str(self._wrapper_dict['input_sub']))

    def _display_output(self, _):
        self.component_message('Output Type', str(self._wrapper_dict['output']))

    def _display_output_sub(self, _):
        self.component_message('Output Channel', str(self._wrapper_dict['output_sub']))

    def _display_monitoring(self, value):
        self.component_message('Monitoring', MONITOR_NAMES[value], display_type=DisplayType.STATUS)

    def _display_crossfade_assign(self, value):
        self.component_message('Crossfade Assignment', XFADE_NAMES[value], display_type=DisplayType.STATUS)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TrackRoutingComponent.pyc
