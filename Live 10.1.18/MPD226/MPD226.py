# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPD226\MPD226.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from itertools import cycle, izip
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _MPDMkIIBase.MPDMkIIBase import MPDMkIIBase
from _MPDMkIIBase.ControlElementUtils import make_button, make_encoder, make_slider
PAD_CHANNEL = 1
PAD_IDS = [
 [
  81, 83, 84, 86], [74, 76, 77, 79], [67, 69, 71, 72], [60, 62, 64, 65]]

class MPD226(MPDMkIIBase):

    def __init__(self, *a, **k):
        super(MPD226, self).__init__(PAD_IDS, PAD_CHANNEL, *a, **k)
        with self.component_guard():
            self._create_device()
            self._create_transport()
            self._create_mixer()

    def _create_controls(self):
        super(MPD226, self)._create_controls()
        self._encoders = ButtonMatrixElement(rows=[
         [ make_encoder(identifier, 0 if index < 4 else 1, b'Encoder_%d' % index) for index, identifier in izip(xrange(8), cycle(xrange(22, 26)))
         ]])
        self._sliders = ButtonMatrixElement(rows=[
         [ make_slider(identifier, 0 if index < 4 else 1, b'Slider_%d' % index) for index, identifier in izip(xrange(8), cycle(xrange(12, 16)))
         ]])
        self._control_buttons = ButtonMatrixElement(rows=[
         [ make_button(identifier, 0 if index < 4 else 1, b'Control_Button_%d' % index) for index, identifier in izip(xrange(8), cycle(xrange(32, 36)))
         ]])
        self._play_button = make_button(118, 0, b'Play_Button')
        self._stop_button = make_button(117, 0, b'Stop_Button')
        self._record_button = make_button(119, 0, b'Record_Button')
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MPD226/MPD226.pyc
