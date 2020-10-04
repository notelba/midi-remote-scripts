# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40_MkII\BankToggleComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ComboElement import ToggleElement
from _Framework.Control import ToggleButtonControl
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class BankToggleComponent(ControlSurfaceComponent):
    bank_toggle_button = ToggleButtonControl()

    def __init__(self, *a, **k):
        super(BankToggleComponent, self).__init__(*a, **k)
        self._toggle_elements = []

    @bank_toggle_button.toggled
    def bank_toggle_button(self, toggled, button):
        for e in self._toggle_elements:
            e.set_toggled(toggled)

    def create_toggle_element(self, *a, **k):
        element = ToggleElement(*a, **k)
        element.toggled = self.bank_toggle_button.is_toggled
        self._toggle_elements.append(element)
        return element
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC40_MkII/BankToggleComponent.pyc
