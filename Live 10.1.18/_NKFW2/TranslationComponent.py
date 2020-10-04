# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\TranslationComponent.py
# Compiled at: 2017-03-07 13:28:53
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import CallableSubjectSlotGroup
from _Framework.Util import nop

class TranslationType(object):
    """ The type of translation to use. """
    CHANNEL = 0
    IDENTIFIERS = 1
    BOTH = 2


CHANNEL_BASED = (
 TranslationType.CHANNEL, TranslationType.BOTH)
ID_BASE = (TranslationType.IDENTIFIERS, TranslationType.BOTH)

class TranslationComponent(ControlSurfaceComponent):
    """ Simple component that translates the MIDI channel and/or identifiers of
    a control, group of controls or several of each and can also enable/disable the
    controls. """

    def __init__(self, translation_type=TranslationType.CHANNEL, channel=0, ids={}, should_enable_controls=True, *a, **k):
        assert channel in xrange(16)
        self._translation_type = translation_type
        self._channel = channel
        self._ids = ids
        self._should_enable_controls = bool(should_enable_controls)
        self._control_map = {}
        self._slot_map = {}
        super(TranslationComponent, self).__init__(*a, **k)
        self.is_private = True

    def disconnect(self):
        for slot in self._slot_map:
            if slot:
                self.disconnect_disconnectable(slot)

        super(TranslationComponent, self).disconnect()
        self._ids = None
        return

    def __getattr__(self, name):
        if len(name) > 4 and name[:4] == 'set_':
            return partial(self._set_control, name[4:])

    def _set_control(self, name, control):
        current_slot = self._slot_map.get(name, None)
        if current_slot is not None:
            del self._slot_map[name]
            self.disconnect_disconnectable(current_slot)
        if control:
            try:
                self._control_map[name] = list(control)
            except:
                self._control_map[name] = [
                 control]

            if self._should_enable_controls:
                slot = CallableSubjectSlotGroup(event='value', listener=nop, function=nop)
                self.register_slot_manager(slot)
                self._slot_map[name] = slot
                slot.replace_subjects(self._control_map[name])
            self._translate_control_list(self._control_map[name], name)
        else:
            current_control = self._control_map.get(name, None)
            if current_control:
                self._revert_control_list(current_control)
            del self._control_map[name]
        return

    def _translate_control_list(self, control_list, name):
        """ Performs the actual translation. """
        for index, control in enumerate(control_list):
            if control:
                control.set_enabled(self._should_enable_controls)
                if self._translation_type in CHANNEL_BASED:
                    control.set_channel(self._channel)
                if self._translation_type in ID_BASE and name in self._ids:
                    control.set_identifier(self._ids[name][index])
                control.reset()

    @staticmethod
    def _revert_control_list(control_list):
        """ Reverts the given controls back to their default settings. """
        for control in control_list:
            if control:
                control.set_enabled(True)
                control.use_default_message()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/TranslationComponent.pyc
