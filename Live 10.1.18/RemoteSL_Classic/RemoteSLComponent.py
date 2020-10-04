# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL_Classic\RemoteSLComponent.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *

class RemoteSLComponent:
    """Baseclass for a subcomponent of the RemoteSL.
    Just defines some handy shortcuts to the main scripts functions...
    for more details about the methods, see the RemoteSLs doc strings
    """

    def __init__(self, remote_sl_parent):
        self.__parent = remote_sl_parent
        self.__support_mkII = False

    def application(self):
        return self.__parent.application()

    def song(self):
        return self.__parent.song()

    def send_midi(self, midi_event_bytes):
        self.__parent.send_midi(midi_event_bytes)

    def request_rebuild_midi_map(self):
        self.__parent.request_rebuild_midi_map()

    def disconnect(self):
        pass

    def build_midi_map(self, script_handle, midi_map_handle):
        pass

    def refresh_state(self):
        pass

    def update_display(self):
        pass

    def cc_status_byte(self):
        return CC_STATUS + SL_MIDI_CHANNEL

    def support_mkII(self):
        return self.__support_mkII

    def set_support_mkII(self, support_mkII):
        self.__support_mkII = support_mkII
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/RemoteSL_Classic/RemoteSLComponent.pyc
