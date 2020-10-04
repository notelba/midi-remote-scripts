# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\configurable_playable.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import PlayableComponent

class ConfigurablePlayableComponent(PlayableComponent):

    def __init__(self, translation_channel, *a, **k):
        self._translation_channel = translation_channel
        super(ConfigurablePlayableComponent, self).__init__(*a, **k)

    def _note_translation_for_button(self, button):
        return (
         button.identifier, self._translation_channel)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/configurable_playable.pyc
