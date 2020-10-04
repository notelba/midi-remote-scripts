# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\session.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from KeyLab_Essential.session import SceneComponent as SceneComponentBase, SessionComponent as SessionComponentBase
from .clip_slot import ClipSlotComponent

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent


class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_mkII/session.pyc
