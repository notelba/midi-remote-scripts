# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Novation_Impulse\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .Novation_Impulse import Novation_Impulse

def create_instance(c_instance):
    return Novation_Impulse(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[25], model_name=b'Impulse 25'), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE, SCRIPT]),
                 inport(props=[NOTES_CC, REMOTE]),
                 outport(props=[NOTES_CC, REMOTE, SCRIPT])]}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Novation_Impulse/__init__.pyc
