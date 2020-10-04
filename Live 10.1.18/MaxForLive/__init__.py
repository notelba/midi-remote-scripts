# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MaxForLive\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .MaxForLive import MaxForLive
from ableton.v2.control_surface.capabilities import GENERIC_SCRIPT_KEY

def get_capabilities():
    return {GENERIC_SCRIPT_KEY: True}


def create_instance(c_instance):
    return MaxForLive(c_instance=c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MaxForLive/__init__.pyc
