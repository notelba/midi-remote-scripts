# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\DrumPadMixerComponent.py
# Compiled at: 2017-04-24 12:52:35
import Live
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from PropertyControl import PropertyControl, ParameterControl
from SpecialControl import SpecialButtonControl
from ShowMessageMixin import ShowMessageMixin, DisplayType
from ControlUtils import release_parameters, reset_button, assign_button_to_note
from ClipUtils import convert_to_note_name
from Utils import live_object_is_valid
from consts import MAX_DR_SCROLL_POS, ZERO_DB_VALUE, PARAM_REL_STEP, NOTE_NAMES
SAMPLE_SELECTOR_INDEX = 3
CHAIN_SELECTOR_INDEX = 9

class SelectProperty(PropertyControl):
    """ SelectProperty is a special type of property for setting the selected
    Drum Rack pad. """

    def set_property_value(self, current_value, new_value):
        if current_value != new_value:
            pads = list(self._parent.canonical_parent.visible_drum_pads)
            setattr(self._parent, self._property_name, pads[new_value])
            if self._display_callback:
                self._display_callback(pads[new_value].name)

    def get_property_value(self):
        if self._parent.selected_drum_pad:
            pads = list(self._parent.canonical_parent.visible_drum_pads)
            if self._parent.selected_drum_pad in pads:
                return pads.index(self._parent.selected_drum_pad)
            return 0
        return 0

    def __str__(self):
        if self._parent and self._parent.selected_drum_pad:
            return self._parent.selected_drum_pad.name
        return ''


class DrumPadMixerComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ DrumPadMixerComponent provides control over the mixer settings of the
    selected Drum Rack pad. """
    mute_button = SpecialButtonControl(color='Track.NotMuted', on_color='Track.Muted', disabled_color='DrumRack.PadEmpty', enabled=False)
    solo_button = SpecialButtonControl(color='Track.NotSoloed', on_color='Track.Soloed', disabled_color='DrumRack.PadEmpty', enabled=False)
    prev_pad_button = SpecialButtonControl(color='DrumRack.CannotSelectPad', on_color='DrumRack.CanSelectPad', disabled_color='DrumRack.PadEmpty', enabled=False)
    next_pad_button = SpecialButtonControl(color='DrumRack.CannotSelectPad', on_color='DrumRack.CanSelectPad', disabled_color='DrumRack.PadEmpty', enabled=False)

    def __init__(self, targets_comp=None, use_0_db_volume=False, translation_channel=9, name='Selected_Drum_Pad_Control', *a, **k):
        super(DrumPadMixerComponent, self).__init__(name=name, *a, **k)
        self._use_0_db_volume = bool(use_0_db_volume)
        self._translation_channel = translation_channel
        self._drum_rack = None
        self._selected_chain = None
        self._selection_control = None
        self._volume_control = None
        self._pan_control = None
        self._sample_selector_control = None
        self._send_controls = []
        self._macro_controls = []
        self._selected_pad_button = None
        self._on_target_drum_rack_changed.subject = targets_comp
        self._select_property = SelectProperty('selected_drum_pad', None, (0, 15), display_name='Pad', display_callback=self._on_pad_selected)
        self._scroll_property = PropertyControl('drum_pads_scroll_position', None, (
         0, MAX_DR_SCROLL_POS), display_name='Position')
        self._0_db_volume_property = ParameterControl('volume', None, (
         0.0, ZERO_DB_VALUE), default_value=ZERO_DB_VALUE, rel_thresh=0, rel_step=PARAM_REL_STEP, quantized=False)
        out_note_transform = lambda x: convert_to_note_name(x, NOTE_NAMES)
        self._out_note_property = PropertyControl('out_note', None, (0, 127), default_value=60, display_name='Note', display_callback=self._on_out_note_selected, display_value_transform=out_note_transform)
        return

    def disconnect(self):
        self._select_property.disconnect()
        self._scroll_property.disconnect()
        self._0_db_volume_property.disconnect()
        self._out_note_property.disconnect()
        super(DrumPadMixerComponent, self).disconnect()
        self._drum_rack = None
        self._selected_chain = None
        self._selection_control = None
        self._volume_control = None
        self._pan_control = None
        self._sample_selector_control = None
        self._send_controls = None
        self._macro_controls = None
        self._selected_pad_button = None
        return

    def set_shift_button(self, button):
        """ Sets the button to use for switching between the functions of the selection
        control. """
        self._on_shift_button_value.subject = button

    def set_selected_pad_button(self, button):
        """ Sets the button to use for playing the selected pad. """
        button_to_reset = button if button else self._selected_pad_button
        reset_button(button_to_reset)
        self._selected_pad_button = button
        self._update_selected_pad_button()

    def set_selection_control(self, control):
        """ Sets the control to use for selecting one of the 16 visible pads. When shift
        is held, moves the Drum Rack's selector. """
        self._select_property.set_control(control)
        self._selection_control = control

    def set_volume_control(self, control):
        """ Sets the control to use for controlling the volume of the selected pad. """
        if self._use_0_db_volume:
            self._0_db_volume_property.set_control(control)
        else:
            release_parameters((self._volume_control,))
            self._volume_control = control
            self._update_volume_connection()

    def set_pan_control(self, control):
        """ Sets the control to use for controlling the panning of the selected pad. """
        release_parameters((self._pan_control,))
        self._pan_control = control
        self._update_pan_connection()

    def set_out_note_control(self, control):
        """ Sets the control to use for controlling the out note of the selected pad. """
        self._out_note_property.set_control(control)

    def set_sample_selector_control(self, control):
        """ Sets the control to use for 128-style control of the selected pad.  This will
        attach to chain selector of the pad's instrument rack or the sample selector
        of the pad's Sampler. """
        release_parameters((self._sample_selector_control,))
        self._sample_selector_control = control
        self._update_sample_selector_connection()

    def set_send_controls(self, controls):
        """ Sets the controls to use for controlling the sends of the selected pad. """
        release_parameters(self._send_controls)
        self._send_controls = controls or []
        self._update_send_connections()

    def set_macro_controls(self, controls):
        """ Sets the controls to use for controlling the Drum Rack's macros. """
        release_parameters(self._macro_controls)
        self._macro_controls = controls or []
        self._update_macro_connections()

    def set_drum_rack(self, drum_rack, _=None):
        """ Sets the drum rack to control. """
        self._drum_rack = drum_rack if live_object_is_valid(drum_rack) else None
        view = drum_rack.view if drum_rack else None
        self._on_selected_drum_pad_changed.subject = view
        self._select_property.set_parent(view)
        self._scroll_property.set_parent(view)
        self._on_selected_drum_pad_changed()
        self._update_macro_connections()
        return

    @mute_button.pressed
    def mute_button(self, _):
        self._toggle_mute()

    @mute_button.released_delayed
    def mute_button(self, _):
        self._toggle_mute(True)

    @mute_button.pressed_delayed
    def mute_button(self, _):
        pass

    @mute_button.released_immediately
    def mute_button(self, _):
        pass

    def _toggle_mute(self, is_release=False):
        if self.is_enabled() and self._selected_chain:
            if not is_release or self._selected_chain.mute:
                self._selected_chain.mute = not self._selected_chain.mute

    @solo_button.pressed
    def solo_button(self, _):
        self._toggle_solo()

    @solo_button.released_delayed
    def solo_button(self, _):
        self._toggle_solo(True)

    @solo_button.pressed_delayed
    def solo_button(self, _):
        pass

    @solo_button.released_immediately
    def solo_button(self, _):
        pass

    def _toggle_solo(self, is_release=False):
        if self.is_enabled() and self._selected_chain:
            if not is_release or self._selected_chain.solo:
                self._selected_chain.solo = not self._selected_chain.solo

    @prev_pad_button.pressed
    def prev_pad_button(self, _):
        self._increment_selected_pad(-1)

    @next_pad_button.pressed
    def next_pad_button(self, _):
        self._increment_selected_pad(1)

    def _increment_selected_pad(self, factor):
        if self.is_enabled() and self._drum_rack:
            dr = self._drum_rack
            current = list(dr.drum_pads).index(dr.view.selected_drum_pad)
            new_selection = current + factor
            if new_selection in xrange(128):
                dr.view.selected_drum_pad = dr.drum_pads[new_selection]
                if dr.view.selected_drum_pad not in dr.visible_drum_pads:
                    new_scroll_pos = dr.view.drum_pads_scroll_position + factor
                    if new_scroll_pos in xrange(MAX_DR_SCROLL_POS + 1):
                        dr.view.drum_pads_scroll_position = new_scroll_pos
                self._on_pad_selected(dr.view.selected_drum_pad.name)

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        self._scroll_property.set_control(None)
        self._select_property.set_control(None)
        if self._selection_control:
            if value:
                self._scroll_property.set_control(self._selection_control)
            else:
                self._select_property.set_control(self._selection_control)
        return

    def update(self):
        """ Extends standard to set/re-set drum rack so that control LEDs get properly
        updated. """
        super(DrumPadMixerComponent, self).update()
        if self.is_enabled():
            self._tasks.add(partial(self.set_drum_rack, self._drum_rack))

    @subject_slot('target_drum_rack')
    def _on_target_drum_rack_changed(self, drum_rack):
        self.set_drum_rack(drum_rack)

    @subject_slot('selected_drum_pad')
    def _on_selected_drum_pad_changed(self):
        if self.is_enabled():
            self._selected_chain = None
            self._on_sends_changed.subject = None
            if self._drum_rack:
                sel_pad = self._drum_rack.view.selected_drum_pad
                if sel_pad and sel_pad.chains:
                    self._selected_chain = sel_pad.chains[0]
                    self._on_sends_changed.subject = self._selected_chain.mixer_device
                    self._on_devices_changed.subject = self._selected_chain
                    self._on_mute_changed.subject = self._selected_chain
                    self._on_solo_changed.subject = self._selected_chain
            self._update_volume_connection()
            self._update_pan_connection()
            self._update_out_note_connection()
            self._update_sample_selector_connection()
            self._update_send_connections()
            self._update_pad_navigation_buttons()
            self._update_selected_pad_button()
            self._on_mute_changed()
            self._on_solo_changed()
        return

    @subject_slot('sends')
    def _on_sends_changed(self):
        if self.is_enabled():
            self._update_send_connections()

    @subject_slot('devices')
    def _on_devices_changed(self):
        if self.is_enabled():
            self._update_sample_selector_connection()

    @subject_slot('mute')
    def _on_mute_changed(self):
        if self.is_enabled():
            self.mute_button.enabled = self._selected_chain is not None
            if self._selected_chain:
                self.mute_button.is_on = self._selected_chain.mute
        return

    @subject_slot('solo')
    def _on_solo_changed(self):
        if self.is_enabled():
            self.solo_button.enabled = self._selected_chain is not None
            if self._selected_chain:
                self.solo_button.is_on = self._selected_chain.solo
        return

    def _on_pad_selected(self, pad_name):
        self.component_message('Selected Pad', pad_name)

    def _on_out_note_selected(self, _):
        self.component_message('Out Note', str(self._out_note_property), display_type=DisplayType.STATUS)

    @subject_slot('value')
    def _on_sample_selector_change(self):
        param = None
        if self._sample_selector_control:
            param = self._sample_selector_control.mapped_parameter()
            if param:
                self.component_message(param.name, param.str_for_value(param.value))
        return

    def _update_volume_connection(self):
        if self._use_0_db_volume:
            self._0_db_volume_property.set_parent(self._selected_chain.mixer_device.volume if self._selected_chain else None)
        else:
            release_parameters((self._volume_control,))
            if self.is_enabled() and self._selected_chain:
                if self._volume_control:
                    self._volume_control.connect_to(self._selected_chain.mixer_device.volume)
        return

    def _update_pan_connection(self):
        release_parameters((self._pan_control,))
        if self.is_enabled() and self._selected_chain:
            if self._pan_control:
                self._pan_control.connect_to(self._selected_chain.mixer_device.panning)

    def _update_out_note_connection(self):
        self._out_note_property.set_parent(self._selected_chain if self._selected_chain else None)
        return

    def _update_sample_selector_connection(self):
        release_parameters((self._sample_selector_control,))
        self._on_sample_selector_change.subject = None
        if self.is_enabled() and self._selected_chain:
            if self._sample_selector_control:
                devs = self._selected_chain.devices
                if devs:
                    d = devs[0]
                    param = None
                    if d.type == Live.Device.DeviceType.instrument and d.can_have_chains:
                        param = d.parameters[CHAIN_SELECTOR_INDEX]
                    elif d.class_name == 'MultiSampler':
                        param = d.parameters[SAMPLE_SELECTOR_INDEX]
                    self._sample_selector_control.connect_to(param)
                    self._on_sample_selector_change.subject = param
        return

    def _update_send_connections(self):
        release_parameters(self._send_controls)
        if self.is_enabled() and self._selected_chain:
            num_sends = len(self._selected_chain.mixer_device.sends)
            for index, control in enumerate(self._send_controls):
                if control and index < num_sends:
                    control.connect_to(self._selected_chain.mixer_device.sends[index])

    def _update_macro_connections(self):
        release_parameters(self._macro_controls)
        if self.is_enabled() and self._drum_rack:
            for index, control in enumerate(self._macro_controls):
                control.connect_to(self._drum_rack.parameters[(index + 1)])

    def _update_pad_navigation_buttons(self):
        if self.is_enabled():
            can_enable = self._drum_rack is not None and self._drum_rack.view.selected_drum_pad is not None
            self.prev_pad_button.enabled = can_enable
            self.next_pad_button.enabled = can_enable
            if can_enable:
                self.prev_pad_button.is_on = self._drum_rack.view.selected_drum_pad.note > 0
                self.next_pad_button.is_on = self._drum_rack.view.selected_drum_pad.note < 127
        return

    def _update_selected_pad_button(self):
        if self._selected_pad_button:
            can_enable = self._drum_rack is not None and self._drum_rack.view.selected_drum_pad is not None
            if can_enable:
                note = self._drum_rack.view.selected_drum_pad.note
                assign_button_to_note(self._selected_pad_button, note, channel=self._translation_channel, color='DrumRack.PadFilled')
            else:
                reset_button(self._selected_pad_button)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/DrumPadMixerComponent.pyc
