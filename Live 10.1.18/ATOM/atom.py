# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\atom.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, inject, listens, liveobj_valid
from ableton.v2.control_surface import ControlSurface, Layer, PercussionInstrumentFinder
from ableton.v2.control_surface.components import ArmedTargetTrackComponent, BackgroundComponent, SessionNavigationComponent, SessionOverviewComponent, SessionRecordingComponent, SessionRingComponent, SimpleTrackAssigner, TransportComponent, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode, ModesComponent, MomentaryBehaviour
from . import midi
from .channel_strip import ChannelStripComponent
from .drum_group import DrumGroupComponent
from .elements import Elements, SESSION_HEIGHT, SESSION_WIDTH
from .keyboard import KeyboardComponent
from .lighting import LightingComponent
from .mixer import MixerComponent
from .session import SessionComponent
from .skin import skin
from .translating_background import TranslatingBackgroundComponent
from .view_toggle import ViewToggleComponent

class ATOM(ControlSurface):

    def __init__(self, *a, **k):
        super(ATOM, self).__init__(*a, **k)
        with self.component_guard():
            with inject(skin=const(skin)).everywhere():
                self._elements = Elements()
        with self.component_guard():
            with inject(element_container=const(self._elements)).everywhere():
                self._create_lighting()
                self._create_transport()
                self._create_record_modes()
                self._create_undo()
                self._create_view_toggle()
                self._create_background()
                self._create_session()
                self._create_mixer()
                self._create_encoder_modes()
                self._create_session_navigation_modes()
                self._create_keyboard()
                self._create_drum_group()
                self._create_note_modes()
                self._create_pad_modes()
                self._create_user_assignments_mode()
                self._target_track = ArmedTargetTrackComponent(name=b'Target_Track')
                self.__on_target_track_changed.subject = self._target_track
        self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=self._target_track.target_track))
        self.__on_drum_group_changed.subject = self._drum_group_finder
        self.__on_drum_group_changed()
        self.__on_main_view_changed.subject = self.application.view

    def disconnect(self):
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)
        super(ATOM, self).disconnect()

    def port_settings_changed(self):
        self._send_midi(midi.NATIVE_MODE_ON_MESSAGE)
        super(ATOM, self).port_settings_changed()

    def _create_lighting(self):
        self._lighting = LightingComponent(name=b'Lighting', is_enabled=False, layer=Layer(shift_button=b'shift_button', zoom_button=b'zoom_button'))
        self._lighting.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name=b'Transport', is_enabled=False, layer=Layer(play_button=b'play_button', loop_button=b'play_button_with_shift', stop_button=b'stop_button', metronome_button=b'click_button'))
        self._transport.set_enabled(True)

    def _create_record_modes(self):
        self._session_record = SessionRecordingComponent(name=b'Session_Record', is_enabled=False, layer=Layer(record_button=b'record_button'))
        self._record_modes = ModesComponent(name=b'Record_Modes')
        self._record_modes.add_mode(b'session', self._session_record)
        self._record_modes.add_mode(b'arrange', AddLayerMode(self._transport, layer=Layer(record_button=b'record_button')))
        self.__on_main_view_changed()

    def _create_undo(self):
        self._undo = UndoRedoComponent(name=b'Undo', is_enabled=False, layer=Layer(undo_button=b'stop_button_with_shift'))
        self._undo.set_enabled(True)

    def _create_view_toggle(self):
        self._view_toggle = ViewToggleComponent(name=b'View_Toggle', is_enabled=False, layer=Layer(detail_view_toggle_button=b'show_hide_button', main_view_toggle_button=b'preset_button'))
        self._view_toggle.set_enabled(True)

    def _create_background(self):
        self._background = BackgroundComponent(name=b'Background', is_enabled=False, add_nop_listeners=True, layer=Layer(set_loop_button=b'set_loop_button', nudge_button=b'nudge_button', bank_button=b'bank_button'))
        self._background.set_enabled(True)

    def _create_session(self):
        self._session_ring = SessionRingComponent(name=b'Session_Ring', num_tracks=SESSION_WIDTH, num_scenes=SESSION_HEIGHT)
        self._session = SessionComponent(name=b'Session', session_ring=self._session_ring)
        self._session_navigation = SessionNavigationComponent(name=b'Session_Navigation', is_enabled=False, session_ring=self._session_ring, layer=Layer(left_button=b'left_button', right_button=b'right_button'))
        self._session_navigation.set_enabled(True)
        self._session_overview = SessionOverviewComponent(name=b'Session_Overview', is_enabled=False, session_ring=self._session_ring, enable_skinning=True, layer=Layer(button_matrix=b'pads_with_zoom'))

    def _create_mixer(self):
        self._mixer = MixerComponent(name=b'Mixer', auto_name=True, tracks_provider=self._session_ring, track_assigner=SimpleTrackAssigner(), invert_mute_feedback=True, channel_strip_component_type=ChannelStripComponent)

    def _create_encoder_modes(self):
        self._encoder_modes = ModesComponent(name=b'Encoder_Modes', enable_skinning=True)
        self._encoder_modes.add_mode(b'volume', AddLayerMode(self._mixer, Layer(volume_controls=b'encoders')))
        self._encoder_modes.add_mode(b'pan', AddLayerMode(self._mixer, Layer(pan_controls=b'encoders')))
        self._encoder_modes.add_mode(b'send_a', AddLayerMode(self._mixer, Layer(send_a_controls=b'encoders')))
        self._encoder_modes.add_mode(b'send_b', AddLayerMode(self._mixer, Layer(send_b_controls=b'encoders')))
        self._encoder_modes.selected_mode = b'volume'

    def _create_session_navigation_modes(self):
        self._session_navigation_modes = ModesComponent(name=b'Session_Navigation_Modes', is_enabled=False, layer=Layer(cycle_mode_button=b'bank_button'))
        self._session_navigation_modes.add_mode(b'default', AddLayerMode(self._session_navigation, layer=Layer(up_button=b'up_button', down_button=b'down_button')), cycle_mode_button_color=b'DefaultButton.Off')
        self._session_navigation_modes.add_mode(b'paged', AddLayerMode(self._session_navigation, layer=Layer(page_up_button=b'up_button', page_down_button=b'down_button', page_left_button=b'left_button', page_right_button=b'right_button')), cycle_mode_button_color=b'DefaultButton.On')
        self._session_navigation_modes.selected_mode = b'default'

    def _create_keyboard(self):
        self._keyboard = KeyboardComponent(midi.KEYBOARD_CHANNEL, name=b'Keyboard', is_enabled=False, layer=Layer(matrix=b'pads', scroll_up_button=b'up_button', scroll_down_button=b'down_button'))

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(name=b'Drum_Group', is_enabled=False, translation_channel=midi.DRUM_CHANNEL, layer=Layer(matrix=b'pads', scroll_page_up_button=b'up_button', scroll_page_down_button=b'down_button'))

    def _create_note_modes(self):
        self._note_modes = ModesComponent(name=b'Note_Modes', is_enabled=False)
        self._note_modes.add_mode(b'keyboard', self._keyboard)
        self._note_modes.add_mode(b'drum', self._drum_group)
        self._note_modes.selected_mode = b'keyboard'

    def _create_pad_modes(self):
        self._pad_modes = ModesComponent(name=b'Pad_Modes', is_enabled=False, layer=Layer(session_button=b'full_level_button', note_button=b'note_repeat_button', channel_button=b'select_button', encoder_modes_button=b'setup_button'))
        self._pad_modes.add_mode(b'session', (
         AddLayerMode(self._background, Layer(unused_pads=b'pads_with_shift')),
         AddLayerMode(self._session, Layer(clip_launch_buttons=b'pads', scene_launch_buttons=self._elements.pads_with_shift.submatrix[
          3:, :])),
         self._session_overview,
         self._session_navigation_modes))
        self._pad_modes.add_mode(b'note', self._note_modes)
        self._pad_modes.add_mode(b'channel', (
         self._elements.pads.reset,
         AddLayerMode(self._mixer, Layer(arm_buttons=self._elements.pads.submatrix[:, :1], solo_buttons=self._elements.pads.submatrix[:, 1:2], track_select_buttons=self._elements.pads.submatrix[:, 2:3])),
         AddLayerMode(self._session, Layer(stop_track_clip_buttons=self._elements.pads.submatrix[:, 3:])),
         self._session_navigation_modes))
        self._pad_modes.add_mode(b'encoder_modes', (
         LayerMode(self._encoder_modes, Layer(volume_button=self._elements.pads_raw[0][0], pan_button=self._elements.pads_raw[0][1], send_a_button=self._elements.pads_raw[0][2], send_b_button=self._elements.pads_raw[0][3])),
         AddLayerMode(self._background, Layer(unused_pads=self._elements.pads.submatrix[:, 1:]))), behaviour=MomentaryBehaviour())
        self._pad_modes.selected_mode = b'session'
        self._pad_modes.set_enabled(True)

    def _create_user_assignments_mode(self):
        self._translating_background = TranslatingBackgroundComponent(midi.USER_CHANNEL, name=b'Translating_Background', is_enabled=False, add_nop_listeners=True, layer=Layer(note_repeat_button=b'note_repeat_button', full_level_button=b'full_level_button', bank_button=b'bank_button', preset_button=b'preset_button', show_hide_button=b'show_hide_button', nudge_button=b'nudge_button', set_loop_button=b'set_loop_button', setup_button=b'setup_button', up_button=b'up_button', down_button=b'down_button', left_button=b'left_button', right_button=b'right_button', select_button=b'select_button', click_button=b'click_button', record_button=b'record_button', play_button=b'play_button', stop_button=b'stop_button', pads=b'pads', encoders=b'encoders'))
        self._top_level_modes = ModesComponent(name=b'Top_Level_Modes', is_enabled=False, support_momentary_mode_cycling=False, layer=Layer(cycle_mode_button=b'editor_button'))
        self._top_level_modes.add_mode(b'default', self.refresh_state, cycle_mode_button_color=b'DefaultButton.Off')
        self._top_level_modes.add_mode(b'user', self._translating_background, cycle_mode_button_color=b'DefaultButton.On')
        self._top_level_modes.selected_mode = b'default'
        self._top_level_modes.set_enabled(True)

    @listens(b'is_view_visible', b'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible(b'Session'):
            self._record_modes.selected_mode = b'session'
        else:
            self._record_modes.selected_mode = b'arrange'

    @listens(b'target_track')
    def __on_target_track_changed(self):
        self._drum_group_finder.device_parent = self._target_track.target_track

    @listens(b'instrument')
    def __on_drum_group_changed(self):
        drum_group = self._drum_group_finder.drum_group
        self._drum_group.set_drum_group_device(drum_group)
        self._note_modes.selected_mode = b'drum' if liveobj_valid(drum_group) else b'keyboard'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/atom.pyc
