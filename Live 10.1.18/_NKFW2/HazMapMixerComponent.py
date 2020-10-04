# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\HazMapMixerComponent.py
# Compiled at: 2017-03-07 13:28:52
from _Framework.CompoundComponent import CompoundComponent
from HazMapBaseComponent import HazMapBaseComponent, subject_slot
from HazMapTrackComponent import HazMapTrackComponent
from ShowMessageMixin import ShowMessageMixin, DisplayType

class HazMapMixerComponent(CompoundComponent, ShowMessageMixin):
    """ HazMapMixerComponent works with the TrackDeviceMixerManager to control
    a group of HazMapBaseComponents and a HazMapTrackComponent, each assigned to a
    different track. """
    __subject_events__ = ('assignments', 'page_names', 'page_index')

    def __init__(self, mixer_manager, targets_comp=None, num_tracks=8, num_pages=8, handle_shift_led=False, name='HazMap_Mixer', *a, **k):
        super(HazMapMixerComponent, self).__init__(name=name, *a, **k)
        self._can_display_page_info = True
        self._display_header = 'Page'
        self._num_tracks = num_tracks
        self._components = []
        mixer_manager.set_song(self.song())
        for i in xrange(num_tracks):
            manager = mixer_manager.get_track_manager(i)
            if i == 0:
                comp = HazMapTrackComponent(manager, targets_comp=targets_comp, num_controls_or_pages=num_pages, handle_shift_led=handle_shift_led, name=name)
                comp.set_on_update_connections_method(self._on_assignments_changed)
                comp.set_on_delete_assignments_method(self._on_assignments_changed)
                self._notify_subjects_of_assignment_changes.subject = comp
                self._notify_subjects_of_page_names_changes.subject = comp
                self._on_page_changed.subject = comp
            else:
                comp = HazMapBaseComponent(manager, num_controls_or_pages=num_pages)
            comp.is_private = True
            self._components.append(comp)
            self.register_component(comp)

    def set_physical_display_element(self, line):
        """ Extends standard to set display element of first component. """
        super(HazMapMixerComponent, self).set_physical_display_element(line)
        self._components[0].set_physical_display_element(line)

    def set_shift_button(self, button):
        """ Sets the button to use to deactivate all assignments and allow for mapping
        activation/de-activation and assignment deletion. """
        self._components[0].set_shift_button(button)

    def set_controls(self, controls):
        """ Sets the group of controls to use for controlling assigned parameters. """
        assert controls is None or len(controls) == self._num_tracks
        controls = list(controls) if controls else [ None for _ in xrange(self._num_tracks)
                                                   ]
        for i, c in enumerate(self._components):
            c.set_control(controls[i])

        return

    def set_multi_device_dict(self, dev_dict):
        """ Sets the multi-device dict to use for all sub-components. """
        for c in self._components:
            c.set_multi_device_dict(dev_dict)

    def set_page_buttons(self, buttons):
        """ Sets the group of buttons to use for navigating between pages. """
        self._components[0].set_page_buttons(buttons)

    def set_page_index(self, index):
        """ Sets this component's page index. """
        self._components[0].set_page_index(index)

    def set_can_display_page_info(self, can_display):
        """ Sets whether this component will show page info in the status bar. """
        self._can_display_page_info = bool(can_display)

    def _set_display_header(self, header):
        """ Sets the header that will be used when displaying page info in the status
        bar. """
        self._display_header = header

    def _get_display_header(self):
        """ Returns the header to use when displaying page info. """
        return self._display_header

    display_header = property(_get_display_header, _set_display_header)

    def _set_assignments(self, assignments):
        """ Sets all the assignments to use. """
        self._components[0].assignments = assignments

    def _get_assignments(self):
        """ Returns a list of the assignments to use. """
        return self._components[0].assignments

    assignments = property(_get_assignments, _set_assignments)

    def _set_page_names(self, page_names):
        """ Sets all the page names to use. """
        self._components[0].page_names = page_names

    def _get_page_names(self):
        """ Returns a list of the page names to use. """
        return self._components[0].page_names

    page_names = property(_get_page_names, _set_page_names)

    @property
    def page_index(self):
        """ Returns the current page index. """
        return self._components[0].page_index

    @property
    def current_page_name(self):
        """ Returns the name of the current page. """
        return self._components[0].current_page_name

    @subject_slot('page_index')
    def _on_page_changed(self):
        self.notify_page_index()
        page_index = self._components[0].page_index
        for c in self._components[1:]:
            c.set_page_index(page_index)

        if self._can_display_page_info:
            page_info = page_index + 1
            page_name = self._components[0].page_names[page_index]
            if page_name is not None:
                page_info = page_name
            self.component_message('%s %s' % (self.name, self._display_header), page_info, display_type=DisplayType.STATUS)
            self.component_message(self._display_header, str(page_info), display_type=DisplayType.PHYSICAL)
        return

    @subject_slot('assignments')
    def _notify_subjects_of_assignment_changes(self):
        self.notify_assignments()

    @subject_slot('page_names')
    def _notify_subjects_of_page_names_changes(self):
        self.notify_page_names()

    def _on_assignments_changed(self):
        assigns = self._components[0].assignments
        for c in self._components[1:]:
            c.assignments = assigns
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/HazMapMixerComponent.pyc
