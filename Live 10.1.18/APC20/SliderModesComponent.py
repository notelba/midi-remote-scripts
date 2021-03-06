# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC20\SliderModesComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent

class SliderModesComponent(ModeSelectorComponent):
    """ SelectorComponent that assigns sliders to different functions """

    def __init__(self, mixer, sliders, *a, **k):
        assert len(sliders) == 8
        super(SliderModesComponent, self).__init__(*a, **k)
        self._mixer = mixer
        self._sliders = sliders
        self._mode_index = 0

    def disconnect(self):
        super(SliderModesComponent, self).disconnect()
        self._mixer = None
        self._sliders = None
        return

    def set_mode_buttons(self, buttons):
        assert isinstance(buttons, (tuple, type(None)))
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                assert isinstance(button, ButtonElement)
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)

        self.update()
        return

    def number_of_modes(self):
        return 8

    def update(self):
        super(SliderModesComponent, self).update()
        if self.is_enabled():
            assert self._mode_index in range(self.number_of_modes())
            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()

            for index in range(len(self._sliders)):
                strip = self._mixer.channel_strip(index)
                slider = self._sliders[index]
                slider.use_default_message()
                slider.set_identifier(slider.message_identifier() - self._mode_index)
                strip.set_volume_control(None)
                strip.set_pan_control(None)
                strip.set_send_controls((None, None, None))
                slider.release_parameter()
                if self._mode_index == 0:
                    strip.set_volume_control(slider)
                elif self._mode_index == 1:
                    strip.set_pan_control(slider)
                elif self._mode_index < 5:
                    send_controls = [
                     None, None, None]
                    send_controls[self._mode_index - 2] = slider
                    strip.set_send_controls(tuple(send_controls))

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC20/SliderModesComponent.pyc
