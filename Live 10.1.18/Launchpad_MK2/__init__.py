# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .Launchpad_MK2 import Launchpad_MK2
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, SYNC, REMOTE

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[
                         105,
                         106,
                         107,
                         108,
                         109,
                         110,
                         111,
                         112,
                         113,
                         114,
                         115,
                         116,
                         117,
                         118,
                         119,
                         120], model_name=[
                         b'Launchpad MK2',
                         b'Launchpad MK2 2',
                         b'Launchpad MK2 3',
                         b'Launchpad MK2 4',
                         b'Launchpad MK2 5',
                         b'Launchpad MK2 6',
                         b'Launchpad MK2 7',
                         b'Launchpad MK2 8',
                         b'Launchpad MK2 9',
                         b'Launchpad MK2 10',
                         b'Launchpad MK2 11',
                         b'Launchpad MK2 12',
                         b'Launchpad MK2 13',
                         b'Launchpad MK2 14',
                         b'Launchpad MK2 15',
                         b'Launchpad MK2 16']), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SCRIPT, SYNC, REMOTE])]}


def create_instance(c_instance):
    return Launchpad_MK2(c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_MK2/__init__.pyc
