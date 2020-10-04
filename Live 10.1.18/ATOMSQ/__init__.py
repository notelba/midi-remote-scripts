# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\__init__.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, SYNC, controller_id, inport, outport
from .atomsq import ATOMSQ

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=6479, product_ids=[522], model_name=[b'ATM SQ']), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SYNC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return ATOMSQ(c_instance=c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/__init__.pyc
