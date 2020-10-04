# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import NOTES_CC, PORTS_KEY, SUGGESTED_PORT_NAMES_KEY, REMOTE, SCRIPT, inport, outport
from .akai_force_mpc import Akai_Force_MPC

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: [
                                b'Akai Network - DAW Control'], 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return Akai_Force_MPC(c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Akai_Force_MPC/__init__.pyc
