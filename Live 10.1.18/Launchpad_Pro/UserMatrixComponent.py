# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\UserMatrixComponent.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

def _disable_control(control):
    for button in control:
        button.set_enabled(False)


class UserMatrixComponent(ControlSurfaceComponent):
    """
    "Component" that expects ButtonMatrixElements that hold
    ConfigurableButtonElements, to then turn them off. This
    is done so the buttons' messages can be forwarded to Live's Tracks.
    """

    def __getattr__(self, name):
        if len(name) > 4 and name[:4] == b'set_':
            return _disable_control
        raise AttributeError(name)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro/UserMatrixComponent.pyc
