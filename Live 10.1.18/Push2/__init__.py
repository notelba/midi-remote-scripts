# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals

def get_capabilities():
    from ableton.v2.control_surface import capabilities as caps
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=10626, product_ids=[6503], model_name=b'Ableton Push 2'), 
       caps.PORTS_KEY: [
                      caps.inport(props=[caps.HIDDEN, caps.NOTES_CC, caps.SCRIPT]),
                      caps.inport(props=[]),
                      caps.outport(props=[caps.HIDDEN, caps.NOTES_CC, caps.SYNC, caps.SCRIPT]),
                      caps.outport(props=[])], 
       caps.TYPE_KEY: b'push2', 
       caps.AUTO_LOAD_KEY: True}


def create_instance(c_instance):
    from .push2 import Push2
    from .push2_model import Root, Sender
    root = Root(sender=Sender(message_sink=c_instance.send_model_update, process_connected=c_instance.process_connected))
    return Push2(c_instance=c_instance, model=root, decoupled_parameter_list_change_notifications=True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/__init__.pyc
