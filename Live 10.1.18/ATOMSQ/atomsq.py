# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\atomsq.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import const, inject, listens
from ableton.v2.control_surface import ControlSurface, Layer, SessionRingSelectionLinking
from ableton.v2.control_surface.components import BackgroundComponent, MixerComponent, SessionNavigationComponent, SessionRecordingComponent, SessionRingComponent, SimpleTrackAssigner, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, EnablingMode, ModesComponent
from novation.simple_device_navigation import SimpleDeviceNavigationComponent
from novation.view_control import NotifyingViewControlComponent
from . import midi
from .button_labels import ButtonLabelsComponent
from .channel_strip import ChannelStripComponent
from .elements import BANK_BUTTON_NAMES, Elements, SESSION_HEIGHT, SESSION_WIDTH
from .launch_and_stop import LaunchAndStopComponent
from .session import SessionComponent
from .simple_device import SimpleDeviceParameterComponent
from .translating_background import TranslatingBackgroundComponent
from .transport import TransportComponent
from .view_toggle import ViewToggleComponent

class ATOMSQ(ControlSurface):

    def __init__(self, *a, **k):
        super(ATOMSQ, self).__init__(*a, **k)
        with self.component_guard():
            self._elements = Elements()
            with inject(element_container=const(self._elements)).everywhere():
                self._create_background()
                self._create_transport()
                self._create_undo()
                self._create_view_toggle()
                self._create_device_parameters()
                self._create_translating_background()
                self._create_device_navigation()
                self._create_launch_and_stop()
                self._create_session()
                self._create_mixer()
                self._create_view_control()
                self._create_button_labels()
                self._create_record_modes()
                self._create_lower_pad_modes()
                self._create_main_modes()
        self.__on_main_view_changed.subject = self.application.view

    def disconnect(self):
        super(ATOMSQ, self).disconnect()
        self._send_midi(midi.NATIVE_MODE_OFF_MESSAGE)

    def port_settings_changed(self):
        self._send_midi(midi.NATIVE_MODE_ON_MESSAGE)
        if self._main_modes.selected_mode == b'instrument':
            self.schedule_message(1, self._elements.upper_firmware_toggle_switch.send_value, 1)
        if self._main_modes.selected_mode != b'song':
            self.schedule_message(1, self._elements.lower_firmware_toggle_switch.send_value, 1)
        super(ATOMSQ, self).port_settings_changed()

    def _create_background(self):
        self._background = BackgroundComponent(name=b'Background', is_enabled=False, add_nop_listeners=True, layer=Layer(**{name:name for name in BANK_BUTTON_NAMES}))
        self._background.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name=b'Transport', is_enabled=False, layer=Layer(scroll_encoder=b'display_encoder', play_button=b'play_button', loop_button=b'play_button_with_shift', stop_button=b'stop_button', metronome_button=b'click_button', capture_midi_button=b'record_button_with_shift', prev_cue_button=b'display_left_button', next_cue_button=b'display_right_button', shift_button=b'shift_button'))
        self._transport.set_enabled(True)

    def _create_undo(self):
        self._undo = UndoRedoComponent(name=b'Undo', is_enabled=False, layer=Layer(undo_button=b'stop_button_with_shift'))
        self._undo.set_enabled(True)

    def _create_view_toggle(self):
        self._view_toggle = ViewToggleComponent(name=b'View_Toggle', is_enabled=False, layer=Layer(main_view_toggle_button=b'bank_a_button', browser_view_toggle_button=b'bank_b_button', detail_view_toggle_button=b'bank_d_button', clip_view_toggle_button=b'bank_h_button'))

    def _create_device_parameters(self):
        self._device_parameters = SimpleDeviceParameterComponent(name=b'Device_Parameters', device_bank_registry=self._device_bank_registry, toggle_lock=self.toggle_lock, layer=Layer(device_name_display=b'device_name_display'), is_enabled=False)
        self._device_parameters.set_enabled(True)

    def _create_translating_background(self):
        self._translating_background = TranslatingBackgroundComponent(name=b'Translating_Background', is_enabled=False, add_nop_listeners=True, layer=Layer(encoders=b'encoders', channel_selection_buttons=b'display_buttons'))

    def _create_device_navigation(self):
        self._device_navigation = SimpleDeviceNavigationComponent(name=b'Device_Navigation', is_enabled=False, layer=Layer(prev_button=b'display_buttons_raw[1]', next_button=b'display_buttons_raw[2]'))

    def _create_launch_and_stop(self):
        self._launch_and_stop = LaunchAndStopComponent(name=b'Launch_And_Stop', is_enabled=False, layer=Layer(clip_launch_button=b'display_buttons_raw[3]', scene_launch_button=b'display_buttons_raw[4]', track_stop_button=b'display_buttons_raw[5]'))

    def _create_session(self):
        self._session_ring = SessionRingComponent(name=b'Session_Ring', num_tracks=SESSION_WIDTH, num_scenes=SESSION_HEIGHT)
        self._session = SessionComponent(name=b'Session', is_enabled=False, session_ring=self._session_ring, layer=Layer(clip_launch_buttons=b'upper_pads'))
        self._session_navigation = SessionNavigationComponent(name=b'Session_Navigation', is_enabled=False, session_ring=self._session_ring, layer=Layer(up_button=b'up_button_with_shift', down_button=b'down_button_with_shift'))
        self._session_navigation.set_enabled(True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name=b'Mixer', auto_name=True, tracks_provider=self._session_ring, track_assigner=SimpleTrackAssigner(), channel_strip_component_type=ChannelStripComponent)
        self._mixer.selected_strip().layer = Layer(track_name_display=b'track_name_display')
        self._mixer.set_enabled(True)

    def _create_view_control(self):
        self._view_control = NotifyingViewControlComponent(name=b'View_Control', is_enabled=False, track_provider=self._session_ring, enable_skinning=False, layer=Layer(next_track_button=b'right_button', prev_track_button=b'left_button', next_scene_button=b'down_button', prev_scene_button=b'up_button'))
        self._view_control.set_enabled(True)
        self._session_ring_selection_linking = self.register_disconnectable(SessionRingSelectionLinking(session_ring=self._session_ring, selection_changed_notifier=self._view_control))

    def _create_button_labels(self):
        self._button_labels = ButtonLabelsComponent(is_enabled=False, layer=Layer(display_lines=b'button_label_display_matrix'))
        self._button_labels.set_enabled(True)

    def _create_record_modes(self):
        self._session_record = SessionRecordingComponent(name=b'Session_Record', is_enabled=False, layer=Layer(record_button=b'record_button'))
        self._record_modes = ModesComponent(name=b'Record_Modes')
        self._record_modes.add_mode(b'session', EnablingMode(self._session_record))
        self._record_modes.add_mode(b'arrange', AddLayerMode(self._transport, layer=Layer(record_button=b'record_button')))
        self.__on_main_view_changed()

    def _create_lower_pad_modes(self):
        self._lower_pad_modes = ModesComponent(name=b'Lower_Pad_Modes', is_enabled=False, layer=Layer(cycle_mode_button=b'minus_button'))
        self._lower_pad_modes.add_mode(b'select', AddLayerMode(self._mixer, Layer(track_select_buttons=b'lower_pads')), cycle_mode_button_color=b'Session.StopClipDisabled')
        self._lower_pad_modes.add_mode(b'stop', AddLayerMode(self._session, Layer(stop_track_clip_buttons=b'lower_pads')), cycle_mode_button_color=b'Session.StopClip')
        self._lower_pad_modes.selected_mode = b'select'

    def _create_main_modes(self):
        self._main_modes = ModesComponent(name=b'Main_Modes', is_enabled=False, layer=Layer(song_button=b'song_mode_button', instrument_button=b'instrument_mode_button', editor_button=b'editor_mode_button', user_button=b'user_mode_button'))
        device_params_mode = AddLayerMode(self._device_parameters, Layer(parameter_controls=b'encoders'))
        enable_lower_fw_functions = partial(self._elements.lower_firmware_toggle_switch.send_value, 1)
        disable_upper_fw_functions = partial(self._elements.upper_firmware_toggle_switch.send_value, 0)
        self._main_modes.add_mode(b'song', (
         partial(self._elements.lower_firmware_toggle_switch.send_value, 0),
         disable_upper_fw_functions,
         self._elements.display_buttons.reset,
         self._view_toggle,
         self._launch_and_stop,
         self._session,
         self._lower_pad_modes,
         AddLayerMode(self._session.scene(0), Layer(launch_button=b'plus_button')),
         AddLayerMode(self._mixer.selected_strip(), Layer(volume_control=b'encoders_raw[0]', pan_control=b'encoders_raw[1]', send_controls=self._elements.encoders.submatrix[2:, :], solo_button=b'display_buttons_raw[0]', mute_button=b'display_buttons_raw[1]', arm_button=b'display_buttons_raw[2]')),
         AddLayerMode(self._mixer, Layer(crossfader_control=b'touch_strip'))))
        self._main_modes.add_mode(b'instrument', (
         enable_lower_fw_functions,
         partial(self._elements.upper_firmware_toggle_switch.send_value, 1),
         device_params_mode))
        self._main_modes.add_mode(b'editor', (
         enable_lower_fw_functions,
         disable_upper_fw_functions,
         device_params_mode,
         self._device_navigation,
         AddLayerMode(self._device_parameters, Layer(device_lock_button=b'display_buttons_raw[0]', device_on_off_button=b'display_buttons_raw[3]', prev_bank_button=b'display_buttons_raw[4]', next_bank_button=b'display_buttons_raw[5]'))))
        self._main_modes.add_mode(b'user', (
         enable_lower_fw_functions,
         disable_upper_fw_functions,
         self._translating_background))
        self._main_modes.selected_mode = b'instrument'
        self._main_modes.set_enabled(True)
        self.__on_main_modes_changed.subject = self._main_modes

    @listens(b'selected_mode')
    def __on_main_modes_changed(self, mode):
        self._button_labels.show_button_labels_for_mode(mode)
        self._elements.track_name_display.clear_send_cache()
        self._elements.device_name_display.clear_send_cache()

    @listens(b'is_view_visible', b'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible(b'Session'):
            self._record_modes.selected_mode = b'session'
        else:
            self._record_modes.selected_mode = b'arrange'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/atomsq.pyc
