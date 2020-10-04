# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC20\ShiftableZoomingComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent

class ShiftableZoomingComponent(DeprecatedSessionZoomingComponent):
    """ Special ZoomingComponent that uses clip stop buttons for stop all when zoomed """

    def __init__(self, session, stop_buttons, *a, **k):
        super(ShiftableZoomingComponent, self).__init__(session, *a, **k)
        self._stop_buttons = stop_buttons
        self._ignore_buttons = False
        for button in self._stop_buttons:
            assert isinstance(button, ButtonElement)
            button.add_value_listener(self._stop_value, identify_sender=True)

    def disconnect(self):
        super(ShiftableZoomingComponent, self).disconnect()
        for button in self._stop_buttons:
            button.remove_value_listener(self._stop_value)

    def set_ignore_buttons(self, ignore):
        if not isinstance(ignore, type(False)):
            raise AssertionError
            if self._ignore_buttons != ignore:
                self._ignore_buttons = ignore
                self._is_zoomed_out or self._session.set_enabled(not ignore)
            self.update()

    def update(self):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self).update()
        elif self.is_enabled():
            if self._scene_bank_buttons != None:
                for button in self._scene_bank_buttons:
                    button.turn_off()

        return

    def _stop_value(self, value, sender):
        if not value in range(128):
            raise AssertionError
            assert sender != None
            if self.is_enabled() and not self._ignore_buttons and self._is_zoomed_out and (value != 0 or not sender.is_momentary()):
                self.song().stop_all_clips()
        return

    def _zoom_value(self, value):
        if not self._zoom_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled():
                if self._zoom_button.is_momentary():
                    self._is_zoomed_out = value > 0
                else:
                    self._is_zoomed_out = not self._is_zoomed_out
                if self._ignore_buttons or self._is_zoomed_out:
                    self._scene_bank_index = int(self._session.scene_offset() / self._session.height() / self._buttons.height())
                else:
                    self._scene_bank_index = 0
                self._session.set_enabled(not self._is_zoomed_out)
                if self._is_zoomed_out:
                    self.update()
        return

    def _matrix_value(self, value, x, y, is_momentary):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._matrix_value(value, x, y, is_momentary)

    def _nav_up_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_up_value(value)

    def _nav_down_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_down_value(value)

    def _nav_left_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_left_value(value)

    def _nav_right_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_right_value(value)

    def _scene_bank_value(self, value, sender):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._scene_bank_value(value, sender)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC20/ShiftableZoomingComponent.pyc
