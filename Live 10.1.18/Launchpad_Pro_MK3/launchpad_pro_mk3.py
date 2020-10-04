# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro_MK3\launchpad_pro_mk3.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import const, inject, listens, liveobj_valid
from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.components import AutoArmComponent, BackgroundComponent, SessionOverviewComponent, UndoRedoComponent
from ableton.v2.control_surface.mode import AddLayerMode, DelayMode, ModesComponent, MomentaryBehaviour, ReenterBehaviour
from novation import sysex
from novation.clip_actions import ClipActionsComponent
from novation.colors import Rgb
from novation.configurable_playable import ConfigurablePlayableComponent
from novation.fixed_length import FixedLengthComponent, FixedLengthSetting
from novation.fixed_length_recording import FixedLengthRecording
from novation.instrument_control import InstrumentControlMixin
from novation.novation_base import NovationBase
from novation.print_to_clip import PrintToClipComponent
from novation.quantization import QuantizationComponent
from novation.simple_device_navigation import SimpleDeviceNavigationComponent
from novation.track_recording import FixedLengthTrackRecordingComponent
from . import sysex_ids as ids
from .channel_strip import ChannelStripComponent
from .drum_group import DrumGroupComponent
from .elements import Elements, FADER_MODES
from .mixer import MixerComponent
from .session import ClipSlotComponent, SessionComponent
from .simple_device import SimpleDeviceParameterComponent
from .skin import skin
from .transport import TransportComponent
DRUM_FEEDBACK_CHANNEL = 1
SCALE_FEEDBACK_CHANNEL = 2
LAYOUT_BYTES_TO_MODE_NAMES_MAP = {ids.SESSION_LAYOUT_BYTES: b'session', 
   ids.CHORD_LAYOUT_BYTES: b'chord', 
   ids.NOTE_LAYOUT_BYTES: b'note'}
LIVE_LAYOUT_BYTES = (
 ids.SESSION_LAYOUT_BYTES[0],
 ids.CHORD_LAYOUT_BYTES[0],
 ids.NOTE_LAYOUT_BYTES[0],
 ids.FADER_LAYOUT_BYTE)
NOTE_MODE_NAMES = ('chord', 'note')

class Launchpad_Pro_MK3(InstrumentControlMixin, NovationBase):
    model_family_code = ids.LP_PRO_MK3_FAMILY_CODE
    element_class = Elements
    session_class = SessionComponent
    mixer_class = MixerComponent
    channel_strip_class = ChannelStripComponent
    skin = skin
    suppress_layout_switch = False
    track_recording_class = FixedLengthTrackRecordingComponent

    def __init__(self, *a, **k):
        self._layout_to_restore = None
        self._can_restore_layout = False
        self._last_layout_bytes = ids.SESSION_LAYOUT_BYTES
        super(Launchpad_Pro_MK3, self).__init__(*a, **k)
        return

    def disconnect(self):
        super(Launchpad_Pro_MK3, self).disconnect()
        self._auto_arm.set_enabled(False)
        self._elements.scale_feedback_switch.send_value(Rgb.GREEN.midi_value)

    def on_identified(self, midi_bytes):
        self._elements.firmware_mode_switch.send_value(sysex.DAW_MODE_BYTE)
        self._elements.layout_switch.send_value(self._last_layout_bytes)
        self._target_track_changed()
        self._drum_group_changed()
        self.set_feedback_channels([DRUM_FEEDBACK_CHANNEL, SCALE_FEEDBACK_CHANNEL])
        self._setup_faders()
        super(Launchpad_Pro_MK3, self).on_identified(midi_bytes)

    def port_settings_changed(self):
        self._auto_arm.set_enabled(False)
        super(Launchpad_Pro_MK3, self).port_settings_changed()

    def _setup_faders(self):
        for i, fader_mode in enumerate(FADER_MODES):
            orientation, polarity = (sysex.FADER_HORIZONTAL_ORIENTATION, sysex.FADER_BIPOLAR) if fader_mode == b'pan' else (
             sysex.FADER_VERTICAL_ORIENTATION, sysex.FADER_UNIPOLAR)
            self._elements.fader_setup_element.send_value(i, orientation, polarity)

    def _create_components(self):
        self._fixed_length_setting = FixedLengthSetting()
        self._fixed_length_recording = FixedLengthRecording(self.song, self._fixed_length_setting)
        with inject(fixed_length_recording=const(self._fixed_length_recording)).everywhere():
            super(Launchpad_Pro_MK3, self)._create_components()
            self._create_recording_modes()
        self._create_session_overview()
        self._create_auto_arm()
        self._create_background()
        self._create_device_navigation()
        self._create_device_parameters()
        self._create_print_to_clip()
        self._create_undo_redo()
        self._create_transport()
        self._create_clip_actions()
        self._create_quantization()
        self._create_fixed_length()
        self._create_drum_group()
        self._create_scale_pad_translator()
        self._create_mixer_modes()
        self._create_session_modes()
        self._create_note_modes()
        self._create_main_modes()
        self.__on_layout_switch_value.subject = self._elements.layout_switch

    def _create_session_overview(self):
        self._session_overview = SessionOverviewComponent(name=b'Session_Overview', is_enabled=False, session_ring=self._session_ring, enable_skinning=True, layer=Layer(button_matrix=b'clip_launch_matrix'))

    def _create_auto_arm(self):
        self._auto_arm = AutoArmComponent(name=b'Auto_Arm', is_enabled=False)

    def _create_background(self):
        self._background = BackgroundComponent(name=b'Background', is_enabled=False, add_nop_listeners=True, layer=Layer(clear_button=b'clear_button', duplicate_button=b'duplicate_button', quantize_button=b'quantize_button', scene_launch_buttons=b'scene_launch_buttons', priority=-1) + Layer(duplicate_button_with_shift=b'duplicate_button_with_shift', track_select_buttons_with_shift=b'track_select_buttons_with_shift', up_button_with_shift=b'up_button_with_shift', down_button_with_shift=b'down_button_with_shift', left_button_with_shift=b'left_button_with_shift', right_button_with_shift=b'right_button_with_shift', double_button=b'duplicate_button_with_shift', clear_button_with_shift=b'clear_button_with_shift', volume_button_with_shift=b'volume_button_with_shift', pan_button_with_shift=b'pan_button_with_shift', sends_button_with_shift=b'sends_button_with_shift', device_button_with_shift=b'device_button_with_shift', stop_clip_button_with_shift=b'stop_clip_button_with_shift', fixed_length_button_with_shift=b'fixed_length_button_with_shift'))
        self._background.set_enabled(True)

    def _create_print_to_clip(self):
        self._print_to_clip = PrintToClipComponent(name=b'Print_To_Clip', is_enabled=False, layer=Layer(print_to_clip_control=b'print_to_clip_element', print_to_clip_enabler=b'print_to_clip_enabler_element'))
        self._print_to_clip.set_enabled(True)

    def _create_undo_redo(self):
        self._undo_redo = UndoRedoComponent(name=b'Undo_Redo', is_enabled=False, layer=Layer(undo_button=b'record_arm_button_with_shift', redo_button=b'mute_button_with_shift'))
        self._undo_redo.undo_button.color = b'Action.Undo'
        self._undo_redo.undo_button.pressed_color = b'Action.UndoPressed'
        self._undo_redo.redo_button.color = b'Action.Redo'
        self._undo_redo.redo_button.pressed_color = b'Action.RedoPressed'
        self._undo_redo.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name=b'Transport', is_enabled=False, layer=Layer(play_button=b'play_button', continue_playing_button=b'play_button_with_shift', metronome_button=b'solo_button_with_shift', capture_midi_button=b'record_button_with_shift', tap_tempo_button=b'sends_button_with_shift'))
        self._transport.tap_tempo_button.color = b'Transport.TapTempo'
        self._transport.set_enabled(True)

    def _create_clip_actions(self):
        self._clip_actions = ClipActionsComponent(name=b'Clip_Actions', is_enabled=False, layer=Layer(duplicate_button=b'duplicate_button', quantize_button=b'quantize_button', double_loop_button=b'duplicate_button_with_shift'))

    def _create_quantization(self):
        self._quantization = QuantizationComponent(name=b'Quantization', is_enabled=False, layer=Layer(quantization_toggle_button=b'quantize_button_with_shift'))
        self._quantization.set_enabled(True)
        ClipActionsComponent.quantization_component = self._quantization
        ClipSlotComponent.quantization_component = self._quantization

    def _create_fixed_length(self):
        self._fixed_length = FixedLengthComponent(fixed_length_setting=self._fixed_length_setting, name=b'Fixed_Length', is_enabled=False, layer=Layer(fixed_length_button=b'fixed_length_button'))
        self._fixed_length.settings_component.layer = Layer(length_option_buttons=b'track_select_buttons')
        self._fixed_length.set_enabled(True)

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(self._clip_actions, name=b'Drum_Group', is_enabled=False, translation_channel=DRUM_FEEDBACK_CHANNEL, layer=Layer(matrix=b'drum_pads'))
        self._drum_group.set_enabled(True)

    def _create_device_parameters(self):
        self._device_parameters = SimpleDeviceParameterComponent(name=b'Device_Parameters', is_enabled=False, device_bank_registry=self._device_bank_registry, layer=Layer(parameter_controls=b'device_button_faders', static_color_controls=b'device_button_fader_color_elements', stop_fader_control=b'stop_fader_element'), static_color_value=Rgb.DARK_BLUE.midi_value)
        self._device_parameters.set_enabled(True)

    def _create_device_navigation(self):
        self._device_navigation = SimpleDeviceNavigationComponent(name=b'Device_Navigation')

    def _create_scale_pad_translator(self):
        self._scale_pad_translator = ConfigurablePlayableComponent(SCALE_FEEDBACK_CHANNEL, name=b'Scale_Pads', is_enabled=False, layer=Layer(matrix=b'scale_pads'))
        self._scale_pad_translator.set_enabled(True)

    def _create_mixer_modes(self):
        self._mixer_modes = ModesComponent(name=b'Mixer_Modes', is_enabled=False, enable_skinning=True, layer=Layer(arm_button=b'record_arm_button', mute_button=b'mute_button', solo_button=b'solo_button', volume_button=b'volume_button', pan_button=b'pan_button', sends_button=b'sends_button', device_button=b'device_button', stop_button=b'stop_clip_button'))
        self._mixer.layer = Layer(volume_controls=b'volume_button_faders', pan_controls=b'pan_button_faders', send_controls=b'sends_button_faders')
        reselect_track_select_mode = partial(setattr, self._mixer_modes, b'selected_mode', b'track_select')

        def restore_main_layout():
            if self._can_restore_layout and self._layout_to_restore:
                self._elements.layout_switch.send_value(self._layout_to_restore)

        def add_track_select_button_mode(name, control=None, component=self._mixer):
            control_key = control if control else (b'{}_buttons').format(name)
            control_dict = {control_key: b'track_select_buttons'}
            self._mixer_modes.add_mode(name, (
             AddLayerMode(component, Layer(**control_dict)),
             DelayMode(restore_main_layout, delay=0.1)), behaviour=ReenterBehaviour(on_reenter=reselect_track_select_mode))

        add_track_select_button_mode(b'track_select')
        add_track_select_button_mode(b'arm')
        add_track_select_button_mode(b'mute')
        add_track_select_button_mode(b'solo')
        add_track_select_button_mode(b'stop', control=b'stop_track_clip_buttons', component=self._session)

        def switch_to_fader_layout(bank):
            fader_layout_bytes = (
             ids.FADER_LAYOUT_BYTE, bank, 0)
            self._elements.layout_switch.send_value(fader_layout_bytes)

        def add_fader_mode(name, bank, add_layer_mode, static_color=None):
            self._mixer_modes.add_mode(name, (
             add_layer_mode,
             AddLayerMode(self._mixer, Layer(track_select_buttons=b'track_select_buttons')),
             partial(self._mixer._update_send_control_colors),
             partial(self._mixer.set_static_color_value, static_color),
             partial(switch_to_fader_layout, bank)), behaviour=ReenterBehaviour(on_reenter=reselect_track_select_mode))

        add_fader_mode(b'volume', 0, AddLayerMode(self._mixer, Layer(static_color_controls=b'volume_button_fader_color_elements')), static_color=Rgb.GREEN.midi_value)
        add_fader_mode(b'pan', 1, AddLayerMode(self._mixer, Layer(track_color_controls=b'pan_button_fader_color_elements')))
        add_fader_mode(b'sends', 2, AddLayerMode(self._mixer, Layer(send_select_buttons=b'scene_launch_buttons', return_track_color_controls=b'sends_button_fader_color_elements', stop_fader_control=b'stop_fader_element')))
        add_fader_mode(b'device', 3, (
         AddLayerMode(self._background, Layer(up_button=b'up_button', down_button=b'down_button')),
         AddLayerMode(self._device_navigation, Layer(prev_button=b'left_button', next_button=b'right_button')),
         AddLayerMode(self._device_parameters, Layer(bank_select_buttons=b'scene_launch_buttons'))))
        self._mixer_modes.selected_mode = b'track_select'
        self._mixer_modes.set_enabled(True)
        return

    def _create_session_modes(self):
        self._session_modes = ModesComponent(name=b'Session_Modes', is_enabled=False, layer=Layer(overview_button=b'session_mode_button'))
        self._session_modes.add_mode(b'launch', AddLayerMode(self._session, Layer(managed_select_button=b'shift_button', managed_delete_button=b'clear_button', managed_duplicate_button=b'duplicate_button', managed_quantize_button=b'quantize_button', managed_double_button=b'duplicate_button_with_shift', scene_launch_buttons=b'scene_launch_buttons')))
        self._session_modes.add_mode(b'overview', (
         self._session_overview,
         AddLayerMode(self._session_navigation, Layer(page_up_button=b'up_button', page_down_button=b'down_button', page_left_button=b'left_button', page_right_button=b'right_button'))), behaviour=MomentaryBehaviour())
        self._session_modes.selected_mode = b'launch'

    def _create_note_modes(self):
        self._note_modes = ModesComponent(name=b'Note_Modes', is_enabled=False)
        self._note_modes.add_mode(b'scale', AddLayerMode(self._clip_actions, Layer(delete_button=b'clear_button')))
        self._note_modes.add_mode(b'drum', AddLayerMode(self._drum_group, Layer(scroll_up_button=b'left_button', scroll_down_button=b'right_button', scroll_page_up_button=b'up_button', scroll_page_down_button=b'down_button', delete_button=b'clear_button')))

    def _create_main_modes(self):
        self._main_modes = ModesComponent(name=b'Main_Modes', is_enabled=False)
        suppressed_arrow_button_mode = (
         AddLayerMode(self._background, Layer(left_button=b'left_button', right_button=b'right_button', up_button=b'up_button', down_button=b'down_button')),)
        self._main_modes.add_mode(b'none', suppressed_arrow_button_mode)
        self._main_modes.add_mode(b'fader', None)
        self._main_modes.add_mode(b'session', self._session_modes)
        self._main_modes.add_mode(b'note', (self._note_modes, self._clip_actions))
        self._main_modes.add_mode(b'chord', suppressed_arrow_button_mode)
        self._main_modes.selected_mode = b'session'
        self._main_modes.set_enabled(True)
        self.__on_main_mode_changed.subject = self._main_modes
        return

    @listens(b'selected_mode')
    def __on_main_mode_changed(self, mode):
        if mode == b'session':
            self._session_modes.selected_mode = b'launch'
        self._recording_modes.selected_mode = b'session' if mode == b'session' else b'track'
        self._update_controlled_track()
        self._auto_arm.set_enabled(self._is_instrument_mode())

    @listens(b'value')
    def __on_layout_switch_value(self, value):
        self._can_restore_layout = value[0] in LIVE_LAYOUT_BYTES
        if not self._can_restore_layout:
            return
        if value[0] == ids.FADER_LAYOUT_BYTE:
            self._main_modes.selected_mode = b'fader'
        else:
            self._layout_to_restore = value
            if self._mixer_modes.selected_mode in FADER_MODES:
                self._mixer_modes.selected_mode = b'track_select'
            if value in LAYOUT_BYTES_TO_MODE_NAMES_MAP:
                self._main_modes.selected_mode = LAYOUT_BYTES_TO_MODE_NAMES_MAP[value]
            else:
                self._main_modes.selected_mode = b'none'
        self._last_layout_bytes = value

    def _drum_group_changed(self):
        drum_group = self._drum_group_finder.drum_group
        drum_group_valid = liveobj_valid(drum_group)
        self._drum_group.set_drum_group_device(drum_group)
        self._elements.layout_switch.send_value(ids.DRUM_LAYOUT_BYTES if drum_group_valid else ids.SCALE_LAYOUT_BYTES)
        self._note_modes.selected_mode = b'drum' if drum_group_valid else b'scale'

    def _is_instrument_mode(self):
        return self._main_modes.selected_mode in NOTE_MODE_NAMES

    def _feedback_velocity_changed(self, feedback_velocity):
        self._elements.scale_feedback_switch.send_value(feedback_velocity)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro_MK3/launchpad_pro_mk3.pyc