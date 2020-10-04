# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\ShowMessageMixin.py
# Compiled at: 2017-03-07 13:28:53
from _Framework.Disconnectable import Disconnectable

class DisplayType(object):
    """ The types of displays that should be shown.
    BOTH - displays in status bar and physical display.
    STATUS - displays in status bar only.
    PHYSICAL - display in physical display only. """
    BOTH = 0
    STATUS = 1
    PHYSICAL = 2


class ShowMessageMixin(Disconnectable):
    """ Simple object that aims to help standardize messages shown in the status bar
    and on a physical display element. """

    def __init__(self):
        self._display_element = None
        super(ShowMessageMixin, self).__init__()
        return

    def disconnect(self):
        super(ShowMessageMixin, self).disconnect()
        self._display_element = None
        return

    def set_physical_display_element(self, element):
        """ Sets the physical display element to use for showing messages. """
        self._display_element = element

    def component_message(self, header, value='', header_2='', value_2='', display_type=DisplayType.BOTH, **k):
        """ Shows a message using a ControlSurfaceComponent's _show_msg_callback. """
        self._show_msg(self._show_msg_callback, header, value, header_2, value_2, display_type, **k)

    def surface_message(self, header, value='', header_2='', value_2='', display_type=DisplayType.BOTH, **k):
        """ Shows a message using the ControlSurface's show_message. """
        self._show_msg(self.show_message, header, value, header_2, value_2, display_type, is_priority=True, **k)

    def _show_msg(self, method, header, value, header_2, value_2, display_type, **k):
        physical_method = self._notify_physical_display_element
        if display_type == DisplayType.PHYSICAL:
            method = lambda *a: None
        elif display_type == DisplayType.STATUS:
            physical_method = lambda *a, **k: None
        if value is not '':
            header += ':'
        if header_2 is not '':
            if value_2 is not '':
                header_2 += ':'
            physical_method(header, value, header_2, value_2, **k)
            method('%s  %s  -  %s  %s' % (header, value, header_2, value_2))
        else:
            physical_method(header, value, **k)
            method('%s  %s' % (header, value))

    def _notify_physical_display_element(self, *a, **k):
        if self._display_element:
            self._display_element.show_message(*a, **k)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/ShowMessageMixin.pyc
