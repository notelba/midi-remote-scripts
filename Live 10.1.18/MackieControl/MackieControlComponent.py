# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\MackieControlComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
import Live

class MackieControlComponent:
    """Baseclass for every 'sub component' of the Mackie Control. Just offers some """

    def __init__(self, main_script):
        self.__main_script = main_script

    def destroy(self):
        self.__main_script = None
        return

    def main_script(self):
        return self.__main_script

    def shift_is_pressed(self):
        return self.__main_script.shift_is_pressed()

    def option_is_pressed(self):
        return self.__main_script.option_is_pressed()

    def control_is_pressed(self):
        return self.__main_script.control_is_pressed()

    def alt_is_pressed(self):
        return self.__main_script.alt_is_pressed()

    def song(self):
        return self.__main_script.song()

    def script_handle(self):
        return self.__main_script.handle()

    def application(self):
        return self.__main_script.application()

    def send_midi(self, bytes):
        self.__main_script.send_midi(bytes)

    def request_rebuild_midi_map(self):
        self.__main_script.request_rebuild_midi_map()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MackieControl/MackieControlComponent.pyc
