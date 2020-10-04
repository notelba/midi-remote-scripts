# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_FA\fa.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import const, inject
from ableton.v2.control_surface import ControlSurface, Layer, MIDI_NOTE_TYPE
from ableton.v2.control_surface.components import DrumGroupComponent, MixerComponent, SessionRecordingComponent, SessionRingComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement
from ableton.v2.control_surface.mode import LayerMode, ModesComponent
from .control_element_utils import make_button, make_encoder
from .navigation import SessionNavigationComponent
from .skin import make_default_skin
from .transport import TransportComponent

class FA(ControlSurface):

    def __init__(self, *a, **k):
        super(FA, self).__init__(*a, **k)
        with self.component_guard():
            with inject(skin=const(make_default_skin())).everywhere():
                self._create_controls()
            self._create_transport()
            self._create_session_recording()
            self._create_mixer()
            self._create_navigation()
            self._create_modes()
            self._create_drums()

    def _create_controls(self):
        self._jump_to_start_button = make_button(21, b'Jump_To_Start_Button')
        self._rwd_button = make_button(22, b'RWD_Button')
        self._ff_button = make_button(23, b'FF_Button')
        self._stop_button = make_button(25, b'Stop_Button')
        self._play_button = make_button(26, b'Play_Button')
        self._record_button = make_button(28, b'Record_Button')
        self._encoders = ButtonMatrixElement(rows=[[ make_encoder(index + 70, b'Encoder_%d' % (index,)) for index in xrange(6) ]], name=b'Encoders')
        self._volume_mode_button = make_button(16, b'Volume_Mode_Button')
        self._pan_mode_button = make_button(17, b'Pan_Mode_Button')
        self._send_a_mode_button = make_button(18, b'Send_A_Mode_Button')
        self._send_b_mode_button = make_button(19, b'Send_B_Mode_Button')
        self._s1_button = make_button(14, b'S1_Button')
        self._s2_button = make_button(15, b'S2_Button')
        self._pads = ButtonMatrixElement(rows=[ [ make_button(col_index + offset, b'Pad_%d_%d' % (col_index, row_index), msg_type=MIDI_NOTE_TYPE) for col_index in xrange(4) ] for row_index, offset in enumerate(xrange(72, 59, -4))
                                              ], name=b'Pads')

    def _create_transport(self):
        self._transport = TransportComponent(name=b'Transport', is_enabled=False, layer=Layer(play_button=self._play_button, stop_button=self._stop_button, seek_backward_button=self._rwd_button, seek_forward_button=self._ff_button, jump_to_start_button=self._jump_to_start_button))
        self._transport.set_enabled(True)

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(name=b'Session_Recording', is_enabled=False, layer=Layer(record_button=self._record_button))
        self._session_recording.set_enabled(True)

    def _create_mixer(self):
        self._session_ring = SessionRingComponent(num_tracks=self._encoders.width(), num_scenes=0, is_enabled=False, name=b'Session_Ring')
        self._mixer = MixerComponent(tracks_provider=self._session_ring, name=b'Mixer')

    def _create_navigation(self):
        self._navigation = SessionNavigationComponent(session_ring=self._session_ring, name=b'Navigation', is_enabled=False, layer=Layer(page_left_button=self._s1_button, page_right_button=self._s2_button))
        self._navigation.set_enabled(True)

    def _create_modes(self):
        self._modes = ModesComponent(name=b'Encoder_Modes')
        self._modes.add_mode(b'volume_mode', LayerMode(self._mixer, Layer(volume_controls=self._encoders)))
        self._modes.add_mode(b'pan_mode', LayerMode(self._mixer, Layer(pan_controls=self._encoders)))
        self._modes.add_mode(b'send_a_mode', [
         LayerMode(self._mixer, Layer(send_controls=self._encoders)),
         partial(self._set_send_index, 0)])
        self._modes.add_mode(b'send_b_mode', [
         LayerMode(self._mixer, Layer(send_controls=self._encoders)),
         partial(self._set_send_index, 1)])
        self._modes.layer = Layer(volume_mode_button=self._volume_mode_button, pan_mode_button=self._pan_mode_button, send_a_mode_button=self._send_a_mode_button, send_b_mode_button=self._send_b_mode_button)
        self._modes.selected_mode = b'volume_mode'

    def _set_send_index(self, index):
        self._mixer.send_index = index if index < self._mixer.num_sends else None
        return

    def _create_drums(self):
        self._drums = DrumGroupComponent(name=b'Drum_Group', is_enabled=False, translation_channel=0, layer=Layer(matrix=self._pads))
        self._drums.set_enabled(True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Roland_FA/fa.pyc
