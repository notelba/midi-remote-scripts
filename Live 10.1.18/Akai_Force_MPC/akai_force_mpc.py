# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\akai_force_mpc.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from contextlib import contextmanager
from functools import partial
from itertools import chain
from ableton.v2.base import const, inject, task
from ableton.v2.control_surface import BankingInfo, ControlSurface, DeviceDecoratorFactory, Layer, Skin
from ableton.v2.control_surface.components import BackgroundComponent, RightAlignTracksTrackAssigner, SessionRingComponent, UndoRedoComponent
from ableton.v2.control_surface.default_bank_definitions import BANK_DEFINITIONS as DEFAULT_BANK_DEFINITIONS
from ableton.v2.control_surface.elements import MultiElement, SysexElement
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode, ModesComponent, MomentaryBehaviour
from .sysex import SYSEX_MSG_HEADER, SYSEX_END_BYTE, MPC_X_PRODUCT_ID, MPC_LIVE_PRODUCT_ID, FORCE_PRODUCT_ID, SUPPORTED_PRODUCT_IDS, BROADCAST_ID, PING_MSG_TYPE, PONG_MSG_TYPE
from .background import LightingBackgroundComponent
from .channel_strip import ChannelStripComponent
from .clip_actions import ClipActionsComponent
from .device import DeviceComponent
from .device_navigation import ScrollingDeviceNavigationComponent
from .device_parameters import DeviceParameterComponent
from .elements import ForceElements, MPCLiveElements, MPCXElements, NUM_SCENE_CONTROLS, NUM_TRACK_CONTROLS
from .mixer import MixerComponent
from .mode import ExtendComboElementMode
from .ping_pong import PingPongComponent
from .scene_list import SceneListComponent
from .session import SessionComponent
from .session_navigation import SessionNavigationComponent
from .session_recording import SessionRecordingComponent
from .skin import ForceColors, MPCColors
from .sysex_element import IdentifyingSysexElement
from .transport import ForceTransportComponent, MPCTransportComponent

class Akai_Force_MPC(ControlSurface):

    def __init__(self, *a, **k):
        super(Akai_Force_MPC, self).__init__(*a, **k)
        self._product_id = None
        self._element_injector = inject(element_container=const(None)).everywhere()
        self._is_initialized = False
        self._initialize_task = self._tasks.add(task.run(self._initialize))
        self._initialize_task.kill()
        self._components_enabled = False
        with self.component_guard():
            self._ping_element = SysexElement(send_message_generator=const(SYSEX_MSG_HEADER + (BROADCAST_ID, PING_MSG_TYPE, SYSEX_END_BYTE)), name=b'Ping_Element')
            self._pong_element = MultiElement(name=b'Pong_Multi_Element', *[ IdentifyingSysexElement(sysex_identifier=SYSEX_MSG_HEADER + (identifier, PONG_MSG_TYPE), name=(b'Pong_Element_{}').format(index)) for index, identifier in enumerate(SUPPORTED_PRODUCT_IDS)
                                                                           ])
            self._ping_pong = PingPongComponent(on_pong_callback=self._identify, on_ping_timeout=partial(self._enable_components, False), name=b'Ping_Pong')
            self._ping_pong.layer = Layer(ping=self._ping_element, pong=self._pong_element)
        return

    @contextmanager
    def _component_guard(self):
        with super(Akai_Force_MPC, self)._component_guard():
            with self._element_injector:
                yield

    @property
    def is_force(self):
        return self._product_id == FORCE_PRODUCT_ID

    def _identify(self, id_byte):
        if id_byte in SUPPORTED_PRODUCT_IDS:
            if not self._is_initialized:
                self._product_id = id_byte
                self._create_elements()
                self._initialize_task.restart()
            elif self._product_id == id_byte:
                self._enable_components(True)

    def _initialize(self):
        self._create_components()
        self._is_initialized = True
        self._enable_components(True)

    def _create_elements(self):
        with self.component_guard():
            skin = Skin(ForceColors if self.is_force else MPCColors)
            with inject(skin=const(skin)).everywhere():
                elements_class = None
                if self.is_force:
                    elements_class = ForceElements
                elif self._product_id == MPC_X_PRODUCT_ID:
                    elements_class = MPCXElements
                elif self._product_id == MPC_LIVE_PRODUCT_ID:
                    elements_class = MPCLiveElements
                self._elements = elements_class(self._product_id)
        self._element_injector = inject(element_container=const(self._elements)).everywhere()
        return

    def _create_components(self):
        with self.component_guard():
            self._create_mixer()
            self._create_session()
            self._create_session_navigation()
            self._create_transport()
            self._create_actions()
            if self.is_force:
                self._create_track_assign_button_modes()
                self._create_background()
            self._create_launch_modes()
            self._create_device()
            self._create_session_recording()

    def _enable_components(self, enable):
        if self._components_enabled != enable:
            if enable:
                self._clear_send_cache()
            with self.component_guard():
                self._components_enabled = enable
                for component in [ c for c in self.root_components if c is not self._ping_pong ]:
                    component.set_enabled(enable)

    def _clear_send_cache(self):
        for control in self.controls:
            control.clear_send_cache()

    def _create_mixer(self):
        self._session_ring = SessionRingComponent(is_enabled=False, num_tracks=NUM_TRACK_CONTROLS, num_scenes=NUM_SCENE_CONTROLS, tracks_to_use=lambda : tuple(self.song.visible_tracks) + tuple(self.song.return_tracks) + (self.song.master_track,), name=b'Session_Ring')
        self._mixer = MixerComponent(is_enabled=False, tracks_provider=self._session_ring, track_assigner=RightAlignTracksTrackAssigner(song=self.song, include_master_track=True), channel_strip_component_type=ChannelStripComponent, name=b'Mixer', layer=Layer(volume_controls=b'volume_sliders', pan_controls=b'pan_sliders', solo_buttons=b'solo_buttons', mute_buttons=b'mute_buttons', arm_buttons=b'arm_buttons', send_controls=b'send_encoders', track_type_controls=b'track_type_controls', output_meter_left_controls=b'meter_controls_left', output_meter_right_controls=b'meter_controls_right', track_select_buttons=b'track_select_buttons', track_name_displays=b'track_name_displays', num_sends_control=b'num_sends_control', track_color_controls=b'tui_track_color_controls', oled_display_style_controls=b'oled_display_style_controls_bank_1', track_name_or_volume_value_displays=b'track_name_or_volume_value_displays', crossfade_assign_controls=b'crossfade_assign_controls', crossfader_control=b'crossfader', solo_mute_buttons=b'solo_mute_buttons', volume_value_displays=b'volume_value_displays', pan_value_displays=b'pan_value_displays', send_value_displays=b'send_value_displays'))
        if not self.is_force:
            self._mixer.layer += Layer(selected_track_arm_button=b'selected_track_arm_button', selected_track_mute_button=b'selected_track_mute_button', selected_track_solo_button=b'selected_track_solo_button')
        else:
            self._mixer.layer += Layer(master_button=b'master_button', physical_track_color_controls=b'physical_track_color_controls')

    def _create_session(self):
        self._session = SessionComponent(is_enabled=False, session_ring=self._session_ring, name=b'Session', layer=Layer(stop_track_clip_buttons=b'clip_stop_buttons', clip_launch_buttons=b'clip_launch_buttons', scene_launch_buttons=b'scene_launch_buttons', clip_name_displays=b'clip_name_displays', scene_name_displays=b'scene_name_displays', scene_color_controls=b'tui_scene_color_controls', clip_color_controls=b'clip_color_controls', playing_position_controls=b'playing_position_controls', select_button=b'clip_select_button' if self.is_force else b'shift_button', scene_selection_controls=b'scene_selection_controls', stop_all_clips_button=b'stop_all_clips_button', insert_scene_button=b'insert_scene_button'))
        if self.is_force:
            self._session.layer += Layer(force_scene_launch_buttons=b'force_physical_scene_launch_buttons')

    def _create_session_navigation(self):
        self._session_navigation = SessionNavigationComponent(is_enabled=False, session_ring=self._session_ring, layer=Layer(page_up_button=b'up_button_with_shift', page_down_button=b'down_button_with_shift', page_left_button=b'left_button_with_shift', page_right_button=b'right_button_with_shift', up_button=b'up_button', down_button=b'down_button', left_button=b'left_button', right_button=b'right_button'), name=b'Session_Navigation')

    def _create_track_assign_button_modes(self):
        self._background = BackgroundComponent(name=b'Background')
        self._modes = ModesComponent(name=b'Track_Assign_Button_Modes', is_enabled=False)
        self._modes.add_mode(b'mute', [
         ExtendComboElementMode(combo_pairs=zip(self._elements.mute_buttons_raw, self._elements.track_assign_buttons_raw)),
         AddLayerMode(self._mixer, Layer(mute_color_controls=b'track_assign_color_controls'))])
        self._modes.add_mode(b'solo', [
         ExtendComboElementMode(combo_pairs=zip(self._elements.solo_buttons_raw, self._elements.track_assign_buttons_raw)),
         AddLayerMode(self._mixer, Layer(solo_color_controls=b'track_assign_color_controls'))])
        self._modes.add_mode(b'rec_arm', [
         ExtendComboElementMode(combo_pairs=zip(self._elements.arm_buttons_raw, self._elements.track_assign_buttons_raw)),
         AddLayerMode(self._mixer, Layer(arm_color_controls=b'track_assign_color_controls'))])
        self._modes.add_mode(b'clip_stop', [
         ExtendComboElementMode(combo_pairs=zip(self._elements.clip_stop_buttons_raw, self._elements.track_assign_buttons_raw)),
         AddLayerMode(self._session, Layer(stop_clip_color_controls=b'track_assign_color_controls'))])
        self._modes.add_mode(b'shift', [
         AddLayerMode(self._transport, Layer(metronome_color_control=b'track_assign_color_controls_raw[4]', clip_trigger_quantization_color_controls=b'physical_track_color_controls')),
         AddLayerMode(self._clip_actions, Layer(quantize_color_control=b'track_assign_color_controls_raw[0]')),
         LayerMode(self._background, Layer(button1=b'track_assign_color_controls_raw[1]', button2=b'track_assign_color_controls_raw[2]', button3=b'track_assign_color_controls_raw[3]', button5=b'track_assign_color_controls_raw[5]', button6=b'track_assign_color_controls_raw[6]', button7=b'track_assign_color_controls_raw[7]'))], behaviour=MomentaryBehaviour())
        self._modes.add_mode(b'assign_a', [
         AddLayerMode(self._mixer, Layer(assign_a_buttons=b'track_assign_buttons', assign_a_color_controls=b'track_assign_color_controls'))], behaviour=MomentaryBehaviour())
        self._modes.add_mode(b'assign_b', [
         AddLayerMode(self._mixer, Layer(assign_b_buttons=b'track_assign_buttons', assign_b_color_controls=b'track_assign_color_controls'))], behaviour=MomentaryBehaviour())
        self._modes.layer = Layer(mute_button=b'mute_button', solo_button=b'solo_button', rec_arm_button=b'rec_arm_button', clip_stop_button=b'clip_stop_button', shift_button=b'shift_button', assign_a_button=b'assign_a_button', assign_b_button=b'assign_b_button')
        self._modes.selected_mode = b'clip_stop'

    def _create_background(self):
        self.background = LightingBackgroundComponent(name=b'Background')
        self.background.layer = Layer(launch_button=b'launch_button')

    def _create_launch_modes(self):
        self._scene_list = SceneListComponent(name=b'Expanded_Scene_Launch', session_ring=self._session_ring, num_scenes=16)
        self._launch_modes = ModesComponent(name=b'Launch_Modes')
        self._launch_modes.add_mode(b'clip_launch', [
         partial(self._elements.launch_mode_switch.send_value, 0),
         ExtendComboElementMode(combo_pairs=zip(chain(*self._elements.clip_launch_buttons_raw), chain(*self._elements.physical_clip_launch_buttons_raw))),
         ExtendComboElementMode(combo_pairs=zip(chain(*self._elements.clip_color_controls_raw), chain(*self._elements.physical_clip_color_controls_raw)))], cycle_mode_button_color=b'Mode.Off')
        if not self.is_force:
            self._launch_modes.add_mode(b'scene_launch', [
             partial(self._elements.launch_mode_switch.send_value, 1),
             LayerMode(self._scene_list, Layer(scene_launch_buttons=b'mpc_scene_launch_buttons', scene_color_controls=b'mpc_scene_color_controls'))], cycle_mode_button_color=b'Mode.On')
            self._launch_modes.layer = Layer(cycle_mode_button=b'xyfx_button' if self._product_id == MPC_X_PRODUCT_ID else b'sixteen_level_button')
        self._launch_modes.selected_mode = b'clip_launch'

    def _create_actions(self):
        self._clip_actions = ClipActionsComponent(name=b'Clip_Actions', is_enabled=False, layer=Layer(duplicate_button=b'duplicate_button', quantization_value_control=b'quantization_value_control', quantize_button=b'quantize_button', delete_button=b'delete_button'))
        self._undo_redo = UndoRedoComponent(name=b'Undo_Redo', is_enabled=False, layer=Layer(undo_button=b'undo_button', redo_button=b'redo_button'))
        self._undo_redo.undo_button.color = b'Action.On'
        self._undo_redo.redo_button.color = b'Action.On'

    def _create_device(self):
        self._device = DeviceComponent(is_enabled=False, device_decorator_factory=DeviceDecoratorFactory(), device_bank_registry=self._device_bank_registry, banking_info=BankingInfo(DEFAULT_BANK_DEFINITIONS), toggle_lock=self.toggle_lock, name=b'Device', layer=Layer(prev_bank_button=b'prev_bank_button', next_bank_button=b'next_bank_button', bank_name_display=b'device_bank_name_display', device_lock_button=b'device_lock_button'))
        self._device_parameters = DeviceParameterComponent(is_enabled=False, parameter_provider=self._device, name=b'Device_Parameters', layer=Layer(parameter_controls=b'physical_device_controls', absolute_parameter_controls=b'tui_device_controls', parameter_enable_controls=b'device_parameter_enable_controls', display_style_controls=b'oled_display_style_controls_bank_2', touch_controls=b'physical_device_control_touch_elements', parameter_name_or_value_displays=b'device_parameter_name_or_value_displays', parameter_name_displays=b'tui_device_parameter_name_displays', parameter_value_displays=b'tui_device_parameter_value_displays', device_enable_button=b'device_enable_button'))
        self._device_navigation = ScrollingDeviceNavigationComponent(is_enabled=False, name=b'Device_Navigation', device_component=self._device, layer=Layer(prev_device_button=b'prev_device_button', next_device_button=b'next_device_button', num_devices_control=b'num_devices_control', device_index_control=b'device_index_control', device_name_display=b'device_name_display'))

    def _create_transport(self):
        transport_component_class = ForceTransportComponent if self.is_force else MPCTransportComponent
        self._transport = transport_component_class(is_enabled=False, name=b'Transport', layer=Layer(tempo_display=b'tempo_display', tempo_control=b'tempo_control', play_button=b'play_button', continue_playing_button=b'continue_button', stop_button=b'stop_button', tap_tempo_button=b'tap_tempo_button', shift_button=b'shift_button', nudge_down_button=b'phase_nudge_down_button', nudge_up_button=b'phase_nudge_up_button', tui_metronome_button=b'tui_metronome_button', metronome_button=b'physical_metronome_button', loop_button=b'loop_button', arrangement_overdub_button=b'arrangement_overdub_button', follow_song_button=b'follow_song_button', clip_trigger_quantization_control=b'clip_trigger_quantization_control', loop_start_display=b'tui_loop_start_display', loop_length_display=b'tui_loop_length_display', arrangement_position_display=b'tui_arrangement_position_display', loop_start_control=b'tui_loop_start_control', loop_length_control=b'tui_loop_length_control', arrangement_position_control=b'tui_arrangement_position_control', tui_arrangement_record_button=b'tui_arrangement_record_button'))
        self._transport.tap_tempo_button.color = b'Transport.TapTempo'
        if self.is_force:
            self._transport.layer += Layer(clip_trigger_quantization_button_row=b'physical_track_select_buttons_with_shift')
        else:
            self._transport.layer += Layer(record_button=b'arrangement_record_button', jump_backward_button=b'jump_backward_button', jump_forward_button=b'jump_forward_button')

    def _create_session_recording(self):
        self._session_recording = SessionRecordingComponent(is_enabled=False, name=b'Session_Recording', layer=Layer(record_button=b'session_record_button', automation_button=b'tui_automation_arm_button'))
        if not self.is_force:
            self._session_recording.layer += Layer(mpc_automation_toggle=b'read_write_button')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/akai_force_mpc.pyc
