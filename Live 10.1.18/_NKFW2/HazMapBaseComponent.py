# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\HazMapBaseComponent.py
# Compiled at: 2017-05-19 14:00:53
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from _Framework.Util import nop
from PageSelector import PageSelector, Pageable
from ControlUtils import release_parameters
from Utils import live_object_is_valid

class HazMapBaseComponent(CompoundComponent, Pageable):
    """ HazMapBaseComponent is the base class for all HazMapComponents and provides the
    basic functionality they all share in common. Note that these components can be used
    for HazMapping (user-assignable) or for static parameter assignments. """
    __subject_events__ = ('assignments', 'page_names')

    def __init__(self, manager, num_controls_or_pages=8, *a, **k):
        super(HazMapBaseComponent, self).__init__(*a, **k)
        self._get_parameter_method = manager.get_assigned_track_parameter
        self._on_update_connections_method = lambda : None
        self._dev_dict = None
        self._assignments = [ None for _ in xrange(num_controls_or_pages) ]
        self._page_names = [ None for _ in xrange(num_controls_or_pages) ]
        self._controls = None
        self._control_slots = []
        self._manager = manager
        self._num_pages = num_controls_or_pages
        self._update_control_connections.subject = manager
        self._page_selector = self.register_component(PageSelector(self))
        self._on_page_changed.subject = self
        return

    def disconnect(self):
        super(HazMapBaseComponent, self).disconnect()
        self._manager.disconnect()
        self._get_parameter_method = None
        self._on_update_connections_method = None
        self._dev_dict = None
        self._assignments = None
        self._controls = None
        return

    def set_control(self, control):
        """ Sets the control to use for controlling assigned parameters. """
        release_parameters(self._controls)
        self._controls = [control] if control else []
        self._update_control_connections()

    def set_page_buttons(self, buttons):
        """ Sets the group of buttons to use for navigating between pages. """
        self._page_selector.set_page_buttons(buttons)

    def set_multi_device_dict(self, dev_dict):
        """ Sets the multi-device dict to use.  If this is set, get_parameter_method will
        be overridden. The dict should be in the form:
        {dev1_class_name: {'instance_name': name, 'parameters': param_list},
         dev2_class_name: {'instance_name': name, 'parameters': param_list}, etc} """
        self._dev_dict = dev_dict

    def set_get_parameter_method(self, method):
        """ Sets the method to use for retrieving the parameter to assign to the
        control. """
        self._get_parameter_method = method

    def set_on_update_connections_method(self, method):
        """ Sets the method to call when assignments have been changed. """
        self._on_update_connections_method = method

    def _set_assignments(self, assignments):
        """ Sets all the assignments to use. """
        self._assignments = assignments
        self._update_control_connections()

    def _get_assignments(self):
        """ Returns a list of the assignments to use. """
        return self._assignments

    assignments = property(_get_assignments, _set_assignments)

    def _set_page_names(self, page_names):
        """ Sets all the page names to use. """
        self._page_names = page_names
        self.notify_page_names()

    def _get_page_names(self):
        """ Returns a list of the page names to use. """
        return self._page_names

    page_names = property(_get_page_names, _set_page_names)

    @property
    def current_page_name(self):
        """ Returns the name of the current page. """
        return self._page_names[self._page_index]

    @subject_slot('page_index')
    def _on_page_changed(self):
        self._update_control_connections()

    def update(self):
        super(HazMapBaseComponent, self).update()
        self._update_control_connections()
        self._page_selector.update()

    @subject_slot('devices')
    def _update_control_connections(self, track_changed=False):
        if self.is_enabled():
            release_parameters(self._controls)
            for slot in self._control_slots:
                self.disconnect_disconnectable(slot)

            del self._control_slots[:]
            if self._controls:
                self._on_update_connections_method()
                for i, control in enumerate(self._controls):
                    if control:
                        param = self._get_parameter(i)
                        if live_object_is_valid(param):
                            control.connect_to(param)
                        else:
                            self._register_slot_for_control(control)

    def _get_parameter(self, i):
        """ This is broken out so that it can be overridden. """
        p_id = i + self._page_index
        if self._dev_dict:
            return self._manager.get_multi_device_track_parameter(self._dev_dict, p_id)
        return self._get_parameter_method(self._assignments[p_id])

    def _register_slot_for_control(self, control):
        if control:
            slot = self.register_slot(control, lambda *a, **k: nop(control, *a, **k), 'value')
            self._control_slots.append(slot)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/HazMapBaseComponent.pyc
