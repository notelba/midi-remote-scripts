# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\launchpad_x.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import listens, liveobj_valid, mixin, nop
from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.components import ArmedTargetTrackComponent, BackgroundComponent, SessionOverviewComponent, SessionRecordingComponent
from ableton.v2.control_surface.mode import AddLayerMode, DelayMode, ImmediateBehaviour, ModesComponent, ReenterBehaviour
from novation import sysex
from novation.colors import Rgb
from novation.configurable_playable import ConfigurablePlayableComponent
from novation.drum_group import DrumGroupComponent
from novation.instrument_control import InstrumentControlMixin
from novation.novation_base import NovationBase
from novation.session_modes import SessionModesComponent
from novation.track_recording import TrackRecordingComponent
from . import sysex_ids as ids
from .channel_strip import ChannelStripComponent
from .elements import Elements
from .session_recording import SessionRecordingMixin
from .skin import skin
DRUM_FEEDBACK_CHANNEL = 1
SCALE_FEEDBACK_CHANNEL = 2
SESSION_MODES_SWITCH_DELAY = 0.1

class Launchpad_X(InstrumentControlMixin, NovationBase):
    model_family_code = ids.LP_X_FAMILY_CODE
    element_class = Elements
    channel_strip_class = ChannelStripComponent
    session_recording_class = mixin(SessionRecordingMixin, SessionRecordingComponent)
    track_recording_class = mixin(SessionRecordingMixin, TrackRecordingComponent)
    target_track_class = ArmedTargetTrackComponent
    skin = skin

    def __init__(self, *a, **k):
        self._last_layout_byte = sysex.SESSION_LAYOUT_BYTE
        super(Launchpad_X, self).__init__(*a, **k)

    def on_identified(self, midi_bytes):
        self._elements.firmware_mode_switch.send_value(sysex.DAW_MODE_BYTE)
        self._elements.layout_switch.send_value(self._last_layout_byte)
        self._target_track_changed()
        self._drum_group_changed()
        self.set_feedback_channels([DRUM_FEEDBACK_CHANNEL, SCALE_FEEDBACK_CHANNEL])
        super(Launchpad_X, self).on_identified(midi_bytes)

    def _create_components(self):
        super(Launchpad_X, self)._create_components()
        self._background = BackgroundComponent(name=b'Background', add_nop_listeners=True)
        self._session_layout_mode = partial(self._elements.layout_switch.send_value, sysex.SESSION_LAYOUT_BYTE)
        self._create_recording_modes()
        self._create_mixer_modes()
        self._create_session_modes()
        self._create_note_modes()
        self._create_main_modes()
        self._mixer.set_send_controls = nop
        self.__on_layout_switch_value.subject = self._elements.layout_switch

    def _create_mixer_modes(self):
        self._mixer_modes = ModesComponent(name=b'Mixer_Modes', is_enabled=False, enable_skinning=True, layer=Layer(volume_button=self._elements.scene_launch_buttons_raw[0], pan_button=self._elements.scene_launch_buttons_raw[1], send_a_button=self._elements.scene_launch_buttons_raw[2], send_b_button=self._elements.scene_launch_buttons_raw[3], stop_button=self._elements.scene_launch_buttons_raw[4], mute_button=self._elements.scene_launch_buttons_raw[5], solo_button=self._elements.scene_launch_buttons_raw[6], arm_button=self._elements.scene_launch_buttons_raw[7]))
        bottom_row = self._elements.clip_launch_matrix.submatrix[:, 7:8]
        select_none_mode = partial(setattr, self._mixer_modes, b'selected_mode', b'none')
        self._mixer_modes.add_mode(b'none', self._session_layout_mode)
        button_fader_layout_mode = partial(self._elements.layout_switch.send_value, sysex.FADERS_LAYOUT_BYTE)

        def add_fader_mode(name, color, is_pan=False):
            control_dict = {(b'{}_controls').format(name): b'button_faders'}
            if is_pan:
                control_dict[b'track_color_controls'] = b'button_fader_color_elements'
            else:
                control_dict[b'static_color_controls'] = b'button_fader_color_elements'
            self._mixer_modes.add_mode(name, (
             partial(self._elements.button_fader_setup_element.send_value, sysex.FADER_HORIZONTAL_ORIENTATION if is_pan else sysex.FADER_VERTICAL_ORIENTATION, sysex.FADER_BIPOLAR if is_pan else sysex.FADER_UNIPOLAR),
             partial(self._mixer.set_static_color_value, color),
             self._clear_send_cache_of_button_fader_color_elements,
             AddLayerMode(self._mixer, Layer(**control_dict)),
             button_fader_layout_mode), behaviour=ReenterBehaviour(on_reenter=select_none_mode))

        add_fader_mode(b'volume', Rgb.GREEN.midi_value)
        add_fader_mode(b'pan', 0, True)
        add_fader_mode(b'send_a', Rgb.VIOLET.midi_value)
        add_fader_mode(b'send_b', Rgb.DARK_BLUE.midi_value)
        self._mixer_modes.add_mode(b'stop', (
         self._session_layout_mode,
         AddLayerMode(self._session, Layer(stop_track_clip_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.add_mode(b'mute', (
         self._session_layout_mode,
         AddLayerMode(self._mixer, Layer(mute_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.add_mode(b'solo', (
         self._session_layout_mode,
         AddLayerMode(self._mixer, Layer(solo_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.add_mode(b'arm', (
         self._session_layout_mode,
         AddLayerMode(self._mixer, Layer(arm_buttons=bottom_row))), behaviour=ReenterBehaviour(on_reenter=select_none_mode))
        self._mixer_modes.selected_mode = b'none'

    def _clear_send_cache_of_button_fader_color_elements(self):
        for element in self._elements.button_fader_color_elements_raw:
            element.clear_send_cache()

    def _create_session_modes(self):
        self._session_overview = SessionOverviewComponent(name=b'Session_Overview', is_enabled=False, session_ring=self._session_ring, enable_skinning=True, layer=Layer(button_matrix=b'clip_launch_matrix'))
        self._session_modes = SessionModesComponent(name=b'Session_Modes', is_enabled=False, layer=Layer(cycle_mode_button=b'session_mode_button', mode_button_color_control=b'session_button_color_element'))
        self._session_modes.add_mode(b'launch', AddLayerMode(self._session, Layer(scene_launch_buttons=b'scene_launch_buttons')))
        self._session_modes.add_mode(b'mixer', DelayMode(self._mixer_modes, SESSION_MODES_SWITCH_DELAY))
        (
         self._session_modes.add_mode(b'overview', (
          self._session_layout_mode,
          self._session_overview,
          AddLayerMode(self._session_navigation, Layer(page_up_button=b'up_button', page_down_button=b'down_button', page_left_button=b'left_button', page_right_button=b'right_button')),
          AddLayerMode(self._background, Layer(scene_launch_buttons=b'scene_launch_buttons')))),)
        self._session_modes.selected_mode = b'launch'

    def _create_note_modes(self):
        self._drum_group = DrumGroupComponent(name=b'Drum_Group', is_enabled=False, translation_channel=DRUM_FEEDBACK_CHANNEL, layer=Layer(matrix=b'drum_pads', scroll_up_button=b'left_button', scroll_down_button=b'right_button', scroll_page_up_button=b'up_button', scroll_page_down_button=b'down_button'))
        self._scale_pad_translator = ConfigurablePlayableComponent(SCALE_FEEDBACK_CHANNEL, name=b'Scale_Pads', is_enabled=False, layer=Layer(matrix=b'scale_pads'))
        self._note_modes = ModesComponent(name=b'Note_Modes', is_enabled=False)
        self._note_modes.add_mode(b'scale', (
         self._scale_pad_translator,
         AddLayerMode(self._background, layer=Layer(up_button=b'up_button', down_button=b'down_button', left_button=b'left_button', right_button=b'right_button'))))
        self._note_modes.add_mode(b'drum', self._drum_group)
        self._note_modes.selected_mode = b'scale'
        self.__on_note_mode_changed.subject = self._note_modes

    def _create_main_modes(self):
        self._main_modes = ModesComponent(name=b'Main_Modes', is_enabled=False, layer=Layer(session_button=b'session_mode_button', note_button=b'note_mode_button', custom_button=b'custom_mode_button'))
        self._main_modes.add_mode(b'session', self._session_modes, behaviour=ImmediateBehaviour())
        self._main_modes.add_mode(b'note', self._note_modes, behaviour=ImmediateBehaviour())
        self._main_modes.add_mode(b'custom', None, behaviour=ImmediateBehaviour())
        self._main_modes.selected_mode = b'session'
        self._main_modes.set_enabled(True)
        self.__on_main_mode_changed.subject = self._main_modes
        return

    @listens(b'selected_mode')
    def __on_main_mode_changed(self, mode):
        self._recording_modes.selected_mode = b'track' if mode == b'note' else b'session'
        if mode == b'session':
            self._session_modes.revert_to_main_mode()
        self._update_controlled_track()
        self._elements.layout_switch.enquire_value()

    @listens(b'selected_mode')
    def __on_note_mode_changed(self, mode):
        if self._note_modes.is_enabled():
            self._update_controlled_track()

    @listens(b'value')
    def __on_layout_switch_value(self, value):
        self._last_layout_byte = value

    def _drum_group_changed(self):
        drum_group = self._drum_group_finder.drum_group
        drum_groud_valid = liveobj_valid(drum_group)
        self._drum_group.set_drum_group_device(drum_group)
        self._elements.note_layout_switch.send_value(sysex.DRUM_LAYOUT_BYTE if drum_groud_valid else sysex.SCALE_LAYOUT_BYTE)
        self._note_modes.selected_mode = b'drum' if drum_groud_valid else b'scale'

    def _is_instrument_mode(self):
        return self._main_modes.selected_mode == b'note'

    def _feedback_velocity_changed(self, feedback_velocity):
        self._elements.scale_feedback_switch.send_value(feedback_velocity)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_X/launchpad_x.pyc
