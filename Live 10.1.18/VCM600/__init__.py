# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\__init__.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from .VCM600 import VCM600

def create_instance(c_instance):
    """ Creates and returns the ADA1 script """
    return VCM600(c_instance)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/VCM600/__init__.pyc
