# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_A_PRO\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .Roland_A_PRO import Roland_A_PRO
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, REMOTE

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1410, product_ids=[271], model_name=b'A-PRO'), 
       PORTS_KEY: [
                 inport(props=[]),
                 inport(props=[NOTES_CC, REMOTE]),
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}


def create_instance(c_instance):
    return Roland_A_PRO(c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Roland_A_PRO/__init__.pyc
