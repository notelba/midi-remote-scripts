# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\__init__.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from .MxDCore import MxDCore as _MxDCore
import sys, warnings

def set_manager(manager):
    assert manager != None
    assert _MxDCore.instance == None
    _MxDCore.instance = _MxDCore()
    _MxDCore.instance.set_manager(manager)
    return


def disconnect():
    _MxDCore.instance.disconnect()
    del _MxDCore.instance


def execute_command(device_id, object_id, command, arguments):
    assert _MxDCore.instance != None
    assert isinstance(arguments, (str, unicode))
    if hasattr(_MxDCore.instance, command):
        try:
            with warnings.catch_warnings(record=True) as (caught_warnings):
                _MxDCore.instance.update_device_context(device_id, object_id)
                function = getattr(_MxDCore.instance, command)
                function(device_id, object_id, arguments)
                for warning in caught_warnings:
                    _MxDCore.instance._warn(device_id, object_id, str(warning.message))

        except:
            if sys.exc_info()[0].__name__ == b'RuntimeError':
                assert_reason = str(sys.exc_info()[1])
            else:
                assert_reason = b'Invalid syntax'
            _MxDCore.instance._raise(device_id, object_id, assert_reason)

    else:
        _MxDCore.instance._raise(device_id, object_id, b'Unknown command: ' + command)
    return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_MxDCore/__init__.pyc
