# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\Capabilities.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
GENERIC_SCRIPT_KEY = b'generic_script'
PORTS_KEY = b'ports'
CONTROLLER_ID_KEY = b'controller_id'
TYPE_KEY = b'surface_type'
FIRMWARE_KEY = b'firmware_version'
AUTO_LOAD_KEY = b'auto_load'
VENDORID = b'vendor_id'
PRODUCTIDS = b'product_ids'
MODEL_NAMES = b'model_names'
DIRECTIONKEY = b'direction'
PORTNAMEKEY = b'name'
MACNAMEKEY = b'mac_name'
PROPSKEY = b'props'
HIDDEN = b'hidden'
SYNC = b'sync'
SCRIPT = b'script'
NOTES_CC = b'notes_cc'
REMOTE = b'remote'
PLAIN_OLD_MIDI = b'plain_old_midi'

def __create_port_dict(direction, port_name, mac_name, props):
    assert isinstance(direction, basestring)
    assert isinstance(port_name, basestring)
    assert props == None or type(props) is list
    if props:
        for prop in props:
            assert isinstance(prop, basestring)

    assert mac_name == None or isinstance(mac_name, basestring)
    capabilities = {DIRECTIONKEY: direction, PORTNAMEKEY: port_name, PROPSKEY: props}
    if mac_name:
        capabilities[MACNAMEKEY] = mac_name
    return capabilities


def inport(port_name=b'', props=[], mac_name=None):
    """ Generate a ..."""
    return __create_port_dict(b'in', port_name, mac_name, props)


def outport(port_name=b'', props=[], mac_name=None):
    """ Generate a ..."""
    return __create_port_dict(b'out', port_name, mac_name, props)


def controller_id(vendor_id, product_ids, model_name):
    """ Generate a hardwareId dict"""
    assert type(vendor_id) is int
    assert type(product_ids) is list
    for product_id in product_ids:
        assert type(product_id) is int

    assert isinstance(model_name, (basestring, list))
    if isinstance(model_name, basestring):
        model_names = [
         model_name]
    else:
        model_names = model_name
    return {VENDORID: vendor_id, PRODUCTIDS: product_ids, MODEL_NAMES: model_names}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Framework/Capabilities.pyc
