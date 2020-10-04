# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import *
from .Launchpad import Launchpad

def create_instance(c_instance):
    return Launchpad(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=4661, product_ids=[
                         14, 32, 54], model_name=[
                         b'Launchpad', b'Launchpad S', b'Launchpad Mini']), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE, SCRIPT]),
                 outport(props=[NOTES_CC, REMOTE, SCRIPT])]}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad/__init__.pyc
