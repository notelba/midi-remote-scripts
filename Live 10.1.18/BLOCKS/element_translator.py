# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BLOCKS\element_translator.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals

class ElementTranslator(object):

    def __init__(self, elements=None, feedback_channel=None, non_feedback_channel=None, *a, **k):
        super(ElementTranslator, self).__init__(*a, **k)
        assert elements is not None
        self._elements = elements
        self._feedback_channel = feedback_channel
        self._non_feedback_channel = non_feedback_channel
        return

    def set_enabled(self, enable):
        for element in self._elements:
            channel = self._non_feedback_channel
            if enable:
                element.reset_state()
                channel = self._feedback_channel
            element.set_channel(channel)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/BLOCKS/element_translator.pyc
