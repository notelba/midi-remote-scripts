# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40\SessionComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import ButtonControl
from _APC.SessionComponent import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):
    """ Special SessionComponent with a button (pedal) to fire the selected clip slot """
    slot_launch_button = ButtonControl()
    selected_scene_launch_button = ButtonControl()

    def set_slot_launch_button(self, button):
        self.slot_launch_button.set_control_element(button)

    @slot_launch_button.pressed
    def slot_launch_button(self, button):
        clip_slot = self.song().view.highlighted_clip_slot
        if clip_slot:
            clip_slot.fire()

    def set_selected_scene_launch_button(self, button):
        self.selected_scene_launch_button.set_control_element(button)

    @selected_scene_launch_button.pressed
    def selected_scene_launch_button(self, button):
        scene = self.song().view.selected_scene
        if scene:
            scene.fire()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC40/SessionComponent.pyc
