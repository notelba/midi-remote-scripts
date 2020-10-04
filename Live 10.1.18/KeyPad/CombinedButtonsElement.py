# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyPad\CombinedButtonsElement.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from itertools import imap
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ButtonElement import OFF_VALUE
from _Framework.Util import const, BooleanContext

class CombinedButtonsElement(ButtonMatrixElement):

    def __init__(self, buttons=None, *a, **k):
        super(CombinedButtonsElement, self).__init__(rows=[buttons], *a, **k)
        self._is_pressed = BooleanContext(False)

    def is_momentary(self):
        return True

    def is_pressed(self):
        return any(imap(lambda (b, _): b.is_pressed() if b is not None else False, self.iterbuttons())) or bool(self._is_pressed)

    def on_nested_control_element_value(self, value, sender):
        with self._is_pressed():
            self.notify_value(value)
        if value != OFF_VALUE and not getattr(sender, b'is_momentary', const(False))():
            self.notify_value(OFF_VALUE)

    def send_value(self, value):
        for button, _ in self.iterbuttons():
            if button:
                button.send_value(value)

    def set_light(self, value):
        for button, _ in self.iterbuttons():
            if button:
                button.set_light(value)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyPad/CombinedButtonsElement.pyc
