# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.Capabilities as caps
from .Launchkey_MK2 import Launchkey_MK2

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=4661, product_ids=[
                              31610, 31866, 32122, 123, 124, 125], model_name=[
                              b'Launchkey MK2 25', b'Launchkey MK2 49', b'Launchkey MK2 61']), 
       caps.PORTS_KEY: [
                      caps.inport(props=[]),
                      caps.inport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE]),
                      caps.outport(props=[]),
                      caps.outport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE])]}


def create_instance(c_instance):
    return Launchkey_MK2(c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_MK2/__init__.pyc
