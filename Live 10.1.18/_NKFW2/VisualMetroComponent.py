# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\VisualMetroComponent.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from ControlUtils import set_group_button_lights

class VisualMetroComponent(ControlSurfaceComponent):
    """  VisualMetroComponent utilizes a group of buttons to display a
    visual metronome. """

    def __init__(self, name='Visual_Metronome', *a, **k):
        super(VisualMetroComponent, self).__init__(name, *a, **k)
        self._last_visual_metro_led = None
        self._last_beat = -1
        self._buttons = None
        self._on_playback_position_changed.subject = self.song()
        self._on_playing_state_changed.subject = self.song()
        return

    def disconnect(self):
        super(VisualMetroComponent, self).disconnect()
        self._buttons = None
        return

    def set_visual_metro_buttons(self, buttons):
        """ Sets the list of buttons to use for displaying the visual metronome.
        Needs to be at least 4 buttons. The first button can be used for toggling
        playback state. """
        assert buttons is None or len(buttons) >= 4
        self._buttons = list(buttons) if buttons else None
        self._on_visual_metro_button_value.replace_subjects(buttons or [])
        self._last_visual_metro_led = None
        set_group_button_lights(self._buttons, 'VisualMetronome.Off')
        return

    @subject_slot_group('value')
    def _on_visual_metro_button_value(self, value, button):
        if value:
            btn_index = self._buttons.index(button)
            if btn_index == 0:
                self.song().is_playing = not self.song().is_playing

    def update(self):
        super(VisualMetroComponent, self).update()
        if self.is_enabled():
            set_group_button_lights(self._buttons, 'VisualMetronome.Off')

    @subject_slot('is_playing')
    def _on_playing_state_changed(self):
        self._on_playback_position_changed()

    @subject_slot('current_song_time')
    def _on_playback_position_changed(self):
        """ Displays the visual metronome. """
        if self.is_enabled() and self._buttons:
            if self.song().is_playing:
                beat = self.song().get_current_beats_song_time().beats - 1
                if self._last_beat != beat:
                    self._last_beat = beat
                    self._clear_last_visual_metro_led()
                    if self._last_beat < len(self._buttons):
                        btn = self._buttons[self._last_beat]
                        if btn:
                            btn.set_light('VisualMetronome.%s' % ('Beat' if self._last_beat else 'Bar'))
                            self._last_visual_metro_led = self._buttons[self._last_beat]
                    else:
                        btn = self._buttons[(-1)]
                        if btn:
                            self._buttons[(-1)].set_light('VisualMetronome.Beat')
                            self._last_visual_metro_led = self._buttons[(-1)]
            else:
                self._clear_last_visual_metro_led()

    def _clear_last_visual_metro_led(self):
        if self.is_enabled() and self._buttons and self._last_visual_metro_led:
            self._last_visual_metro_led.set_light('VisualMetronome.Off')
        self._last_visual_metro_led = None
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/VisualMetroComponent.pyc
