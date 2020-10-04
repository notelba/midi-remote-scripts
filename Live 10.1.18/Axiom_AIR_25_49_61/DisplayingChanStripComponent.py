# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\DisplayingChanStripComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from .consts import *

class DisplayingChanStripComponent(ChannelStripComponent):
    """ Special channel strip class that displays Mute/Solo/Arm state"""

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._name_display = None
        self._value_display = None
        return

    def disconnect(self):
        ChannelStripComponent.disconnect(self)
        self._name_display = None
        self._value_display = None
        return

    def set_name_display(self, name_display):
        self._name_display = name_display

    def set_value_display(self, value_display):
        self._value_display = value_display

    def set_arm_button(self, button):
        assert button == None or isinstance(button, ButtonElement)
        if button != self._arm_button:
            if self._arm_button != None:
                self._arm_button.remove_value_listener(self._arm_value)
                self._arm_button.reset()
            self._arm_pressed = False
            self._arm_button = button
            if self._arm_button != None:
                self._arm_button.add_value_listener(self._arm_value)
            self.update()
        return

    def _on_mute_changed(self):
        if self._mute_button != None:
            if self._track != None and self._track != self.song().master_track:
                self._mute_button.set_on_off_values(AMB_FULL, AMB_LOW)
            else:
                self._mute_button.set_on_off_values(AMB_LOW, LED_OFF)
        ChannelStripComponent._on_mute_changed(self)
        return

    def _on_solo_changed(self):
        if self._solo_button != None:
            if self._track != None and self._track != self.song().master_track:
                self._solo_button.set_on_off_values(AMB_FULL, AMB_LOW)
            else:
                self._solo_button.set_on_off_values(AMB_LOW, LED_OFF)
        ChannelStripComponent._on_solo_changed(self)
        return

    def _on_arm_changed(self):
        if self._arm_button != None:
            if self._track != None and self._track in self.song().tracks:
                self._arm_button.set_on_off_values(RED_FULL, RED_LOW)
            else:
                self._arm_button.set_on_off_values(RED_LOW, LED_OFF)
        ChannelStripComponent._on_arm_changed(self)
        return

    def _mute_value(self, value):
        ChannelStripComponent._mute_value(self, value)
        if self._track != None and self._track != self.song().master_track and self._name_display != None and self._value_display != None:
            if value != 0:
                self._name_display.display_message(b'Mute :')
                self._value_display.send_midi(DISPLAY_WORD_ON) if self._track.mute else self._value_display.send_midi(DISPLAY_WORD_OFF)
        return

    def _solo_value(self, value):
        ChannelStripComponent._solo_value(self, value)
        if self._track != None and self._track != self.song().master_track and self._name_display != None and self._value_display != None:
            if value != 0:
                self._name_display.display_message(b'Solo :')
                self._value_display.send_midi(DISPLAY_WORD_ON) if self._track.solo else self._value_display.send_midi(DISPLAY_WORD_OFF)
        return

    def _arm_value(self, value):
        ChannelStripComponent._arm_value(self, value)
        if self._track != None and self._track != self.song().master_track and self._name_display != None and self._value_display != None and self._track not in self.song().return_tracks:
            if value != 0:
                self._name_display.display_message(b'Arm :')
                self._value_display.send_midi(DISPLAY_WORD_ON) if self._track.arm else self._value_display.send_midi(DISPLAY_WORD_OFF)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_AIR_25_49_61/DisplayingChanStripComponent.pyc
