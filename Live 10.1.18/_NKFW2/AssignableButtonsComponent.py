# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\AssignableButtonsComponent.py
# Compiled at: 2018-01-15 18:16:49
from _Framework.CompoundComponent import CompoundComponent
from _Framework.Layer import Layer
from _Framework.SubjectSlot import subject_slot, CallableSubjectSlotGroup
from _Framework.Util import nop
from GlobalButtonsComponent import GlobalButtonsComponent
from ClyphXComponent import ClyphXComponent
from AssignableButtonsConsts import ASSIGNABLES, create_assignment
from ShowMessageMixin import ShowMessageMixin
from ControlUtils import reset_group_buttons
from ClipUtils import delete_clip, duplicate_clip, double_clip

class AssignableButtonsComponent(CompoundComponent, ShowMessageMixin):
    """ AssignableButtonsComponent allows a matrix or group of buttons to control a
    variety of global properties/parameter and trigger ClyphX actions that are defined in
    a file.  The settings for each button in the file should take one of the following
    forms:

        For a matrix:
            ROW_x_BTN_x = assign_name, off_color, on_color
            ROW_x_BTN_x = CX, color, on_action, off_action
        For a button group:
            BTN_x = assign_name, off_color, on_color
            BTN_x = CX, color, on_action, off_action """
    __subject_events__ = ('clip_playing_status', 'track_playing_status')

    def __init__(self, targets_comp, clip_creator=None, color_class=None, is_matrix=True, name='Assignable_Button_Control', *a, **k):
        super(AssignableButtonsComponent, self).__init__(name=name, *a, **k)
        self._color_dict = color_class.__dict__.keys() if color_class else None
        self._color_class_name = str(color_class).split('.')[(-1)] if color_class else ''
        self._is_matrix = bool(is_matrix)
        self._assigned_button_indexes = []
        self._assignable_controls = {}
        self._global_comp_layer = None
        self._global_comp_dict = {}
        self._global_comp = self.register_component(GlobalButtonsComponent(clip_creator=clip_creator))
        self._cx_button_indexes = []
        self._cx_comp = self.register_component(ClyphXComponent(color_class, False))
        self._unassigned_button_listener = self.register_slot_manager(CallableSubjectSlotGroup(event='value', listener=nop, function=nop))
        self._parse_method = self._parse_colored_setting if color_class else self._parse_non_colored_setting
        self._clip = None
        self._scene = None
        self._track = None
        self._on_target_clip_changed.subject = targets_comp
        self._on_target_clip_changed(targets_comp.target_clip)
        self._on_target_track_changed.subject = targets_comp
        self._on_target_track_changed(targets_comp.target_track)
        self.on_selected_scene_changed()
        return

    def disconnect(self):
        super(AssignableButtonsComponent, self).disconnect()
        self._color_dict = None
        self._color_class_name = None
        self._parse_method = None
        self._assigned_button_indexes = None
        self._assignable_controls = None
        self._global_comp = None
        self._global_comp_dict = None
        self._global_comp_layer = None
        self._cx_comp = None
        self._cx_button_indexes = None
        self._unassigned_button_listener = None
        self._clip = None
        self._scene = None
        self._track = None
        return

    def set_physical_display_element(self, element):
        """ Extends standard to set the physical display element of the
        GlobalButtonsComponent. """
        super(AssignableButtonsComponent, self).set_physical_display_element(element)
        if self._global_comp:
            self._global_comp.set_physical_display_element(element)

    def set_shift_button(self, button):
        """ Sets the shift button to use with the GlobalButtonsComponent. """
        if self._global_comp:
            self._global_comp.set_shift_button(button)

    def set_buttons(self, buttons):
        """ Sets the buttons to use with the parsed assignments. """
        buttons = list(buttons) if buttons else None
        if buttons:
            for k, v in self._assignable_controls.iteritems():
                v.set_button(buttons[k])

            if self._global_comp_layer is None and self._global_comp_dict:
                layer_dict = {}
                for k, v in self._global_comp_dict.iteritems():
                    layer_dict[v] = buttons[k]

                self._global_comp_layer = Layer(**layer_dict)
                self._global_comp_dict = None
            self._global_comp.layer = self._global_comp_layer
            if self._cx_button_indexes:
                cx_buttons = [ b if i in self._cx_button_indexes else None for i, b in enumerate(buttons) ]
                self._cx_comp.set_buttons(cx_buttons)
            unassigned = [ b for i, b in enumerate(buttons) if i not in self._assigned_button_indexes ]
            self._unassigned_button_listener.replace_subjects(unassigned)
            reset_group_buttons(unassigned)
        else:
            if self._assignable_controls:
                for v in self._assignable_controls.values():
                    v.set_button(None)

            if self._global_comp:
                self._global_comp.layer = None
            if self._cx_comp:
                self._cx_comp.set_buttons(None)
            if self._unassigned_button_listener:
                self._unassigned_button_listener.replace_subjects([])
        return

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, clip):
        """ Sets the parent of clip-based assignments and sets up subjects. """
        self._clip = clip
        is_midi = clip.is_midi_clip if clip else False
        slot = clip.canonical_parent if clip else None
        if slot:
            slot.duplicate_clip = self._duplicate_clip
            slot.delete_clip = self._delete_clip
        if is_midi:
            clip.double_clip = self._double_clip
        self._on_clip_playing_status_changed.subject = clip
        for c in self._assignable_controls.values():
            if c.floating_type == 'any_clip':
                c.parent = clip
            elif c.floating_type == 'midi_clip':
                c.parent = clip if is_midi else None
            elif c.floating_type == 'audio_clip':
                c.parent = clip if not is_midi else None
            elif c.floating_type == 'self_clip':
                c.parent = self if clip else None
            elif c.floating_type == 'slot':
                c.parent = slot

        return

    @subject_slot('playing_status')
    def _on_clip_playing_status_changed(self):
        """ Notifies listeners on clip playing status changes.  This is needed as the clip
        object itself doesn't include specific enough listeners. """
        self.notify_clip_playing_status()

    @property
    def clip_playing_status--- This code section failed: ---

 L. 157         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_clip'
                6  POP_JUMP_IF_FALSE    43  'to 43'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             0  '_clip'
               15  LOAD_ATTR             1  'is_playing'
               18  JUMP_IF_TRUE_OR_POP    46  'to 46'
               21  LOAD_FAST             0  'self'
               24  LOAD_ATTR             0  '_clip'
               27  LOAD_ATTR             2  'is_triggered'
               30  JUMP_IF_TRUE_OR_POP    46  'to 46'
               33  LOAD_FAST             0  'self'
               36  LOAD_ATTR             0  '_clip'
               39  LOAD_ATTR             3  'is_recording'
               42  RETURN_END_IF    
             43_0  COME_FROM            30  '30'
             43_1  COME_FROM            18  '18'
             43_2  COME_FROM             6  '6'
               43  LOAD_GLOBAL           4  'False'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _play_clip(self):
        """ Toggles the playing status of the clip. This is needed as the clip object
        itself doesn't include specific enough listeners. """
        if self._clip:
            self._clip.is_playing = not self._clip.is_playing

    def _fire_clip(self):
        """ Fires the clip. This is needed as the clip object itself doesn't include
        specific enough listeners. """
        if self._clip:
            self._clip.fire()

    def _delete_clip(self):
        """ Deletes the clip.  This is needed for status message compliance. """
        if self._clip:
            delete_clip(self._clip.canonical_parent, self.component_message)

    def _duplicate_clip(self):
        """ Duplicates the clip and selects the scene it's on. """
        if self._track and self._clip:

            def _callback():
                self.song().view.selected_scene = self.song().scenes[(self._get_scene_index() + 1)]

            duplicate_clip(self.song(), self._clip, callback=_callback, show_message=self.component_message)

    def _double_clip(self):
        """ Doubles the MIDI clip's loop.  This is needed for proper exception
        handling. """
        if self._clip and self._clip.is_midi_clip:
            double_clip(self._clip, self.component_message)

    def on_selected_scene_changed(self):
        """ Sets the parent of scene-based assignments. """
        self._scene = self.song().view.selected_scene
        for c in self._assignable_controls.values():
            if c.floating_type == 'scene':
                c.parent = self._scene

    @subject_slot('target_track')
    def _on_target_track_changed(self, track):
        """ Sets the parent of track-based assignments. """
        is_armable = track and track.can_be_armed
        is_master = track == self.song().master_track
        self._track = track if track in self.song().tracks else None
        self._on_track_playing_status_changed.subject = self._track
        for c in self._assignable_controls.values():
            if c.floating_type == 'not_master_track':
                c.parent = track if not is_master else None
            elif c.floating_type == 'not_master_track_mixer':
                c.parent = track.mixer_device if not is_master else None
            elif c.floating_type == 'armable_track':
                c.parent = track if is_armable else None
            elif c.floating_type == 'self_track':
                c.parent = self if self._track else None

        return

    @subject_slot('playing_slot_index')
    def _on_track_playing_status_changed(self):
        """ Notifies listeners on track playing status changes.  This is needed as the
        track object itself doesn't include specific enough listeners. """
        self.notify_track_playing_status()

    @property
    def track_playing_status--- This code section failed: ---

 L. 226         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_track'
                6  POP_JUMP_IF_FALSE    43  'to 43'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             0  '_track'
               15  LOAD_ATTR             1  'playing_slot_index'
               18  LOAD_CONST               0
               21  COMPARE_OP            5  >=
               24  JUMP_IF_TRUE_OR_POP    46  'to 46'
               27  LOAD_FAST             0  'self'
               30  LOAD_ATTR             0  '_track'
               33  LOAD_ATTR             2  'fired_slot_index'
               36  LOAD_CONST               0
               39  COMPARE_OP            5  >=
               42  RETURN_END_IF    
             43_0  COME_FROM            24  '24'
             43_1  COME_FROM             6  '6'
               43  LOAD_GLOBAL           3  'False'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _stop_track(self):
        """ Stops the track. This is needed as the track object iself doesn't include
        specific enough listeners. """
        if self._track:
            self._track.stop_all_clips()

    def _play_track(self):
        """ Toggles the playing status of the track. This is needed as the track object
        itself doesn't include specific enough listeners. """
        if self._track:
            if self.track_playing_status:
                self._track.stop_all_clips()
            else:
                self._track.clip_slots[self._get_scene_index()].fire()

    def _fire_track(self):
        """ Fires the track. This is needed as the track object itself doesn't include
        specific enough listeners. """
        if self._track:
            self._track.clip_slots[self._get_scene_index()].fire()

    def _fire_track_as_selected(self):
        """ Fires the track and selects the next scene down similar to scene's fire as
        selected. """
        if self._track:
            current_index = self._get_scene_index()
            index_to_select = current_index + 1
            if index_to_select >= len(self.song().scenes):
                index_to_select = 0
            self._track.clip_slots[current_index].fire()
            self.song().view.selected_scene = self.song().scenes[index_to_select]

    def _get_scene_index(self):
        """ Returns the index of the selected scene. """
        return list(self.song().scenes).index(self.song().view.selected_scene)

    def parse_settings(self, settings):
        """ Parses the given dict of settings for button assignments. """
        if settings:
            for k, v in settings.iteritems():
                b_index = self._parse_button_index(k)
                if v.upper().startswith('CX'):
                    self._assigned_button_indexes.append(b_index)
                    self._cx_button_indexes.append(b_index)
                    self._cx_comp.parse_settings({'CX_BTN_%s' % (b_index + 1): v[3:]})
                else:
                    self._parse_method(b_index, v)

            self._on_target_clip_changed(self._clip)
            self._on_target_track_changed(self._track)
            self.on_selected_scene_changed()

    def _parse_colored_setting(self, button_index, setting_value):
        """ Parses a setting that includes LED colors. """
        if button_index >= 0:
            data = setting_value.split(',')
            if len(data) < 3:
                return
            off_color = self._parse_color_name(data[1], False)
            on_color = self._parse_color_name(data[2], True)
            self._create_assignment(button_index, data[0], off_color, on_color)
        return

    def _parse_non_colored_setting(self, button_index, setting_value):
        """ Parses a setting that does not include LED colors. """
        if button_index >= 0 and setting_value:
            self._create_assignment(button_index, setting_value, 'DefaultButton.Off', 'DefaultButton.On')

    def _parse_button_index(self, setting_key):
        """ Parses the given key for the index of the button that the settings
        relate to. """
        try:
            if self._is_matrix:
                row = int(setting_key[4:5]) - 1
                column = int(setting_key[10:]) - 1
                return row * 8 + column
            else:
                return int(setting_key[4:]) - 1

        except ValueError:
            self.canonical_parent.log_message('ValueError when parsing ' + 'AssignableButtonsComponent settings.')
            return -1

    def _parse_color_name(self, color, is_on):
        """ Returns the full color name for the given color or a default color name if
        invalid color name. """
        color = color.upper().strip()
        if color in self._color_dict:
            return '%s.%s' % (self._color_class_name, color)
        return 'DefaultButton.%s' % ('On' if is_on else 'Off')

    def _create_assignment(self, button_index, setting, off_color, on_color):
        """ Creates an assignment and handles its associated setup based on the given
        arguments. """
        assign = ASSIGNABLES.get(setting.upper().strip(), None)
        if assign:
            if assign['type'] == 'global':
                self._global_comp_dict[button_index] = assign['button']
                if assign['button'] == 'increase_button' or assign['button'] == 'decrease_button':
                    self._global_comp.set_default_scroll_color(on_color)
                else:
                    button = getattr(self._global_comp, assign['button'])
                    button.color = off_color
                    button.on_color = on_color
            else:
                parent = self._get_parent(assign['parent'])
                self._assignable_controls[button_index] = self.register_component(create_assignment(parent, assign, off_color, on_color))
            self._assigned_button_indexes.append(button_index)
        return

    def _get_parent(self, parent_name):
        """ Returns the parent object associated with the parent name or None. """
        if parent_name == 'song':
            return self.song()
        else:
            if parent_name == 'song_view':
                return self.song().view
            if parent_name == 'app_view':
                return self.application().view
            if parent_name == 'crossfader':
                return self.song().master_track.mixer_device.crossfader
            return
