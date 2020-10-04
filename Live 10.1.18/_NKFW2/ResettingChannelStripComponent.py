# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ResettingChannelStripComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot
from ControlUtils import reset_parameter
RESET_COLORS = {'volume': {'on': ('ResetStrip.VolumeCanReset', ), 'off': ('ResetStrip.VolumeCannotReset', )}, 
   'panning': {'on': ('ResetStrip.PanCanReset', ), 'off': ('ResetStrip.PanCannotReset', )}, 
   'sends': {'on': ('ResetStrip.SendACanReset', 'ResetStrip.SendBCanReset'), 
             'off': ('ResetStrip.SendACannotReset', 'ResetStrip.SendBCannotReset')}}

class ResettingChannelStripComponent(ControlSurfaceComponent):
    """ Component that includes buttons for resetting mixer parameters. """

    def __init__(self, *a, **k):
        super(ResettingChannelStripComponent, self).__init__(*a, **k)
        self.is_private = True
        self._track = None
        self._reset_volume_button = None
        self._reset_pan_button = None
        self._reset_send_a_button = None
        self._reset_send_b_button = None
        return

    def disconnect(self):
        super(ResettingChannelStripComponent, self).disconnect()
        self._track = None
        self._reset_volume_button = None
        self._reset_pan_button = None
        self._reset_send_a_button = None
        self._reset_send_b_button = None
        return

    def set_track(self, track):
        self._track = track
        self._on_volume_changed.subject = track.mixer_device.volume if track else None
        self._on_pan_changed.subject = track.mixer_device.panning if track else None
        self._on_returns_changed.subject = track.mixer_device if track else None
        self._on_returns_changed()
        self.update()
        return

    def set_reset_volume_button(self, button):
        """ Sets the button to use for resetting volume. """
        self._reset_volume_button = button
        self._on_reset_volume_button_value.subject = self._reset_volume_button
        self._update_reset_button(self._reset_volume_button, 'volume')

    def set_reset_pan_button(self, button):
        """ Sets the button to use for resetting pan. """
        self._reset_pan_button = button
        self._on_reset_pan_button_value.subject = self._reset_pan_button
        self._update_reset_button(self._reset_pan_button, 'panning')

    def set_reset_send_a_button(self, button):
        """ Sets the button to use for resetting send A. """
        self._reset_send_a_button = button
        self._on_reset_send_a_button_value.subject = self._reset_send_a_button
        self._update_reset_button(self._reset_send_a_button, 'sends', 0)

    def set_reset_send_b_button(self, button):
        """ Sets the button to use for resetting send B. """
        self._reset_send_b_button = button
        self._on_reset_send_b_button_value.subject = self._reset_send_b_button
        self._update_reset_button(self._reset_send_b_button, 'sends', 1)

    @subject_slot('value')
    def _on_reset_volume_button_value(self, value):
        if value:
            self._handle_reset('volume')

    @subject_slot('value')
    def _on_reset_pan_button_value(self, value):
        if value:
            self._handle_reset('panning')

    @subject_slot('value')
    def _on_reset_send_a_button_value(self, value):
        if value:
            self._handle_reset('sends', 0)

    @subject_slot('value')
    def _on_reset_send_b_button_value(self, value):
        if value:
            self._handle_reset('sends', 1)

    def _handle_reset(self, param_name, send_index=None):
        if self._track:
            param = getattr(self._track.mixer_device, param_name)
            if send_index is not None:
                num_returns = len(self.song().return_tracks)
                if send_index < num_returns:
                    param = param[send_index]
                else:
                    return
            self._reset_parameter(param)
        return

    @staticmethod
    def _reset_parameter(param):
        reset_parameter(param)

    @subject_slot('sends')
    def _on_returns_changed(self):
        num_sends = len(self._track.mixer_device.sends) if self._track else None
        self._on_send_a_changed.subject = self._track.mixer_device.sends[0] if num_sends else None
        self._on_send_b_changed.subject = self._track.mixer_device.sends[1] if num_sends > 1 else None
        self._update_reset_button(self._reset_send_a_button, 'sends', 0)
        self._update_reset_button(self._reset_send_b_button, 'sends', 1)
        return

    @subject_slot('value')
    def _on_volume_changed(self):
        self._update_reset_button(self._reset_volume_button, 'volume')

    @subject_slot('value')
    def _on_pan_changed(self):
        self._update_reset_button(self._reset_pan_button, 'panning')

    @subject_slot('value')
    def _on_send_a_changed(self):
        self._update_reset_button(self._reset_send_a_button, 'sends', 0)

    @subject_slot('value')
    def _on_send_b_changed(self):
        self._update_reset_button(self._reset_send_b_button, 'sends', 1)

    def update(self):
        super(ResettingChannelStripComponent, self).update()
        self._update_reset_button(self._reset_volume_button, 'volume')
        self._update_reset_button(self._reset_pan_button, 'panning')
        self._update_reset_button(self._reset_send_a_button, 'sends', 0)
        self._update_reset_button(self._reset_send_b_button, 'sends', 1)

    def _update_reset_button(self, button, param_name, send_index=None):
        if self.is_enabled() and button:
            if self._track:
                param = getattr(self._track.mixer_device, param_name)
                if send_index is not None:
                    num_returns = len(self.song().return_tracks)
                    if send_index < num_returns:
                        param = param[send_index]
                    else:
                        button.set_light('Track.Empty')
                        return
                if param.value == param.default_value:
                    button.set_light(RESET_COLORS[param_name]['off'][(send_index or 0)])
                else:
                    button.set_light(RESET_COLORS[param_name]['on'][(send_index or 0)])
            else:
                button.set_light('Track.Empty')
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ResettingChannelStripComponent.pyc
