# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\__init__.py
# Compiled at: 2020-07-20 20:22:59
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.capabilities import controller_id, CONTROLLER_ID_KEY, inport, NOTES_CC, outport, PORTS_KEY, REMOTE, SCRIPT
from .blackstar_live_logic import Blackstar_Live_Logic

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=10196, product_ids=[
                         4097], model_name=[
                         b'Live Logic MIDI Controller']), 
       PORTS_KEY: [
                 inport(props=[SCRIPT, REMOTE, NOTES_CC]),
                 outport(props=[SCRIPT, REMOTE, NOTES_CC])]}


def create_instance(c_instance):
    return Blackstar_Live_Logic(c_instance=c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Blackstar_Live_Logic/__init__.pyc
