# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launch_Control_XL\SkinDefault.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import Skin
from _Framework.ButtonElement import Color

class Defaults:

    class DefaultButton:
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)


class BiLedColors:

    class Mixer:
        SoloOn = Color(60)
        SoloOff = Color(28)
        MuteOn = Color(29)
        MuteOff = Color(47)
        ArmSelected = Color(15)
        ArmUnselected = Color(13)
        TrackSelected = Color(62)
        TrackUnselected = Color(29)
        NoTrack = Color(0)
        Sends = Color(47)
        Pans = Color(60)

    class Device:
        Parameters = Color(13)
        NoDevice = Color(0)
        BankSelected = Color(15)
        BankUnselected = Color(0)


def make_default_skin():
    return Skin(Defaults)


def make_biled_skin():
    return Skin(BiLedColors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launch_Control_XL/SkinDefault.pyc
