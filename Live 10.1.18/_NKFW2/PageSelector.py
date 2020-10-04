# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\_NKFW2\PageSelector.py
# Compiled at: 2017-09-30 15:26:23
from _Framework.SubjectSlot import SlotManager, Subject, subject_slot
from SpecialControl import RadioButtonGroup
PAGE_BTN_OFF_POS = 0
PAGE_BTN_ON_POS = 1

class Pageable(Subject):
    """ Pageable is an interface for an object that has pages that can be selected and/or
    navigated between. """
    __subject_events__ = ('page_index', )

    def __init__(self, num_pages=1):
        super(Pageable, self).__init__()
        self._num_pages = num_pages
        self._page_index = 0

    def can_select_pages(self):
        """ Returns whether or not pages can be selected.  This doesn't need to be
        implemented unless there are cases where pages cannot be selected. """
        return True

    def increment_page(self, factor, roundtrip=False):
        """ Increments to the next/prev page by the given factor. """
        new_index = self.get_index_to_increment() + factor
        if new_index in xrange(self.num_pages):
            self.set_page_index(new_index)
        elif factor > 0 and roundtrip:
            self.set_page_index(0)

    def set_page_index(self, index):
        """ Sets the page index directly. """
        if index in xrange(self._num_pages):
            self.handle_set_page_index(index)
            self._page_index = index
            self.notify_page_index()

    def _get_page_index(self):
        return self._page_index

    page_index = property(_get_page_index, set_page_index)

    def get_index_to_increment(self):
        """ Returns the index to increment, which will typically just
        be the _page_index, but subclasses may need to change. """
        return self._page_index

    def handle_set_page_index(self, index):
        """ Handles additional tasks that need to be performed
        when the page index changes. """
        pass

    @property
    def num_pages(self):
        """ Returns the number of pages available. """
        return self._num_pages


class PageableObjectProperty(Pageable):
    """ PageableObjectProperty is a Pageable meant
    to be used for selecting between values of a
    property of an object. This will not allow selection
    if the object doesn't exist. """

    def __init__(self, num_pages, prop_name):
        self._object = None
        self._prop_name = prop_name
        super(PageableObjectProperty, self).__init__(num_pages)
        return

    def disconnect(self):
        super(PageableObjectProperty, self).disconnect()
        self._object = None
        self._prop_name = None
        return

    def set_object(self, obj):
        """ Set the object associated with the property. """
        self._object = obj

    def can_select_pages(self):
        return self._object is not None

    def get_index_to_increment(self):
        return getattr(self._object, self._prop_name)

    def handle_set_page_index(self, index):
        setattr(self._object, self._prop_name, index)

    @property
    def object(self):
        return self._object

    @property
    def page_index(self):
        if self._object:
            return getattr(self._object, self._prop_name)
        else:
            return

    @property
    def num_pages(self):
        return self._num_pages


class PageSelector(SlotManager):
    """  PageSelector allows for using a set of prev/next buttons to increment between
    pages and/or a group of buttons to directly select pages of a Pageable object.

    Note that this does not do scrolling.  If scrolling is needed, use
    ScrollComponent from the Framework."""
    button_group_type = RadioButtonGroup

    def __init__(self, pageable, page_button_led_values=('DefaultButton.Disabled', 'Pages.NotSelected', 'Pages.Selected'), page_nav_led_values=('DefaultButton.Off', 'Navigation.PageEnabled'), *a, **k):
        assert isinstance(page_button_led_values, tuple)
        assert isinstance(page_nav_led_values, tuple)
        super(PageSelector, self).__init__(*a, **k)
        self._pageable = pageable
        self._page_nav_led_values = page_nav_led_values
        self._page_buttons = self.button_group_type(num_buttons=self._pageable.num_pages, checked_color=page_button_led_values[2], unchecked_color=page_button_led_values[1], disabled_color=page_button_led_values[0])
        self._on_page_button_value.subject = self._page_buttons

    def disconnect(self):
        super(PageSelector, self).disconnect()
        self._pageable = None
        self._page_nav_led_values = None
        self._page_buttons = None
        return

    def set_page_buttons(self, buttons):
        """ Sets the button to use for directly selecting pages. """
        self._page_buttons.set_buttons(buttons)

    def set_prev_page_button(self, button):
        """ Sets the button to use for navigating to the previous page. """
        self._on_prev_page_button_value.subject = button if button else None
        self._update_page_nav_leds()
        return

    def set_next_page_button(self, button):
        """ Sets the button to use for navigating to the next page. If this is assigned
        on its own (without a prev_page_button) then roundtrip paging will be used. """
        self._on_next_page_button_value.subject = button if button else None
        self._update_page_nav_leds()
        return

    def set_enabled(self, enable):
        """ Sets the enabled state of the RadioButtonGroup and updates. """
        self._page_buttons.set_enabled(enable)
        self.update()

    def _set_enabled_recursive(self, enable):
        """ Sets the component's enabled state for use with CompoundComponents. """
        self.set_enabled(enable)

    def update(self):
        self._update_page_nav_leds()
        self._page_buttons.set_checked_index(self._pageable.page_index)
        self._page_buttons.update()

    def _use_roundtrip_paging(self):
        """ Returns whether or not roundtrip paging will be used. """
        return self._on_prev_page_button_value.subject is None

    @subject_slot('checked_index')
    def _on_page_button_value(self, index):
        if self._pageable.can_select_pages():
            self._pageable.set_page_index(index)

    @subject_slot('value')
    def _on_prev_page_button_value(self, value):
        if value and self._pageable.can_select_pages():
            self._pageable.increment_page(-1, self._use_roundtrip_paging())

    @subject_slot('value')
    def _on_next_page_button_value(self, value):
        if value and self._pageable.can_select_pages():
            self._pageable.increment_page(1, self._use_roundtrip_paging())

    def _update_page_nav_leds(self):
        next_button = self._on_next_page_button_value.subject
        prev_button = self._on_prev_page_button_value.subject
        if self._pageable.can_select_pages():
            page_index = self._pageable.page_index
            if prev_button:
                prev_pos = PAGE_BTN_ON_POS if page_index > 0 else PAGE_BTN_OFF_POS
                prev_button.set_light(self._page_nav_led_values[prev_pos])
                if next_button:
                    next_pos = PAGE_BTN_ON_POS if page_index + 1 < self._pageable.num_pages else PAGE_BTN_OFF_POS
                    next_button.set_light(self._page_nav_led_values[next_pos])
            elif next_button:
                next_button.set_light(self._page_nav_led_values[PAGE_BTN_ON_POS])
        else:
            if prev_button:
                prev_button.set_light(self._page_nav_led_values[PAGE_BTN_OFF_POS])
            if next_button:
                next_button.set_light(self._page_nav_led_values[PAGE_BTN_OFF_POS])


class PagedProperty(PageSelector):
    """ Simple object that combines a PageSelector and PageableObjectProperty to allow
    for ease of use, particularly in CompoundComponents. """

    def __init__(self, prop_name, num_prop_values, page_button_led_values, page_nav_led_values):
        super(PagedProperty, self).__init__(PageableObjectProperty(num_prop_values, prop_name), page_button_led_values=page_button_led_values, page_nav_led_values=page_nav_led_values)

    def set_object(self, obj):
        """ Sets the pageable's object. """
        self._pageable.set_object(obj)

    def update(self):
        super(PagedProperty, self).update()
        self._page_buttons.set_enabled(self._pageable.object is not None)
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_NKFW2/PageSelector.pyc
