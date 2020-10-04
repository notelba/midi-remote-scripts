# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialSessionRecordingComponent.py
# Compiled at: 2017-03-07 13:28:53
import Live
from _Framework.SessionRecordingComponent import SessionRecordingComponent, subject_slot

class DummyCreator(object):
    """ Dummy object to pass to base class to prevent the base class from causing issues
    with the specialized version. """
    fixed_length = None


class SpecialSessionRecordingComponent(SessionRecordingComponent):
    """ Specialized SessionRecordingComponent that doesn't require a view controller,
     allows for proper skin usage, adds a button to create MIDI clips and
     works with targets. """

    def __init__(self, targets_component, clip_creator, multi_trk_record, name='Session_Recording_Control', *a, **k):
        super(SpecialSessionRecordingComponent, self).__init__(clip_creator=DummyCreator(), view_controller=True, name=name, *a, **k)
        self._automation_toggle.view_transform = lambda x: 'Recording.Automation%s' % ('On' if x else 'Off')
        self._delete_automation.view_transform = lambda x: 'Recording.Can%sDeleteAutomation' % ('' if x else 'not')
        self._re_enable_automation_toggle.view_transform = lambda x: 'Recording.Can%sEnableAutomation' % ('' if x else 'not')
        self._on_target_track_changed.subject = targets_component
        self._on_target_clip_changed.subject = targets_component
        self._targets_component = targets_component
        self._use_multi_trk_ssn_record = multi_trk_record
        self._clip_creator = clip_creator

    def disconnect(self):
        super(SpecialSessionRecordingComponent, self).disconnect()
        self._targets_component = None
        self._clip_creator = None
        return

    def set_create_clip_button(self, button):
        """ Sets the button to use for creating MIDI clips in empty slots. """
        self._on_create_clip_button_value.subject = button
        self._update_create_clip_button()

    @subject_slot('value')
    def _on_record_button_value(self, value):
        """ Overrides standard to handle fixed length recording and single or multi-track
        behavior. """
        if value:
            song = self.song()
            trk = self._targets_component.target_track
            trk_can_record = trk.can_be_armed and (trk.arm or trk.implicit_arm) and song.session_record_status == Live.Song.SessionRecordStatus.off
            slot_can_record = False
            if trk_can_record:
                slot = trk.clip_slots[list(song.scenes).index(song.view.selected_scene)]
                slot_can_record = not slot.has_clip
            if trk_can_record and slot_can_record:
                creator = self._clip_creator
                if self._use_multi_trk_ssn_record:
                    if creator.fixed_length_enabled:
                        song.trigger_session_record(creator.fixed_length)
                    else:
                        song.trigger_session_record()
                else:
                    self.song().overdub = True
                    if creator.fixed_length_enabled:
                        slot.fire(record_length=creator.fixed_length)
                    else:
                        slot.fire()
            else:
                song.session_record = not song.session_record

    @subject_slot('value')
    def _on_create_clip_button_value(self, value):
        if self.is_enabled() and value:
            slot = self._get_empty_slot()
            if slot:
                self._clip_creator.create_clip(slot)

    @subject_slot('value')
    def _on_new_button_value(self, value):
        """ Overrides standard to use target track. """
        if self.is_enabled() and value and self._prepare_new_action():
            song = self.song()
            view = song.view
            try:
                track = self._targets_component.target_track
                if view.selected_track != track:
                    view.selected_track = track
                selected_scene_index = list(song.scenes).index(view.selected_scene)
                track.stop_all_clips(False)
                self._jump_to_next_slot(track, selected_scene_index)
            except Live.Base.LimitationError:
                self._handle_limitation_error_on_scene_creation()

            self._view_selected_clip_detail()

    def _prepare_new_action(self):
        """ Overrides standard to use target track. """
        song = self.song()
        track = self._targets_component.target_track
        if track.can_be_armed:
            song.overdub = False
            return True

    @subject_slot('value')
    def _on_delete_automation_value(self, value):
        """ Overrides standard to use target track. """
        if self.is_enabled() and value:
            clip = self._get_playing_clip()
            track = self._targets_component.target_track
            track_frozen = track and track.is_frozen
            if clip and not track_frozen:
                clip.clear_all_envelopes()

    def _get_playing_clip(self):
        """ Overrides standard to return target clip, which may not be playing. """
        if self._targets_component:
            return self._targets_component.target_clip
        else:
            return
            return

    def update(self):
        super(SpecialSessionRecordingComponent, self).update()
        self._update_create_clip_button()

    def _update_record_button(self):
        """ Overrides standard to properly handle skin. """
        if self.is_enabled() and self._record_button:
            song = self.song()
            status = song.session_record_status
            if status == Live.Song.SessionRecordStatus.transition:
                self._record_button.set_light('Recording.Transition')
            elif status == Live.Song.SessionRecordStatus.on or song.session_record:
                self._record_button.set_light('Recording.On')
            else:
                self._record_button.set_light('Recording.Off')

    def _update_generic_new_button(self, new_button):
        """ Overrides standard to properly handle skin and target track. """
        if self.is_enabled() and new_button:
            track = self._targets_component.target_track
            can_new = track in self.song().tracks and track.can_be_armed and track.clip_slots[list(self.song().scenes).index(self.song().view.selected_scene)].has_clip
            new_button.set_light('Recording.NewOn' if can_new else 'Recording.NewOff')

    def _update_create_clip_button(self):
        if self.is_enabled():
            button = self._on_create_clip_button_value.subject
            if button:
                button.set_light('Recording.CreateOn' if self._get_empty_slot() else 'Recording.CreateOff')

    def _get_empty_slot(self):
        """ Returns an empty slot that can be used for creating a MIDI clip or None. """
        track = self._targets_component.target_track
        if track and track.has_midi_input:
            slot = track.clip_slots[list(self.song().scenes).index(self.song().view.selected_scene)]
            if slot.has_clip:
                return
            return slot
        return

    def _view_selected_clip_detail(self):
        """ Overrides standard to not call to view controller. """
        view = self.song().view
        if view.highlighted_clip_slot.clip:
            view.detail_clip = view.highlighted_clip_slot.clip
        app_view = self.application().view
        if not app_view.is_view_visible('Detail'):
            app_view.show_view('Detail')
        if not app_view.is_view_visible('Detail/Clip'):
            app_view.show_view('Detail/Clip')

    @subject_slot('target_track')
    def _on_target_track_changed(self, _):
        self.update()

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, _):
        self.update()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialSessionRecordingComponent.pyc
