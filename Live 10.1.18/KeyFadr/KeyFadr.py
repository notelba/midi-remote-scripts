# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyFadr\KeyFadr.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from KeyPad import KeyPad

class KeyFadr(KeyPad):
    """
    Reloop KeyFadr controller script.
    """
    _encoder_range = range(80, 72, -1)
    _product_model_id = 102

    def __init__(self, *a, **k):
        super(KeyFadr, self).__init__(*a, **k)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyFadr/KeyFadr.pyc
