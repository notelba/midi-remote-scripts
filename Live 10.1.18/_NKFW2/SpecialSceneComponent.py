# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SpecialSceneComponent.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.SceneComponent import SceneComponent
from _Framework.SubjectSlot import subject_slot
from SpecialClipSlotComponent import SpecialClipSlotComponent
from ShowMessageMixin import ShowMessageMixin
from ControlUtils import is_button_pressed
from Utils import get_name

class SpecialSceneComponent(SceneComponent, ShowMessageMixin):
    """ SpecialSceneComponent extends standard to add duplicate modifier and utilize
    SpecialClipSlotComponent. """
    clip_slot_component_type = SpecialClipSlotComponent

    def __init__(self, *a, **k):
        self._duplicate_button = None
        super(SpecialSceneComponent, self).__init__(*a, **k)
        return

    def disconnect(self):
        super(SpecialSceneComponent, self).disconnect()
        self._duplicate_button = None
        return

    def set_duplicate_button(self, button):
        """ Sets the button to use to modify the launch button to duplicate the scene. """
        self._duplicate_button = button

    def set_launch_button(self, button):
        """ Extends standard to call LED update method regardless of whether the
        button being set is the same as the current button. """
        super(SpecialSceneComponent, self).set_launch_button(button)
        self._update_launch_button()

    @subject_slot('value')
    def _launch_value(self, value):
        """ Overrides standard to deal with new modifier. """
        if self.is_enabled():
            if is_button_pressed(self._select_button) and value:
                self._do_select_scene(self._scene)
            elif self._scene is not None:
                if is_button_pressed(self._delete_button):
                    if value:
                        self._do_delete_scene(self._scene)
                elif is_button_pressed(self._duplicate_button):
                    if value:
                        self._do_duplicate_scene()
                else:
                    self._do_launch_scene(value)
        return

    def _do_select_scene(self, scene):
        """ Extends standard to show name of selected scene. """
        super(SpecialSceneComponent, self)._do_select_scene(scene)
        self.component_message('Scene Selection', get_name(self._scene) if self._scene else 'none')

    def _do_delete_scene(self, scene):
        """ Extends standard to show delete message. """
        if scene:
            self.component_message('Scene Deleted', get_name(scene))
        super(SpecialSceneComponent, self)._do_delete_scene(scene)

    def _do_duplicate_scene(self):
        """ Attempts to duplicate the scene. """
        try:
            song = self.song()
            song.duplicate_scene(list(song.scenes).index(self._scene))
            self.component_message('Scene Duplicated', get_name(self._scene))
        except:
            pass
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SpecialSceneComponent.pyc
