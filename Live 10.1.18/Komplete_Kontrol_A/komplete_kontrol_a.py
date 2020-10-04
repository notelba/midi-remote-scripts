# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_A\komplete_kontrol_a.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Komplete_Kontrol.komplete_kontrol_base import KompleteKontrolBase, Layer, create_button, create_encoder
from .view_control_component import ViewControlComponent

class Komplete_Kontrol_A(KompleteKontrolBase):

    def _create_controls(self):
        super(Komplete_Kontrol_A, self)._create_controls()
        self._mute_button = create_button(67, b'Mute_Button')
        self._solo_button = create_button(68, b'Solo_Button')
        self._vertical_encoder = create_encoder(48, b'Vertical_Encoder')
        self._horizontal_encoder = create_encoder(50, b'Horizontal_Encoder')

    def _create_components(self):
        super(Komplete_Kontrol_A, self)._create_components()
        self._create_view_control()

    def _create_view_control(self):
        self._view_control = ViewControlComponent(name=b'View_Control', is_enabled=False, layer=Layer(vertical_encoder=self._vertical_encoder, horizontal_encoder=self._horizontal_encoder))

    def _create_mixer_component_layer(self):
        return super(Komplete_Kontrol_A, self)._create_mixer_component_layer() + Layer(mute_button=self._mute_button, solo_button=self._solo_button)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Komplete_Kontrol_A/komplete_kontrol_a.pyc
