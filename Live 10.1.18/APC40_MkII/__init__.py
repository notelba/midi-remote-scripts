# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC40_MkII\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, SYNC, REMOTE, controller_id, inport, outport
from .APC40_MkII import APC40_MkII

def create_instance(c_instance):
    return APC40_MkII(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[41], model_name=b'Akai APC40 MkII'), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[SYNC, SCRIPT, REMOTE])]}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/APC40_MkII/__init__.pyc
