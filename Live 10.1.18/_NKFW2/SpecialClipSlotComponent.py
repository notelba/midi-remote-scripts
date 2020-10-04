# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialClipSlotComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.SubjectSlot import subject_slot
from ShowMessageMixin import ShowMessageMixin
from ClipUtils import delete_clip, duplicate_clip, double_clip
from ControlUtils import is_button_pressed
from Utils import get_name, live_object_is_valid

class SpecialClipSlotComponent(ClipSlotComponent, ShowMessageMixin):
    """ SpecialClipSlotComponent extends standard to add new modifiers (double and
    quantize buttons), handle automatic track arming and fixed length recording.  This
    can also block group clips from being launched if elected. """

    def __init__(self, *a, **k):
        self._should_arm = False
        self._double_button = None
        self._quantize_button = None
        self._clip_creator = None
        self._quantize_component = None
        super(SpecialClipSlotComponent, self).__init__(*a, **k)
        return

    def disconnect(self):
        super(SpecialClipSlotComponent, self).disconnect()
        self._double_button = None
        self._quantize_button = None
        self._clip_creator = None
        self._quantize_component = None
        return

    def setup_group_clip_blocking(self, setup):
        """ Sets up methods that will block group clips from being launched and also to
        use a different LED color for group clips. """
        if setup:
            self._do_launch_clip = self._blocking_do_launch_clip
            self._feedback_value = self._blocking_feedback_value
            self.update()

    def set_clip_creator(self, creator):
        """ Sets the component that provides fixed_length_enabled and
        fixed_clip_length properties. """
        self._clip_creator = creator

    def set_quantize_component(self, comp):
        """ Sets the component that provides a quantize_clip(clip) method. """
        self._quantize_component = comp

    def set_launch_button(self, button, should_arm=False):
        """ Extends standard to add param to determine if the launch button should
        arm the track to commence recording. """
        self._should_arm = should_arm
        super(SpecialClipSlotComponent, self).set_launch_button(button)

    def set_double_button(self, button):
        """ Sets the button to use to modify the launch button to double the clip. """
        self._double_button = button

    def set_quantize_button(self, button):
        """ Sets the button to use to modify the launch button to quantize the clip. """
        self._quantize_button = button

    @subject_slot('value')
    def _launch_button_value(self, value):
        """ Overrides standard to deal with new modifiers and handle new
        functionality. """
        if self.is_enabled():
            if is_button_pressed(self._select_button) and value:
                self._do_select_clip(self._clip_slot)
            elif self._clip_slot is not None:
                if is_button_pressed(self._delete_button):
                    if value:
                        self._do_delete_clip()
                elif is_button_pressed(self._duplicate_button):
                    if value:
                        self._do_duplicate_clip()
                elif is_button_pressed(self._double_button):
                    if value:
                        self._do_double_clip()
                elif is_button_pressed(self._quantize_button):
                    if value:
                        self._do_quantize_clip()
                else:
                    if self._should_arm:
                        if value:
                            self._do_track_arm()
                            if self._can_do_fixed_length_recording():
                                self._do_fixed_length_recording()
                                return
                    elif value and self._can_do_fixed_length_recording():
                        self._do_fixed_length_recording()
                        return
                    self._do_launch_clip(value)
        return

    def _can_do_fixed_length_recording(self):
        """ Returns whether or not fixed length recording is possible. """
        if not self._clip_slot.has_clip and self._clip_creator and self._clip_creator.fixed_length_enabled:
            parent = self._clip_slot.canonical_parent
            if parent.can_be_armed and (self._should_arm or parent.arm):
                return True
        return False

    def _do_fixed_length_recording(self):
        """ Commences fixed length recording in the slot. """
        self._clip_slot.fire(record_length=self._clip_creator.fixed_length)

    def _do_select_clip(self, clip_slot, display=True):
        """ Extends standard to show name of selected slot/clip. """
        super(SpecialClipSlotComponent, self)._do_select_clip(clip_slot)
        if display:
            name = 'none'
            if self._clip_slot:
                name = get_name(self._clip_slot.clip) if self._clip_slot.has_clip else 'empty slot'
            self.component_message('Clip Selection', name)

    def _do_delete_clip(self):
        """ Overrides standard to use compliant method and messaging. """
        if self._clip_slot.has_clip:
            delete_clip(self._clip_slot, self.component_message)

    def _do_duplicate_clip(self):
        """ Duplicate the clip if one exists. """
        if self._clip_slot.has_clip:
            duplicate_clip(self.song(), self._clip_slot.clip, show_message=self.component_message)

    def _do_double_clip(self):
        """ Doubles the clip if one exists. """
        if self._clip_slot.has_clip:
            self._do_select_clip(self._clip_slot, False)
            double_clip(self._clip_slot.clip, self.component_message)

    def _do_quantize_clip(self):
        """ Quantizes the clip if one exists. """
        clip = self._clip_slot.clip
        if clip and self._quantize_component:
            self._quantize_component.quantize_clip(clip)

    def _do_track_arm(self):
        """ Arms the given track (with exclusive arm handling) and turns on session
        record if a clip already exists in the slot (for overdubbing). """
        track = self._clip_slot.canonical_parent
        if track.can_be_armed and not track.arm:
            if self.song().exclusive_arm:
                for t in self.song().tracks:
                    if t.can_be_armed and t.arm:
                        t.arm = False

            track.arm = True
            if self.song().view.selected_track != track:
                self.song().view.selected_track = track
        if self._clip_slot.has_clip:
            self.song().session_record = True
        if self.song().select_on_launch:
            self._do_select_clip(self._clip_slot, False)

    def _blocking_do_launch_clip(self, value):
        """ Patches standard to block launching group clips if elected. """
        if self._clip_slot.canonical_parent.is_foldable:
            return
        super(SpecialClipSlotComponent, self)._do_launch_clip(value)

    def _blocking_feedback_value(self):
        """ Patches standard to use different LED color for group clips if elected. """
        if live_object_is_valid(self._clip_slot):
            if self._clip_slot.canonical_parent.is_foldable:
                return 'Session.BlockedGroupClip'
            return super(SpecialClipSlotComponent, self)._feedback_value()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialClipSlotComponent.pyc
