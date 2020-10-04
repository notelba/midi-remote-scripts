# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import controller_id, inport, outport, AUTO_LOAD_KEY, CONTROLLER_ID_KEY, FIRMWARE_KEY, HIDDEN, NOTES_CC, PORTS_KEY, SCRIPT, SYNC, TYPE_KEY
from .firmware_handling import get_provided_firmware_version
from .push import Push

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[21], model_name=b'Ableton Push'), 
       PORTS_KEY: [
                 inport(props=[HIDDEN, NOTES_CC, SCRIPT]),
                 inport(props=[]),
                 outport(props=[HIDDEN, NOTES_CC, SYNC, SCRIPT]),
                 outport(props=[])], 
       TYPE_KEY: b'push', 
       FIRMWARE_KEY: get_provided_firmware_version(), 
       AUTO_LOAD_KEY: True}


def create_instance(c_instance):
    """ Creates and returns the Push script """
    return Push(c_instance=c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push/__init__.pyc
