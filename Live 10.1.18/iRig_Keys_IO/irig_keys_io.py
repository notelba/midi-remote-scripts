# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\irig_keys_io.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.control_surface import ControlSurface, Layer, MIDI_CC_TYPE, MIDI_NOTE_TYPE
from ableton.v2.control_surface.components import TransportComponent
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
from .mixer import MixerComponent
from .session_recording import SessionRecordingComponent
from .session_ring import SelectedTrackFollowingSessionRingComponent
from .skin import skin
PAD_IDS = (36, 38, 40, 42, 46, 43, 47, 49)
PAD_CHANNEL = 9

class IRigKeysIO(ControlSurface):

    def __init__(self, *a, **k):
        super(IRigKeysIO, self).__init__(*a, **k)
        with self.component_guard():
            self._create_controls()
            self._create_mixer()
            self._create_transport()

    def _create_controls(self):
        self._encoders = ButtonMatrixElement(rows=[
         [ EncoderElement(MIDI_CC_TYPE, 0, identifier, map_mode=Live.MidiMap.MapMode.absolute, name=(b'Volume_Encoder_{}').format(index)) for index, identifier in enumerate(xrange(12, 20))
         ]], name=b'Volume_Encoders')
        self._data_encoder = EncoderElement(MIDI_CC_TYPE, 0, 22, map_mode=Live.MidiMap.MapMode.relative_smooth_two_compliment, name=b'Data_Encoder')
        self._data_encoder_button = ButtonElement(True, MIDI_CC_TYPE, 0, 23, name=b'Data_Encoder_Button', skin=skin)
        self._play_button = ButtonElement(False, MIDI_CC_TYPE, 0, 118, name=b'Play_Button', skin=skin)
        self._record_button = ButtonElement(False, MIDI_CC_TYPE, 0, 119, name=b'Record_Button', skin=skin)
        self._record_stop_button = ButtonElement(False, MIDI_CC_TYPE, 0, 116, name=b'Record_Stop_Button', skin=skin)
        self._stop_button = ButtonElement(False, MIDI_CC_TYPE, 0, 117, name=b'Stop_Button', skin=skin)
        self._pads = ButtonMatrixElement(rows=[
         [ ButtonElement(True, MIDI_NOTE_TYPE, PAD_CHANNEL, identifier, name=(b'Pad_{}').format(index), skin=skin) for index, identifier in enumerate(PAD_IDS)
         ]])

    def _create_mixer(self):
        self._session_ring = SelectedTrackFollowingSessionRingComponent(is_enabled=False, num_tracks=self._encoders.width(), num_scenes=self._encoders.height(), name=b'Session_Ring')
        self._mixer = MixerComponent(tracks_provider=self._session_ring, name=b'Mixer')
        self._mixer.layer = Layer(volume_controls=self._encoders, track_scroll_encoder=self._data_encoder, selected_track_arm_button=self._data_encoder_button, mute_buttons=self._pads)

    def _create_transport(self):
        self._transport = TransportComponent(name=b'Transport')
        self._transport.layer = Layer(play_button=self._play_button, stop_button=self._stop_button)
        self._session_recording = SessionRecordingComponent(name=b'Session_Recording')
        self._session_recording.layer = Layer(record_button=self._record_button, record_stop_button=self._record_stop_button)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/iRig_Keys_IO/irig_keys_io.pyc
