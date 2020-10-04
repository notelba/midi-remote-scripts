# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Code_Series\code.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, inject
from ableton.v2.control_surface import ControlSurface, Layer
from ableton.v2.control_surface.components import MixerComponent, SessionRingComponent, TransportComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement
from .element_utils import make_button, make_encoder, make_slider
from .mixer_navigation import MixerNavigationComponent
from .skin_default import make_default_skin

class Code(ControlSurface):
    mixer_navigation_type = MixerNavigationComponent

    def __init__(self, *a, **k):
        super(Code, self).__init__(*a, **k)
        with self.component_guard():
            with inject(skin=const(make_default_skin())).everywhere():
                self._create_controls()
            self._create_transport()
            self._create_mixer()
            self._create_mixer_navigation()

    def _create_controls(self):
        self._rw_button = make_button(91, b'RW_Button')
        self._ff_button = make_button(92, b'FF_Button')
        self._stop_button = make_button(93, b'Stop_Button')
        self._play_button = make_button(94, b'Play_Button')
        self._record_button = make_button(95, b'Record_Button')
        self._faders = ButtonMatrixElement(rows=[[ make_slider(index, b'Fader_%d' % (index + 1,)) for index in xrange(8) ]], name=b'Faders')
        self._master_fader = make_slider(8, b'Master_Fader')
        self._encoders = ButtonMatrixElement(rows=[
         [ make_encoder(index + 16, b'Encoder_%d' % (index + 1,)) for index in xrange(8)
         ]], name=b'Encoders')
        self._track_select_buttons = ButtonMatrixElement(rows=[
         [ make_button(index + 24, b'Track_Select_Button_%d' % (index + 1,)) for index in xrange(8)
         ]], name=b'Track_Select_Buttons')
        self._mute_buttons = ButtonMatrixElement(rows=[
         [ make_button(index + 8, b'Mute_Button_%d' % (index + 1,)) for index in xrange(8)
         ]], name=b'Mute_Buttons')
        self._solo_buttons = ButtonMatrixElement(rows=[
         [ make_button(index + 16, b'Solo_Button_%d' % (index + 1,)) for index in xrange(8)
         ]], name=b'Solo_Buttons')
        self._arm_buttons = ButtonMatrixElement(rows=[
         [ make_button(index, b'Record_Arm_Button_%d' % (index + 1,)) for index in xrange(8)
         ]], name=b'Record_Arm_Buttons')
        self._bank_up_button = make_button(47, b'Bank_Up_Button')
        self._bank_down_button = make_button(46, b'Bank_Down_Button')

    def _create_transport(self):
        self._transport = TransportComponent(name=b'Transport', is_enabled=False, layer=Layer(seek_forward_button=self._ff_button, seek_backward_button=self._rw_button, stop_button=self._stop_button, play_button=self._play_button, record_button=self._record_button))
        self._transport.set_enabled(True)

    def _create_mixer(self):
        self._session_ring = SessionRingComponent(name=b'Session_Navigation', num_tracks=8, num_scenes=0, is_enabled=False)
        self._mixer = MixerComponent(name=b'Mixer', is_enabled=False, tracks_provider=self._session_ring, invert_mute_feedback=True, layer=Layer(volume_controls=self._faders, pan_controls=self._encoders, track_select_buttons=self._track_select_buttons, solo_buttons=self._solo_buttons, mute_buttons=self._mute_buttons, arm_buttons=self._arm_buttons))
        self._mixer.master_strip().layer = Layer(volume_control=self._master_fader)
        self._mixer.set_enabled(True)

    def _create_mixer_navigation(self):
        self._mixer_navigation = self.mixer_navigation_type(name=b'Mixer_Navigation', is_enabled=False, session_ring=self._session_ring, layer=Layer(page_left_button=self._bank_down_button, page_right_button=self._bank_up_button))
        self._mixer_navigation.set_enabled(True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Code_Series/code.pyc
