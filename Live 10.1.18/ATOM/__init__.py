# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from .atom import ATOM

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479, product_ids=[518], model_name=[b'ATOM']), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return ATOM(c_instance=c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/__init__.pyc
