# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\session.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase, SceneComponent as SceneComponentBase, SessionComponent as SessionComponentBase
from .colors import LIVE_COLOR_INDEX_TO_RGB

class ClipSlotComponent(ClipSlotComponentBase):

    def _color_value(self, slot_or_clip):
        return LIVE_COLOR_INDEX_TO_RGB.get(slot_or_clip.color_index, 0)


class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent

    def _color_value(self, color):
        if liveobj_valid(self._scene):
            return LIVE_COLOR_INDEX_TO_RGB.get(self._scene.color_index, 0)
        return 0


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/session.pyc
