# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\BackgroundComponent.py
# Compiled at: 2017-03-07 13:28:52
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.Util import nop

class BackgroundComponent(ControlSurfaceComponent):
    """
    This component resets and adds a no-op listener to every control
    that it receives via arbitrary set_* methods.  It is specially
    useful to give it a layer with every control and low priority such
    that it prevents leaking LED lights or midi notes slipping into
    the midi track.

    This is from the 9.1.5 Framework. Listeners were removed in 9.2.
    """

    def __init__(self, *a, **k):
        super(BackgroundComponent, self).__init__(*a, **k)
        self._control_slots = {}
        self._control_map = {}

    def disconnect(self):
        for slot in self._control_slots:
            if slot:
                self.disconnect_disconnectable(slot)

        super(BackgroundComponent, self).disconnect()

    def __getattr__(self, name):
        if len(name) > 4 and name[:4] == 'set_':
            return partial(self._clear_control, name[4:])

    def _clear_control(self, name, control):
        slot = self._control_slots.get(name, None)
        if slot:
            del self._control_slots[name]
            self.disconnect_disconnectable(slot)
        if control:
            self._reset_control(control)
            self._control_map[name] = control
            self._control_slots[name] = self.register_slot(control, lambda *a, **k: nop(control, *a, **k), 'value')
        elif name in self._control_map:
            del self._control_map[name]
        return

    @staticmethod
    def _reset_control(control):
        control.reset()

    def update(self):
        super(BackgroundComponent, self).update()
        if self.is_enabled():
            for control in self._control_map.itervalues():
                self._reset_control(control)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/BackgroundComponent.pyc
