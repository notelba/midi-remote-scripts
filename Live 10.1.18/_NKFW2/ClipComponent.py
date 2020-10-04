# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ClipComponent.py
# Compiled at: 2017-09-30 15:26:22
import Live
LSQ = Live.Song.Quantization
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from _Framework.Control import ButtonControl
from ShowMessageMixin import ShowMessageMixin
from PlayingOrSelectedClipMixin import PlayingOrSelectedClipMixin
from ClipUtils import delete_clip, double_clip, duplicate_clip
from ControlUtils import is_button_pressed
from Utils import live_object_is_valid

class ClipComponent(CompoundComponent, ShowMessageMixin):
    """ ClipComponent is the base class for a component that controls a clip.  This is a
    CompoundComponent for flexibility when sub-classed. This module includes
    TrackClipComponent, which applies to the playing or selected clip on a track.  """
    delete_button = ButtonControl(disabled_color='Clip.NoClip', color='Clip.DeleteActive', pressed_color='Modifiers.Pressed', enabled=False)
    double_button = ButtonControl(disabled_color='Clip.NoClip', color='Clip.DoubleActive', pressed_color='Modifiers.Pressed', enabled=False)
    duplicate_button = ButtonControl(disabled_color='Clip.NoClip', color='Clip.DuplicateActive', pressed_color='Modifiers.Pressed', enabled=False)
    quantize_button = ButtonControl(disabled_color='Clip.NoClip', color='Clip.QuantizeActive', pressed_color='Modifiers.Pressed', enabled=False)

    def __init__(self, zoom_loop=True, qntz_comp=None, target_clip_comp=None, *a, **k):
        super(ClipComponent, self).__init__(*a, **k)
        self._zoom_loop_on_edit = bool(zoom_loop)
        self._quantize_component = qntz_comp
        self._clip = None
        self._shift_button = None
        self._on_target_clip_changed.subject = target_clip_comp
        return

    def disconnect(self):
        super(ClipComponent, self).disconnect()
        self._quantize_component = None
        self._clip = None
        self._shift_button = None
        return

    @property
    def clip(self):
        """ The clip that is being controlled. """
        return self._clip

    def set_loop_button(self, button):
        """ Sets the button to use for toggling/resetting the clip's loop. """
        self._on_loop_button_value.subject = button if button else None
        self._on_looping_status_changed()
        return

    def set_play_toggle_button(self, button):
        """ Sets the button to use for stopping/launching the clip with or without
        quantization/legato. """
        self._on_play_toggle_button.subject = button if button else None
        self._on_playing_status_changed()
        return

    def set_shift_button(self, button):
        """ Sets the shift modifier to use. """
        self._shift_button = button

    @subject_slot('target_clip')
    def _on_target_clip_changed(self, clip):
        self.set_clip(clip)

    def set_clip(self, clip):
        """ Sets the clip for the component to control, adds listeners and calls
        on_clip_changed, which sub-classes should override. """
        assert clip is None or isinstance(clip, Live.Clip.Clip)
        if clip != self._clip or not live_object_is_valid(self._clip):
            self._clip = clip
            self._on_looping_status_changed.subject = self._clip
            self._on_playing_status_changed.subject = self._clip
            self.on_clip_name_changed.subject = self._clip
            self.on_clip_changed()
            self.on_clip_name_changed()
            self._on_looping_status_changed()
            self._on_playing_status_changed()
            self._update_delete_button()
            self._update_double_button()
            self._update_duplicate_button()
            self._update_quantize_button()
        return

    def update(self):
        super(ClipComponent, self).update()
        self._on_looping_status_changed()
        self._on_playing_status_changed()
        self.on_clip_name_changed()
        self._update_delete_button()
        self._update_double_button()
        self._update_duplicate_button()
        self._update_quantize_button()

    def on_clip_changed(self):
        """ Called when the clip this component is assigned to changes.
        To be overridden. """
        pass

    @subject_slot('name')
    def on_clip_name_changed(self):
        """ Called when the name of the clip assigned to this component changes.
        To be overridden. """
        pass

    @subject_slot('value')
    def _on_loop_button_value(self, value):
        """ Toggles/resets the clip's loop. """
        if self.is_enabled() and self._clip and value:
            if is_button_pressed(self._shift_button) and self._clip.looping:
                self._clip.loop_start = 0.0
                self._clip.loop_end = self._clip.end_marker
            else:
                self._clip.looping = not self._clip.looping
            if self._zoom_loop_on_edit:
                self._clip.view.show_loop()
                self._clip.view.show_loop()

    @subject_slot('value')
    def _on_play_toggle_button(self, value):
        """ If Clip is playing and not triggered to stop, this will stop it with or
        without quantization depending on whether shift is pressed. Otherwise, this will
        launch the clip with or without quantization/legato depending on whether shift
        is pressed. """
        if self.is_enabled() and self.is_session_clip and value:
            track = self._clip.canonical_parent.canonical_parent
            if track.fired_slot_index != -2 and (self._clip.is_playing or self._clip.is_triggered or self._clip.is_recording):
                track.stop_all_clips(not is_button_pressed(self._shift_button))
            elif is_button_pressed(self._shift_button):
                self._clip.canonical_parent.fire(force_legato=True, launch_quantization=LSQ)
            else:
                self._clip.fire()

    @delete_button.pressed
    def delete_button(self, _):
        if self._clip:
            delete_clip(self._clip.canonical_parent, self.component_message)

    @double_button.pressed
    def double_button(self, _):
        double_clip(self._clip, self.component_message)

    @duplicate_button.pressed
    def duplicate_button(self, _):
        duplicate_clip(self.song(), self._clip, show_message=self.component_message)

    @quantize_button.pressed
    def quantize_button(self, _):
        if self._quantize_component:
            self._quantize_component.quantize_clip(self._clip)

    @subject_slot('looping')
    def _on_looping_status_changed(self):
        """ Updates loop button LED on looping status changed. """
        if self.is_enabled():
            button = self._on_loop_button_value.subject
            if button:
                status = 'Clip.NoClip'
                if self._clip:
                    status = 'Clip.Loop.On' if self._clip.looping else 'Clip.Loop.Off'
                button.set_light(status)

    @subject_slot('playing_status')
    def _on_playing_status_changed(self):
        """ Updates stop button LED on playing status changed. """
        if self.is_enabled():
            button = self._on_play_toggle_button.subject
            if button:
                status = 'Clip.NoClip'
                if self.is_session_clip():
                    status = 'Clip.StopActive' if self._clip.is_playing or self._clip.is_triggered or self._clip.is_recording else 'Clip.StopInactive'
                button.set_light(status)

    def _update_delete_button(self):
        self.delete_button.enabled = self.is_enabled() and self.is_session_clip()

    def _update_double_button(self):
        self.double_button.enabled = self.is_enabled() and self._clip is not None and self._clip.is_midi_clip
        return

    def _update_duplicate_button(self):
        self.duplicate_button.enabled = self.is_enabled() and self._clip is not None
        return

    def _update_quantize_button(self):
        self.quantize_button.enabled = self.is_enabled() and self._clip is not None
        return

    def is_session_clip(self):
        """ Returns whether the current clip (if there is one) is a clip in session. """
        return self._clip is not None and not self._clip.is_arrangement_clip


class TrackClipComponent(PlayingOrSelectedClipMixin, ClipComponent):
    """ TrackClipComponent is the base class for a ClipComponent that controls the
    playing or selected clip on a track. """

    def __init__(self, qntz_comp=None, targets_comp=None, name='Clip_Control', is_private=False, *a, **k):
        super(TrackClipComponent, self).__init__(zoom_loop=False, qntz_comp=qntz_comp, name=name, targets_comp=targets_comp, *a, **k)
        self.is_private = bool(is_private)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ClipComponent.pyc
