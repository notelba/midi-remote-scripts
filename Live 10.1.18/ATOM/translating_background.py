# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\translating_background.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import BackgroundComponent

class TranslatingBackgroundComponent(BackgroundComponent):

    def __init__(self, translation_channel, *a, **k):
        super(TranslatingBackgroundComponent, self).__init__(*a, **k)
        self._translation_channel = translation_channel

    def _clear_control(self, name, control):
        prior_control = self._control_map.get(name, None)
        if prior_control:
            if prior_control.name == b'Encoders':
                for encoder in prior_control:
                    encoder.use_default_message()

            prior_control.reset()
        super(TranslatingBackgroundComponent, self)._clear_control(name, control)
        if control:
            control.set_channel(self._translation_channel)
            if control.name == b'Pads':
                for button in control:
                    if button:
                        button.set_light(b'DefaultButton.RgbOff')

        return

    def update(self):
        super(BackgroundComponent, self).update()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/translating_background.pyc
