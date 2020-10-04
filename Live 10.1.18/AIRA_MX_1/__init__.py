# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AIRA_MX_1\__init__.py
# Compiled at: 2020-07-31 16:19:16
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, SCRIPT, controller_id, inport, outport
from .RolandMX1 import RolandMX1

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410, product_ids=[
                         419], model_name=[
                         b'MX-1']), 
       PORTS_KEY: [
                 inport(props=[]),
                 inport(props=[SCRIPT]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return RolandMX1(c_instance=c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/AIRA_MX_1/__init__.pyc
