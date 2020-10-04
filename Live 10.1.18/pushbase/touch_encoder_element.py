# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\touch_encoder_element.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import TouchEncoderElement as TouchEncoderElementBase

class TouchEncoderObserver(object):
    """ Interface for observing the state of one or more TouchEncoderElements """

    def on_encoder_touch(self, encoder):
        pass

    def on_encoder_parameter(self, encoder):
        pass


class TouchEncoderElement(TouchEncoderElementBase):
    """ Class representing an encoder that is touch sensitive """

    def __init__(self, undo_step_handler=None, undo_group=None, delete_handler=None, *a, **k):
        super(TouchEncoderElement, self).__init__(*a, **k)
        self._trigger_undo_step = False
        self._undo_step_open = False
        self._undo_step_handler = undo_step_handler
        self._undo_group = undo_group
        self._delete_handler = delete_handler
        self.set_observer(None)
        return

    def set_observer(self, observer):
        if observer is None:
            observer = TouchEncoderObserver()
        self._observer = observer
        return

    def on_nested_control_element_value(self, value, control):
        self._trigger_undo_step = value
        if value:
            param = self.mapped_parameter()
            if self._delete_handler and self._delete_handler.is_deleting and param:
                self._delete_handler.delete_clip_envelope(param)
            else:
                self.begin_gesture()
                self._begin_undo_step()
                self._observer.on_encoder_touch(self)
                self.notify_touch_value(value)
        else:
            self._end_undo_step()
            self._observer.on_encoder_touch(self)
            self.notify_touch_value(value)
            self.end_gesture()

    def connect_to(self, parameter):
        if parameter != self.mapped_parameter():
            self.last_mapped_parameter = parameter
            super(TouchEncoderElement, self).connect_to(parameter)
            self._observer.on_encoder_parameter(self)

    def release_parameter(self):
        if self.mapped_parameter() != None:
            super(TouchEncoderElement, self).release_parameter()
            self._observer.on_encoder_parameter(self)
        return

    def receive_value(self, value):
        self._begin_undo_step()
        super(TouchEncoderElement, self).receive_value(value)

    def disconnect(self):
        super(TouchEncoderElement, self).disconnect()
        self._undo_step_handler = None
        return

    def _begin_undo_step(self):
        if self._undo_step_handler and self._trigger_undo_step:
            self._undo_step_handler.begin_undo_step(client=self._undo_group)
            self._trigger_undo_step = False
            self._undo_step_open = True

    def _end_undo_step(self):
        if self._undo_step_handler and self._undo_step_open:
            self._undo_step_handler.end_undo_step(client=self._undo_group)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/pushbase/touch_encoder_element.pyc