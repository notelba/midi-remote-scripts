# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .MiniLab import MiniLab
import _Framework.Capabilities as caps

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=7285, product_ids=[516], model_name=[b'Arturia MINILAB']), 
       caps.PORTS_KEY: [
                      caps.inport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE]),
                      caps.outport(props=[caps.SCRIPT])]}


def create_instance(c_instance):
    return MiniLab(c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MiniLab/__init__.pyc
