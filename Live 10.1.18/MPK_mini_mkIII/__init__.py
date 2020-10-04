# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPK_mini_mkIII\__init__.py
# Compiled at: 2020-07-20 20:22:59
from __future__ import absolute_import, print_function, unicode_literals
from _Generic.GenericScript import GenericScript
import Live
from .config import *

def create_instance(c_instance):
    """ The generic script can be customised by using parameters (see config.py). """
    return GenericScript(c_instance, Live.MidiMap.MapMode.absolute, Live.MidiMap.MapMode.absolute, DEVICE_CONTROLS, TRANSPORT_CONTROLS, VOLUME_CONTROLS, TRACKARM_CONTROLS, BANK_CONTROLS, CONTROLLER_DESCRIPTION)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[73], model_name=b'MPK mini 3'), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, REMOTE, SCRIPT]), outport(props=[SCRIPT])]}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MPK_mini_mkIII/__init__.pyc
