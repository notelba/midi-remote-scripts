# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ButtonMatrixElement.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from .CompoundElement import CompoundElement
from .Util import in_range, product, const, slicer, to_slice

class ButtonMatrixElement(CompoundElement):
    """
    Class representing a 2-dimensional set of buttons.

    When using as a resource, buttons might be individually grabbed at
    any time by other components. The matrix will automatically block
    messages coming from or sent to a button owned by them, and will
    return None when you try to query it.
    """

    def __init__(self, rows=[], *a, **k):
        super(ButtonMatrixElement, self).__init__(*a, **k)
        self._buttons = []
        self._orig_buttons = []
        self._button_coordinates = {}
        self._max_row_width = 0
        map(self.add_row, rows)

    @property
    @slicer(2)
    def submatrix(self, col_slice, row_slice):
        col_slice = to_slice(col_slice)
        row_slice = to_slice(row_slice)
        rows = [ row[col_slice] for row in self._orig_buttons[row_slice] ]
        return ButtonMatrixElement(rows=rows)

    def add_row(self, buttons):
        self._buttons.append([None] * len(buttons))
        self._orig_buttons.append(buttons)
        for index, button in enumerate(buttons):
            self._button_coordinates[button] = (
             index, len(self._buttons) - 1)
            self.register_control_element(button)

        if self._max_row_width < len(buttons):
            self._max_row_width = len(buttons)
        return

    def width(self):
        return self._max_row_width

    def height(self):
        return len(self._buttons)

    def send_value(self, column, row, value, force=False):
        assert in_range(value, 0, 128)
        assert in_range(column, 0, self.width())
        assert in_range(row, 0, self.height())
        if len(self._buttons[row]) > column:
            button = self._buttons[row][column]
            if button:
                button.send_value(value, force=force)

    def set_light(self, column, row, value):
        assert in_range(column, 0, self.width())
        assert in_range(row, 0, self.height())
        if len(self._buttons[row]) > column:
            button = self._buttons[row][column]
            if button:
                button.set_light(value)

    def get_button(self, column, row):
        assert in_range(column, 0, self.width())
        assert in_range(row, 0, self.height())
        if len(self._buttons[row]) > column:
            return self._buttons[row][column]

    def reset(self):
        for button in self:
            if button:
                button.reset()

    def __iter__(self):
        for j, i in product(xrange(self.height()), xrange(self.width())):
            button = self.get_button(i, j)
            yield button

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return map(self._do_get_item, range(*indices))
        else:
            if index < 0:
                index += len(self)
            return self._do_get_item(index)

    def _do_get_item(self, index):
        assert in_range(index, 0, len(self)), b'Index out of range'
        row, col = divmod(index, self.width())
        return self.get_button(col, row)

    def __len__(self):
        return self.width() * self.height()

    def iterbuttons(self):
        for j, i in product(xrange(self.height()), xrange(self.width())):
            button = self.get_button(i, j)
            yield (button, (i, j))

    def on_nested_control_element_value(self, value, sender):
        x, y = self._button_coordinates[sender]
        assert self._buttons[y][x]
        is_momentary = getattr(sender, b'is_momentary', const(None))()
        self.notify_value(value, x, y, is_momentary)
        return

    def on_nested_control_element_received(self, control):
        x, y = self._button_coordinates[control]
        self._buttons[y][x] = control

    def on_nested_control_element_lost(self, control):
        x, y = self._button_coordinates[control]
        self._buttons[y][x] = None
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Framework/ButtonMatrixElement.pyc
