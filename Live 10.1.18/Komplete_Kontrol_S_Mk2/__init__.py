# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .komplete_kontrol_s_mk2 import Komplete_Kontrol_S_Mk2
from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: [b'Komplete Kontrol DAW - 1']}


def create_instance(c_instance):
    return Komplete_Kontrol_S_Mk2(c_instance=c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Komplete_Kontrol_S_Mk2/__init__.pyc
