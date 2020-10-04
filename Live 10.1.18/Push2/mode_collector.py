# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\mode_collector.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listenable_property, listens, EventObject

class ModeCollector(EventObject):

    def __init__(self, main_modes=None, mix_modes=None, global_mix_modes=None, device_modes=None, *a, **k):
        super(ModeCollector, self).__init__(*a, **k)
        self._main_modes = main_modes
        self._mix_modes = mix_modes
        self._global_mix_modes = global_mix_modes
        self._device_modes = device_modes
        self._on_selected_main_mode_changed.subject = main_modes
        self._on_selected_mix_mode_changed.subject = mix_modes
        self._on_selected_global_mix_mode_changed.subject = global_mix_modes
        self._on_selected_device_mode_changed.subject = device_modes

    @listenable_property
    def main_mode(self):
        return self._main_modes.selected_mode

    @listens(b'selected_mode')
    def _on_selected_main_mode_changed(self, mode):
        self.notify_main_mode()

    @listenable_property
    def mix_mode(self):
        return self._mix_modes.selected_mode

    @listens(b'selected_mode')
    def _on_selected_mix_mode_changed(self, mode):
        self.notify_mix_mode()

    @listenable_property
    def global_mix_mode(self):
        return self._global_mix_modes.selected_mode

    @listens(b'selected_mode')
    def _on_selected_global_mix_mode_changed(self, mode):
        self.notify_global_mix_mode()

    @listenable_property
    def device_mode(self):
        return self._device_modes.selected_mode

    @listens(b'selected_mode')
    def _on_selected_device_mode_changed(self, mode):
        self.notify_device_mode()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/mode_collector.pyc