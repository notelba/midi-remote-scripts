# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_mini\APC_mini.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
from APC_Key_25.APC_Key_25 import APC_Key_25

class APC_mini(APC_Key_25):
    SESSION_HEIGHT = 8
    HAS_TRANSPORT = False

    def __init__(self, *a, **k):
        super(APC_mini, self).__init__(*a, **k)
        with self.component_guard():
            self.register_disconnectable(SimpleLayerOwner(layer=Layer(_unused_buttons=self.wrap_matrix(self._unused_buttons))))

    def _make_stop_all_button(self):
        return self.make_shifted_button(self._scene_launch_buttons[7])

    def _create_controls(self):
        super(APC_mini, self)._create_controls()
        self._unused_buttons = map(self.make_shifted_button, self._scene_launch_buttons[5:7])
        self._master_volume_control = make_slider(0, 56, name=b'Master_Volume')

    def _create_mixer(self):
        mixer = super(APC_mini, self)._create_mixer()
        mixer.master_strip().layer = Layer(volume_control=self._master_volume_control)
        return mixer

    def _product_model_id_byte(self):
        return 40
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC_mini/APC_mini.pyc
