# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\SongNavigationComponent.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot
from ShowMessageMixin import ShowMessageMixin
from SpecialControl import SpecialButtonControl
from ControlUtils import set_group_button_lights
from Utils import calculate_bar_length

class SongNavigationComponent(ControlSurfaceComponent, ShowMessageMixin):
    """ SongNavigationComponent allows a group of buttons to jump to specific bars
    and includes resettable page navigation so that all bars are accessible. """
    prev_page_button = SpecialButtonControl(color='Navigation.Disabled', on_color='Navigation.PageEnabled')
    next_page_button = SpecialButtonControl(color='Navigation.Disabled', on_color='Navigation.PageEnabled')

    def __init__(self, name='Song_Navigation_Control', *a, **k):
        super(SongNavigationComponent, self).__init__(name=name, *a, **k)
        self._page_offset = 0
        self._last_bar = -1
        self._last_bar_button = None
        self._num_bar_buttons = 0
        self._bar_buttons = None
        self._on_song_time_changed.subject = self.song()
        self._on_numerator_changed.subject = self.song()
        self._on_denominator_changed.subject = self.song()
        return

    def disconnect(self):
        super(SongNavigationComponent, self).disconnect()
        self._bar_buttons = None
        return

    def set_bar_buttons(self, buttons):
        """ Sets the buttons to use for jumping between bars and displaying the bar that's
        playing. """
        self._last_bar = -1
        self._last_bar_button = None
        self._bar_buttons = list(buttons) if buttons else None
        self._num_bar_buttons = len(self._bar_buttons) if buttons else 0
        self._on_bar_button_value.replace_subjects(self._bar_buttons or [])
        set_group_button_lights(self._bar_buttons, 'DefaultButton.Off')
        self._on_song_time_changed()
        return

    @prev_page_button.pressed
    def prev_page_button(self, _):
        self._handle_page_change(-self._num_bar_buttons)

    @next_page_button.pressed
    def next_page_button(self, _):
        self._handle_page_change(self._num_bar_buttons)

    def _handle_page_change(self, factor):
        should_reset = self.prev_page_button.is_pressed and self.next_page_button.is_pressed
        if not should_reset and factor < 0 and self._page_offset == 0:
            return
        if should_reset:
            self._page_offset = 0
        else:
            self._page_offset += factor
        self._last_bar = -1
        self._on_song_time_changed()
        page_range = '%s - %s' % (self._page_offset + 1,
         self._page_offset + self._num_bar_buttons)
        self.component_message('Navigating Bars', page_range)
        self._update_prev_page_button()

    @subject_slot_group('value')
    def _on_bar_button_value(self, value, button):
        if value:
            bar_num = self._bar_buttons.index(button) + self._page_offset
            pos_to_set = calculate_bar_length(self.song()) * bar_num
            if pos_to_set < self.song().song_length:
                self.song().current_song_time = pos_to_set
                self.component_message('Bar', str(bar_num + 1))

    def update(self):
        super(SongNavigationComponent, self).update()
        self._last_bar = -1
        self._on_song_time_changed()
        self._update_prev_page_button()
        self.next_page_button.is_on = True

    @subject_slot('signature_numerator')
    def _on_numerator_changed(self):
        self._last_bar = -1
        self._on_song_time_changed()

    @subject_slot('signature_denominator')
    def _on_denominator_changed(self):
        self._last_bar = -1
        self._on_song_time_changed()

    @subject_slot('current_song_time')
    def _on_song_time_changed(self):
        if self.is_enabled() and self._bar_buttons:
            current_bar = self.song().get_current_beats_song_time().bars - 1
            current_bar -= self._page_offset
            if current_bar in xrange(self._num_bar_buttons):
                if self._last_bar != current_bar:
                    self._clear_last_bar_button()
                    self._bar_buttons[current_bar].set_light('DefaultButton.On')
                    self._last_bar_button = self._bar_buttons[current_bar]
                self._last_bar = current_bar
            elif self._last_bar_button:
                self._clear_last_bar_button()

    def _clear_last_bar_button(self):
        if self.is_enabled() and self._last_bar_button:
            self._last_bar_button.set_light('DefaultButton.Off')
            self._last_bar_button = None
        return

    def _update_prev_page_button(self):
        self.prev_page_button.is_on = self._page_offset != 0
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/SongNavigationComponent.pyc
