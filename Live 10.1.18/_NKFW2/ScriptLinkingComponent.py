# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ScriptLinkingComponent.py
# Compiled at: 2018-04-06 01:46:39
import Live
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import SlotManager, subject_slot
from _Framework.SessionComponent import SessionComponent
from ableton.v2.control_surface.components.session_ring import SessionRingComponent
from SpecialMixerComponent import SpecialMixerComponent

class LinkType(object):
    """ The type of linking to use. """
    horizontal = 0
    vertical = 1
    matched = 2
    matched_track_only = 3


LINK_TYPE_NAMES = [
 'HORIZONTAL', 'VERTICAL', 'MATCHED']
TRACK_ONLY_LINK_TYPES = (
 LinkType.horizontal, LinkType.matched_track_only)
DEFAULT_LINK_NAMES = [ None for _ in xrange(6) ]
DEFAULT_LINK_TYPES = [ LinkType.horizontal for _ in xrange(5) ]

def get_link_type(comp_a, comp_b, link_type):
    """ Returns the link type to use. This will simply return the given link_type
    unless one or both of the components is the SpecialMixerComponent, which can only
    do horizontal or matched_track_only. """
    need_to_verify = isinstance(comp_a, SpecialMixerComponent) or isinstance(comp_b, SpecialMixerComponent)
    if need_to_verify and link_type is not LinkType.horizontal:
        link_type = LinkType.matched_track_only
    return link_type


class ScriptLinkingComponent(ControlSurfaceComponent):
    """ ScriptLinkingComponent manages linking two or more scripts via Linker objects.
    The settings for this are read from a file. The settings within the file should
    include SCRIPT_1, SCRIPT_2 and LINK_TYPE_1 settings at the very least. Up to SCRIPT_6
    and LINK_TYPE_5 is supported. """

    def __init__(self, *a, **k):
        super(ScriptLinkingComponent, self).__init__(*a, **k)
        self.is_private = True
        self._script_names = list(DEFAULT_LINK_NAMES)
        self._link_types = list(DEFAULT_LINK_TYPES)
        self._linkers = []

    def disconnect(self):
        """ Extends standard to disconnect linkers. """
        self._disconnect_linkers()
        super(ScriptLinkingComponent, self).disconnect()
        self._script_names = None
        self._link_types = None
        self._linkers = None
        return

    def parse_settings(self, settings):
        """ Parses a dictionary of settings read from file for link-related settings. """
        if settings:
            for k, v in settings.iteritems():
                if k.startswith('SCRIPT_'):
                    try:
                        index = int(k.replace('SCRIPT_', '')) - 1
                        self._script_names[index] = v
                    except:
                        pass

                if k.startswith('LINK_TYPE_') and v in LINK_TYPE_NAMES:
                    try:
                        index = int(k.replace('LINK_TYPE_', '')) - 1
                        self._link_types[index] = LINK_TYPE_NAMES.index(v)
                    except:
                        pass

        if 'PUSH2' in self._script_names:
            task = partial(self.connect_script_instances, self.canonical_parent._control_surfaces())
            self.canonical_parent.schedule_message(50, task)

    def connect_script_instances(self, scripts):
        """ Called by the ControlSurface to locate the scripts to link up and create
        Linker objects for them. """
        self._disconnect_linkers()
        l_scripts = self._get_linkable_scripts(scripts)
        for index in xrange(5):
            current = self._script_names[index:index + 2]
            if self._can_link_scripts(current, l_scripts):
                link_type = get_link_type(l_scripts[current[0]], l_scripts[current[1]], self._link_types[index])
                self._linkers.append(Linker(self.song(), l_scripts[current[0]], l_scripts[current[1]], link_type))

    def on_track_list_changed(self):
        self._refresh_linkers()

    def on_scene_list_changed(self):
        self._refresh_linkers()

    def _refresh_linkers(self):
        for l in self._linkers:
            l.refresh()

    def _get_linkable_scripts(self, scripts):
        """ Returns a dict of scripts that can be linked to (contain a linkable
        component). """
        avail_scripts = {}
        for script in scripts:
            script_name = script.__class__.__name__.upper()
            if script_name not in avail_scripts and hasattr(script, 'components'):
                l_comp = self._get_linkable_component(script)
                if l_comp:
                    avail_scripts[script_name] = l_comp

        return avail_scripts

    @staticmethod
    def _get_linkable_component(script):
        """ Returns the linkable component (either a SessionComponent,
        SpecialMixerComponent or SessionRingComponent) found in the list of components
        or None. """
        component = None
        for c in script.components:
            if isinstance(c, SessionComponent):
                return c
            if isinstance(c, SpecialMixerComponent) and not c.is_return_mixer:
                component = c

        if component is None:
            if hasattr(script, '_session_ring'):
                return script._session_ring
        return component

    @staticmethod
    def _can_link_scripts(script_names, avail_scripts):
        """ Returns whether the two script_names were found in the dict of available
        scripts. """
        return script_names[0] is not None and script_names[1] is not None and script_names[0] in avail_scripts and script_names[1] in avail_scripts

    def _disconnect_linkers(self):
        for linker in self._linkers:
            linker.disconnect()

        self._linkers = []


class Linker(SlotManager):
    """ Linker handles bidirectionally linking two scripts. """

    def __init__(self, song, comp_a, comp_b, link_type, *a, **k):
        super(Linker, self).__init__(*a, **k)
        self._song = song
        self._link_type = link_type
        self._self_component = comp_a
        self._observed_component = comp_b
        self._track_offset = 0
        self._scene_offset = 0
        self._monkey_patch_component(comp_a)
        self._monkey_patch_component(comp_b)
        add_tracks_listener = True
        self._self_can_link_tracks = True
        self._observed_can_link_tracks = True
        self._can_link_tracks = True
        if link_type in TRACK_ONLY_LINK_TYPES:
            self._on_self_track_offset_changed.subject = comp_a
            self._on_observed_track_offset_changed.subject = comp_b
            self._refresh_method = self._on_self_track_offset_changed
            self._track_offset = comp_a.width() if link_type is LinkType.horizontal else 0
        elif link_type is LinkType.vertical:
            self._on_self_scene_offset_changed.subject = comp_a
            self._on_observed_scene_offset_changed.subject = comp_b
            self._refresh_method = self._on_self_scene_offset_changed
            self._scene_offset = comp_a.height()
            add_tracks_listener = False
        else:
            self._on_self_offsets_changed.subject = comp_a
            self._on_observed_offsets_changed.subject = comp_b
            self._refresh_method = self._on_self_offsets_changed
        if add_tracks_listener:
            if hasattr(comp_a, 'items'):
                self._on_self_tracks_changed.subject = comp_a
            if hasattr(comp_b, 'items'):
                self._on_observed_tracks_changed.subject = comp_b
        self._refresh_method()

    def disconnect(self):
        super(Linker, self).disconnect()
        self._self_component = None
        self._observed_component = None
        self._refresh_method = None
        return

    def refresh(self):
        """ Calls the applicable refresh method, which is dependent upon the type of
        linking in use. """
        self._refresh_method()

    @subject_slot('offset')
    def _on_self_track_offset_changed(self, arg_a=None, arg_b=None):
        self._handle_track_offset_changed(self._self_component, self._observed_component, self._track_offset)

    @subject_slot('offset')
    def _on_observed_track_offset_changed(self, arg_a=None, arg_b=None):
        self._handle_track_offset_changed(self._observed_component, self._self_component, -self._track_offset)

    @subject_slot('offset')
    def _on_self_scene_offset_changed(self, arg_a=None, arg_b=None):
        self._handle_scene_offset_changed(self._self_component, self._observed_component, self._scene_offset)

    @subject_slot('offset')
    def _on_observed_scene_offset_changed(self, arg_a=None, arg_b=None):
        self._handle_scene_offset_changed(self._observed_component, self._self_component, -self._scene_offset)

    @subject_slot('offset')
    def _on_self_offsets_changed(self, arg_a=None, arg_b=None):
        self._handle_offsets_changed(self._self_component, self._observed_component, self._track_offset, self._scene_offset)

    @subject_slot('offset')
    def _on_observed_offsets_changed(self, arg_a=None, arg_b=None):
        self._handle_offsets_changed(self._observed_component, self._self_component, -self._track_offset, -self._scene_offset)

    @subject_slot('tracks')
    def _on_self_tracks_changed(self):
        t = [ isinstance(t, Live.Track.Track) or t is None for t in self._self_component.controlled_tracks()
            ]
        self._self_can_link_tracks = all(t)
        self._can_link_tracks = self._self_can_link_tracks and self._observed_can_link_tracks
        self._refresh_method()
        return

    @subject_slot('tracks')
    def _on_observed_tracks_changed(self):
        t = [ isinstance(t, Live.Track.Track) or t is None for t in self._observed_component.controlled_tracks()
            ]
        self._observed_can_link_tracks = all(t)
        self._can_link_tracks = self._self_can_link_tracks and self._observed_can_link_tracks
        self._refresh_method()
        return

    def _handle_track_offset_changed(self, master, slave, offset_delta):
        """ Handles changing the track offset of the slave relative to the master. """
        if not self._can_link_tracks:
            return
        target_offset = self._get_target_track_offset(master, slave, offset_delta)
        if target_offset >= 0:
            slave.set_offsets(target_offset, slave.scene_offset_method())

    def _handle_scene_offset_changed(self, master, slave, offset_delta):
        """ Handles changing the scene offset of the slave relative to the master. """
        target_offset = self._get_target_scene_offset(master, slave, offset_delta)
        if target_offset >= 0:
            slave.set_offsets(slave.track_offset_method(), target_offset)

    def _handle_offsets_changed(self, master, slave, track_offset_delta, scene_offset_delta):
        """ Handles changing the track and scenes offsets of the slave relative to the
        master. """
        track_target_offset = self._get_target_track_offset(master, slave, track_offset_delta)
        if track_target_offset < 0 or not self._can_link_tracks:
            track_target_offset = slave.track_offset_method()
        scene_target_offset = self._get_target_scene_offset(master, slave, scene_offset_delta)
        if scene_target_offset < 0:
            scene_target_offset = slave.scene_offset_method()
        if track_target_offset == slave.track_offset_method() and scene_target_offset == slave.scene_offset_method():
            return
        slave.set_offsets(track_target_offset, scene_target_offset)

    def _get_target_scene_offset(self, master, slave, offset_delta):
        """ Returns the scene offset to use for the slave or -1 if not in range or the
        same as the current offset. """
        num_scenes = len(self._song.scenes)
        current_offset = slave.scene_offset_method()
        target_offset = min(num_scenes, master.scene_offset_method() + offset_delta)
        if current_offset != target_offset:
            return target_offset
        return -1

    @staticmethod
    def _get_target_track_offset(master, slave, offset_delta):
        """ Returns the track offset to use for the slave or -1 if not in range or the
        same as the current offset. """
        num_tracks = len(slave.tracks_to_use())
        current_offset = slave.track_offset_method()
        target_offset = min(num_tracks, master.track_offset_method() + offset_delta)
        if current_offset != target_offset:
            return target_offset
        return -1

    @staticmethod
    def _monkey_patch_component(comp):
        """ Handles monkey patching the given component so that it will contain the
        methods needed for linking. This is needed since the SessionRingComponent uses
        different method/attribute names for things. """
        if isinstance(comp, SessionRingComponent):
            comp.height = lambda : comp.num_scenes
            comp.width = lambda : comp.num_tracks
            comp.scene_offset_method = lambda : comp.scene_offset
            comp.track_offset_method = lambda : comp.track_offset
        else:
            comp.scene_offset_method = comp.scene_offset
            comp.track_offset_method = comp.track_offset
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ScriptLinkingComponent.pyc
