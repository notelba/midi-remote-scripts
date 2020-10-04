# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\SelectButtonModeSelector.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.MixerComponent import MixerComponent

class SelectButtonModeSelector(ModeSelectorComponent):
    """ Class that reassigns buttons on the AxiomPro to different mixer functions """

    def __init__(self, mixer, buttons):
        assert isinstance(mixer, MixerComponent)
        assert isinstance(buttons, tuple)
        assert len(buttons) == 8
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._buttons = buttons
        self._mode_display = None
        self._mode_index = 0
        self.update()
        return

    def disconnect(self):
        self._mixer = None
        self._buttons = None
        self._mode_display = None
        return

    def set_mode_display(self, display):
        assert isinstance(display, PhysicalDisplayElement)
        self._mode_display = display

    def number_of_modes(self):
        return 4

    def update(self):
        super(SelectButtonModeSelector, self).update()
        if self.is_enabled():
            for index in range(len(self._buttons)):
                if self._mode_index == 0:
                    self._mixer.channel_strip(index).set_select_button(self._buttons[index])
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_mute_button(None)
                    self._mixer.channel_strip(index).set_solo_button(None)
                elif self._mode_index == 1:
                    self._mixer.channel_strip(index).set_select_button(None)
                    self._mixer.channel_strip(index).set_arm_button(self._buttons[index])
                    self._mixer.channel_strip(index).set_mute_button(None)
                    self._mixer.channel_strip(index).set_solo_button(None)
                elif self._mode_index == 2:
                    self._mixer.channel_strip(index).set_select_button(None)
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_mute_button(self._buttons[index])
                    self._mixer.channel_strip(index).set_solo_button(None)
                elif self._mode_index == 3:
                    self._mixer.channel_strip(index).set_select_button(None)
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_mute_button(None)
                    self._mixer.channel_strip(index).set_solo_button(self._buttons[index])
                else:
                    print(b'Invalid mode index')
                    assert False

        return

    def _toggle_value(self, value):
        assert self._mode_toggle.is_momentary()
        ModeSelectorComponent._toggle_value(self, value)
        if value != 0 and self._mode_display is not None:
            mode_name = b''
            if self._mode_index == 0:
                mode_name = b'Select'
            elif self._mode_index == 1:
                mode_name = b'Arm'
            elif self._mode_index == 2:
                mode_name = b'Mute'
            elif self._mode_index == 3:
                mode_name = b'Solo'
            self._mode_display.display_message(mode_name)
        else:
            self._mode_display.update()
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/AxiomPro/SelectButtonModeSelector.pyc
