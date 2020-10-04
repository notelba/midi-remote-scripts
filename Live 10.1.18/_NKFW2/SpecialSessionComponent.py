# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialSessionComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.SessionComponent import SessionComponent, product
from SpecialSceneComponent import SpecialSceneComponent
from ModifierMixin import ModifierMixin
from ControlUtils import skin_scroll_component, kill_scroll_tasks

class SpecialSessionComponent(SessionComponent, ModifierMixin):
    """ SpecialSessionComponent extends standard to utilize SpecialSceneComponent, add
    extra skin handling and provide convenience method for setting modifiers for
    sub-components. """
    scene_component_type = SpecialSceneComponent

    def __init__(self, num_tracks, num_scenes, handle_modifier_leds=True, *a, **k):
        super(SpecialSessionComponent, self).__init__(num_tracks, num_scenes, auto_name=True, enable_skinning=True, handle_modifier_leds=handle_modifier_leds, *a, **k)
        self._num_scenes = num_scenes
        self._original_num_scenes = num_scenes
        self._original_num_tracks = num_tracks
        skin_scroll_component(self._vertical_banking, color='Navigation.SessionEnabled')
        skin_scroll_component(self._horizontal_banking, color='Navigation.SessionEnabled')
        skin_scroll_component(self._vertical_paginator, color='Navigation.SessionEnabled')
        skin_scroll_component(self._horizontal_paginator, color='Navigation.SessionEnabled')

    def height(self):
        """ Overrides standard to return the num_scenes, which is changeable. """
        return self._num_scenes

    def set_mixer(self, mixer):
        """ Extends standard to update highlight when mixer is set so returns will be
        included in the highlight if the mixer controls returns. """
        super(SpecialSessionComponent, self).set_mixer(mixer)
        self._do_show_highlight()

    def setup_group_clip_blocking(self, setup):
        """ Sets whether group clips should not be launchable and should use a different
        LED color. """
        for s in xrange(self._original_num_scenes):
            scene = self.scene(s)
            for c in xrange(self._original_num_tracks):
                scene.clip_slot(c).setup_group_clip_blocking(setup)

    def set_clip_creator(self, creator):
        """ Sets the component that provides fixed_length_enabled and
        fixed_clip_length properties. """
        for s in xrange(self._original_num_scenes):
            scene = self.scene(s)
            for c in xrange(self._original_num_tracks):
                scene.clip_slot(c).set_clip_creator(creator)

    def set_quantize_component(self, comp):
        """ Sets the component that provides a quantize_clip(clip) method. """
        for s in xrange(self._original_num_scenes):
            scene = self.scene(s)
            for c in xrange(self._original_num_tracks):
                scene.clip_slot(c).set_quantize_component(comp)

    def set_physical_display_element(self, element):
        """ Sets the display element to use for clip slot and scene components. """
        for s in xrange(self._original_num_scenes):
            scene = self.scene(s)
            scene.set_physical_display_element(element)
            for c in xrange(self._original_num_tracks):
                scene.clip_slot(c).set_physical_display_element(element)

    def set_clip_launch_buttons(self, buttons):
        """ Overrides standard to allow matricies of different heights to be used. """
        assert not buttons or buttons.width() == self._num_tracks
        if buttons:
            buttons.reset()
            for button, (x, y) in buttons.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(button)

            if buttons.height() != self._num_scenes:
                self._num_scenes = buttons.height()
                self._do_show_highlight()
                self.notify_offset()
        else:
            for x, y in product(xrange(self._original_num_tracks), xrange(self._original_num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(None)

        return

    def set_arming_clip_launch_buttons(self, buttons):
        """ Sets launch buttons that will arm tracks in addition to launching their
        respective slot. """
        assert not buttons or buttons.width() == self._num_tracks
        if buttons:
            buttons.reset()
            for button, (x, y) in buttons.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(button, should_arm=True)

            if buttons.height() != self._num_scenes:
                self._num_scenes = buttons.height()
                self._do_show_highlight()
                self.notify_offset()
        else:
            for x, y in product(xrange(self._original_num_tracks), xrange(self._original_num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(None)

        return

    def set_scene_launch_buttons(self, buttons):
        """ Overrides standard which had incorrect assert. """
        assert not buttons or buttons.height() + buttons.width() <= self._original_num_scenes + 1
        if buttons:
            use_width = buttons.width() > buttons.height()
            for button, (w, h) in buttons.iterbuttons():
                scene = self.scene(w if use_width else h)
                scene.set_launch_button(button)

        else:
            for x in xrange(self._original_num_scenes):
                scene = self.scene(x)
                scene.set_launch_button(None)

        return

    def set_scene_bank_up_button(self, button):
        """ Overrides standard to kill scroll task on button set. """
        kill_scroll_tasks((self._vertical_banking,))
        self._vertical_banking.set_scroll_up_button(button)

    def set_scene_bank_down_button(self, button):
        """ Overrides standard to kill scroll task on button set. """
        kill_scroll_tasks((self._vertical_banking,))
        self._vertical_banking.set_scroll_down_button(button)

    def set_track_bank_left_button(self, button):
        """ Overrides standard to kill scroll task on button set. """
        kill_scroll_tasks((self._horizontal_banking,))
        self._horizontal_banking.set_scroll_up_button(button)

    def set_track_bank_right_button(self, button):
        """ Overrides standard to kill scroll task on button set. """
        kill_scroll_tasks((self._horizontal_banking,))
        self._horizontal_banking.set_scroll_down_button(button)

    def _set_modifier(self, button, modifier_name):
        """ Extends standard to set up modifiers for sub-components. """
        set_on_scene = modifier_name not in ('double', 'quantize')
        for scene_index in xrange(self._original_num_scenes):
            scene = self.scene(scene_index)
            if set_on_scene:
                getattr(scene, 'set_%s_button' % modifier_name)(button)
            for track_index in xrange(self._original_num_tracks):
                slot = scene.clip_slot(track_index)
                getattr(slot, 'set_%s_button' % modifier_name)(button)

        super(SpecialSessionComponent, self)._set_modifier(button, modifier_name)

    def update(self):
        super(SpecialSessionComponent, self).update()
        self.update_modifier_leds()

    def _update_stop_all_clips_button(self):
        """ Overrides standard to handle skin settings. """
        if self.is_enabled():
            button = self._stop_all_button
            if button:
                button.set_light('Session.StopAllPressed' if button.is_pressed() else 'Session.StopAll')

    def _update_stop_clips_led(self, index):
        """ Overrides standard to handle extra skin definition. """
        if self.is_enabled() and self._stop_track_clip_buttons is not None and index < len(self._stop_track_clip_buttons):
            track_index = index + self.track_offset()
            tracks_to_use = self.tracks_to_use()
            button = self._stop_track_clip_buttons[index]
            if button:
                value_to_send = None
                if track_index < len(tracks_to_use) and tracks_to_use[track_index].clip_slots:
                    if tracks_to_use[track_index].fired_slot_index == -2:
                        value_to_send = 'Session.StopClipTriggered'
                    elif tracks_to_use[track_index].playing_slot_index >= 0:
                        value_to_send = 'Session.StopClip'
                    else:
                        value_to_send = 'Session.StoppedClip'
                if value_to_send is None:
                    button.set_light('DefaultButton.Off')
                else:
                    button.set_light(value_to_send)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialSessionComponent.pyc
