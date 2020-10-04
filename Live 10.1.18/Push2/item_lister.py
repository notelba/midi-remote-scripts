# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\item_lister.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ItemListerComponent as ItemListerComponentBase, ItemSlot, SimpleItemSlot

class IconItemSlot(SimpleItemSlot):

    def __init__(self, icon=b'', *a, **k):
        super(IconItemSlot, self).__init__(*a, **k)
        self._icon = icon

    @property
    def icon(self):
        return self._icon


class ItemListerComponent(ItemListerComponentBase):

    def _create_slot(self, index, item, nesting_level):
        items = self._item_provider.items[self.item_offset:]
        num_slots = min(self._num_visible_items, len(items))
        slot = None
        if index == 0 and self.can_scroll_left():
            slot = IconItemSlot(icon=b'page_left.svg')
            slot.is_scrolling_indicator = True
        elif index == num_slots - 1 and self.can_scroll_right():
            slot = IconItemSlot(icon=b'page_right.svg')
            slot.is_scrolling_indicator = True
        else:
            slot = ItemSlot(item=item, nesting_level=nesting_level)
            slot.is_scrolling_indicator = False
        return slot
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/item_lister.pyc
