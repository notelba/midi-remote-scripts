# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\optional.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ...base import listens
from .combo import ToggleElement

class ChoosingElement(ToggleElement):
    """
    An Element wrapper that enables one of the nested elements based on
    the value of the given flag.
    """

    def __init__(self, flag=None, *a, **k):
        super(ChoosingElement, self).__init__(*a, **k)
        self.__on_flag_changed.subject = flag
        self.__on_flag_changed(flag.value)

    @listens(b'value')
    def __on_flag_changed(self, value):
        self.set_toggled(value)


class OptionalElement(ChoosingElement):
    """
    An Element wrapper that enables the nested element IFF some given
    flag is set to a specific value.
    """

    def __init__(self, control=None, flag=None, value=None, *a, **k):
        on_control = control if value else None
        off_control = None if value else control
        super(OptionalElement, self).__init__(on_control=on_control, off_control=off_control, flag=flag, *a, **k)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ableton/v2/control_surface/elements/optional.pyc
