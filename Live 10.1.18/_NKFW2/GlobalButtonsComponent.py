# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\GlobalButtonsComponent.py
# Compiled at: 2017-03-07 13:28:52
import Live
GQ = Live.Song.Quantization
RQ = Live.Song.RecordingQuantization
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from ShowMessageMixin import ShowMessageMixin, DisplayType
from SpecialControl import SpecialButtonControl
from ResettableScrollComponent import ScrolledProperty
from consts import RECORD_QUANTIZE_NAMES
MULTI_SCROLL_FACTORS = {'Tempo': {'name': 'tempo', 'min': 20.0, 'max': 999.0, 'def': 120.0, 
             'factor': 1.0}, 
   'Tempo Fine': {'name': 'tempo', 'min': 20.0, 'max': 999.0, 'def': 120.0, 
                  'factor': 0.1}, 
   'Global Quantize': {'name': 'clip_trigger_quantization', 'min': 0, 'max': 13, 'def': 4, 
                       'factor': 1}, 
   'Record Quantize': {'name': 'midi_recording_quantization', 'min': 0, 'max': 8, 'def': 5, 
                       'factor': 1}, 
   'Fixed Length': {'name': 'num_bars', 'min': 1, 'max': 32, 'def': 2, 
                    'factor': 1}}

class GlobalButtonsComponent(CompoundComponent, ShowMessageMixin):
    """ GlobalButtonsComponent provides a set of multi-scroll buttons that can control
    various properties depending on the state of other buttons, which themselves can
    also be used to toggle properties on/off if pressed quickly. """
    global_quantize_button = SpecialButtonControl()
    record_quantize_button = SpecialButtonControl()
    fixed_length_button = SpecialButtonControl()

    def __init__(self, clip_creator=None, scroll_color='DefaultButton.On', *a, **k):
        super(GlobalButtonsComponent, self).__init__(*a, **k)
        self.is_private = True
        self._should_display_record_quantization = False
        self._last_global_quantization = GQ.q_bar
        self._last_record_quantization = RQ.rec_q_sixtenth
        self._clip_creator = clip_creator
        self._scroll_color = scroll_color
        self._multi_scroll = self.register_component(ScrolledProperty(scroll_color, 'tempo', 20.0, 999.0, 120.0, factor=1.0))
        self._multi_scroll.set_object(self.song())
        self._on_global_quantize_changed.subject = self.song()
        self._on_record_quantize_changed.subject = self.song()
        self._on_fixed_length_enabled_changed.subject = clip_creator

    def disconnect(self):
        super(GlobalButtonsComponent, self).disconnect()
        self._clip_creator = None
        self._multi_scroll = None
        return

    def set_physical_display_element(self, element):
        """ Extends standard to set display element of clip creator. """
        super(GlobalButtonsComponent, self).set_physical_display_element(element)
        if self._clip_creator:
            self._clip_creator.set_physical_display_element(element)

    def set_shift_button(self, button):
        """ Sets the shift button used for switching between fine and coarse tempo
        adjustment. """
        self._on_shift_button_value.subject = button

    def set_decrease_button(self, button):
        """ Sets the multi-scroll's decrease button. """
        if self._multi_scroll:
            self._multi_scroll.set_scroll_down_button(button)

    def set_increase_button(self, button):
        """ Sets the multi-scroll's increase button. """
        if self._multi_scroll:
            self._multi_scroll.set_scroll_up_button(button)

    def set_default_scroll_color(self, color):
        """ Sets the default LED color to use for multi-scroll. """
        self._scroll_color = color

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        """ Toggles between coarse and fine tempo adjustment. """
        self._update_multi_scroll('Tempo Fine' if value else 'Tempo')

    @global_quantize_button.released_immediately
    def global_quantize_button(self, _):
        """ Toggles global quantization. """
        is_on = self.song().clip_trigger_quantization != GQ.q_no_q
        if is_on:
            self._last_global_quantization = self.song().clip_trigger_quantization
            self.song().clip_trigger_quantization = GQ.q_no_q
        else:
            self.song().clip_trigger_quantization = self._last_global_quantization

    @global_quantize_button.pressed_delayed
    def global_quantize_button(self, _):
        """ Sets multi-scroll to control global quantization. """
        self._update_multi_scroll('Global Quantize', self.global_quantize_button)

    @global_quantize_button.released_delayed
    def global_quantize_button(self, _):
        """ Reverts multi-scroll to tempo. """
        self._update_multi_scroll()

    @global_quantize_button.pressed
    def global_quantize_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    @record_quantize_button.released_immediately
    def record_quantize_button(self, _):
        """ Toggles record quantization.  This uses a hack to properly display the new
        setting. """
        self._should_display_record_quantization = True
        is_on = self.song().midi_recording_quantization != RQ.rec_q_no_q
        if is_on:
            self._last_record_quantization = self.song().midi_recording_quantization
            self.song().midi_recording_quantization = RQ.rec_q_no_q
            self._on_record_quantize_changed(0)
        else:
            self.song().midi_recording_quantization = self._last_record_quantization
            self._on_record_quantize_changed(int(self._last_record_quantization))
        self._should_display_record_quantization = False

    @record_quantize_button.pressed_delayed
    def record_quantize_button(self, _):
        """ Sets multi-scroll to control record quantization. """
        self._should_display_record_quantization = True
        self._update_multi_scroll('Record Quantize', self.record_quantize_button)

    @record_quantize_button.released_delayed
    def record_quantize_button(self, _):
        """ Reverts multi-scroll to tempo. """
        self._should_display_record_quantization = False
        self._update_multi_scroll()

    @record_quantize_button.pressed
    def record_quantize_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    @fixed_length_button.released_immediately
    def fixed_length_button(self, _):
        """ Toggles fixed length. """
        if self._clip_creator:
            self._clip_creator.fixed_length_enabled = not self._clip_creator.fixed_length_enabled

    @fixed_length_button.pressed_delayed
    def fixed_length_button(self, _):
        """ Sets multi-scroll to control fixed length. """
        self._update_multi_scroll('Fixed Length', self.fixed_length_button)

    @fixed_length_button.released_delayed
    def fixed_length_button(self, _):
        """ Reverts multi-scroll to tempo. """
        self._update_multi_scroll()

    @fixed_length_button.pressed
    def fixed_length_button(self, _):
        """ Unused, but needed when using release_delayed. """
        pass

    def update(self):
        super(GlobalButtonsComponent, self).update()
        self._should_display_record_quantization = False
        self._update_multi_scroll(should_display=False)
        self._on_global_quantize_changed()
        self._on_record_quantize_changed()
        self._on_fixed_length_enabled_changed()

    def _update_multi_scroll(self, scroll_type='Tempo', button=None, should_display=True):
        """ Updates the object that multi-scroll should control and displays its
        current assignment. """
        msf = MULTI_SCROLL_FACTORS[scroll_type]
        if scroll_type == 'Fixed Length':
            self._multi_scroll.set_object(self._clip_creator or None)
        else:
            self._multi_scroll.set_object(self.song())
        self._multi_scroll.set_property_name(msf['name'])
        self._multi_scroll.set_min_and_max_values(msf['min'], msf['max'])
        self._multi_scroll.set_default_value(msf['def'])
        self._multi_scroll.set_adjustment_factor(msf['factor'])
        self._multi_scroll.set_color(button.on_color if button else self._scroll_color)
        if should_display:
            self.component_message('Multi-Scroll assigned to', scroll_type, display_type=DisplayType.STATUS)
            self.component_message('Multi-Scroll', scroll_type, display_type=DisplayType.PHYSICAL)
        return

    @subject_slot('clip_trigger_quantization')
    def _on_global_quantize_changed(self):
        if self.is_enabled():
            self.global_quantize_button.is_on = self.song().clip_trigger_quantization != GQ.q_no_q

    @subject_slot('midi_recording_quantization')
    def _on_record_quantize_changed(self, value=None):
        if self.is_enabled():
            value = value if value is not None else int(self.song().midi_recording_quantization)
            self.record_quantize_button.is_on = value != 0
            if self._should_display_record_quantization:
                name = 'None'
                if value > 0:
                    name = RECORD_QUANTIZE_NAMES[(value - 1)]
                self.component_message('Record Quantize', name)
        return

    @subject_slot('fixed_length_enabled')
    def _on_fixed_length_enabled_changed(self):
        if self.is_enabled():
            self.fixed_length_button.is_on = self._clip_creator and self._clip_creator.fixed_length_enabled
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/GlobalButtonsComponent.pyc
