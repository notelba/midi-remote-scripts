# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .Axiom_AIR_25_49_61 import Axiom_AIR_25_49_61
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[8243], model_name=b'Axiom AIR 49'), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC]),
                 inport(props=[SCRIPT]),
                 inport(props=[NOTES_CC]),
                 outport(props=[NOTES_CC]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Axiom_AIR_25_49_61(c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_AIR_25_49_61/__init__.pyc
