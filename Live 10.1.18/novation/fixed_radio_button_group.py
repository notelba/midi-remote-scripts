# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\fixed_radio_button_group.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import RadioButtonGroup

class FixedRadioButtonGroup(RadioButtonGroup):
    """
    RadioButtonGroup of a fixed size that always listens to the controls it's given to
    prevent unused controls from leaking into the track input.  Use active_control_count
    instead of control_count to set the number of controls that should be active in the
    group. Inactive controls will be disabled.
    """

    def __init__(self, control_count, *a, **k):
        super(FixedRadioButtonGroup, self).__init__(control_count=control_count, *a, **k)

    class State(RadioButtonGroup.State):

        @property
        def active_control_count(self):
            return self._active_control_count

        @active_control_count.setter
        def active_control_count(self, control_count):
            self._active_control_count = control_count
            for index, control in enumerate(self._controls):
                control._get_state(self._manager).enabled = index < control_count
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/fixed_radio_button_group.pyc
