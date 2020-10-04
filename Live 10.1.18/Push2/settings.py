# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\settings.py
# Compiled at: 2020-07-31 16:17:47
from __future__ import absolute_import, print_function, unicode_literals
from pushbase.setting import OnOffSetting

def create_settings(preferences=None):
    preferences = preferences if preferences is not None else {}
    return {b'workflow': OnOffSetting(name=b'Workflow', value_labels=[
                   b'Scene', b'Clip'], default_value=True, preferences=preferences)}
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Push2/settings.pyc
