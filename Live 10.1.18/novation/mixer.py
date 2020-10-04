# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\mixer.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import izip_longest
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase

class MixerComponent(MixerComponentBase):

    def __getattr__(self, name):
        """
        Extends standard to handle arbitrary set_x_control or set_x_display methods
        needed by channel_strips. This assumes that the set methods will be used in
        conjunction with Controls that have a set_control_element method.

        For example, if channel_strips have a Control named my_control. The control
        element for those Controls could be set by calling set_my_controls on this
        component.
        """
        if name.startswith(b'set_') and (name.endswith(b'controls') or name.endswith(b'displays')) and not getattr(self, name[4:], None):
            return partial(self._set_controls_on_all_channel_strips, name[4:-1])
        else:
            raise AttributeError
            return

    def _set_controls_on_all_channel_strips(self, attr_name, controls):
        for strip, control in izip_longest(self._channel_strips, controls or []):
            getattr(strip, attr_name).set_control_element(control)

    def set_static_color_value(self, value):
        for strip in self._channel_strips:
            strip.set_static_color_value(value)

    def set_send_a_controls(self, controls):
        self._set_send_controls(controls, 0)

    def set_send_b_controls(self, controls):
        self._set_send_controls(controls, 1)

    def _set_send_controls(self, controls, send_index):
        if controls:
            for index, control in enumerate(controls):
                if control:
                    self.channel_strip(index).set_send_controls((None, ) * send_index + (control,))

        else:
            for strip in self._channel_strips:
                strip.set_send_controls(None)

        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/mixer.pyc
