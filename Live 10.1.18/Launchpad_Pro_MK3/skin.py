# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro_MK3\skin.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import merge_skins, Skin
from novation.colors import Rgb
from novation.skin import skin as base_skin

class Colors:

    class Device:
        Navigation = Rgb.DARK_BLUE_HALF
        NavigationPressed = Rgb.WHITE

    class Mode:

        class Device:
            On = Rgb.DARK_BLUE
            Off = Rgb.WHITE_HALF

            class Bank:
                Selected = Rgb.DARK_BLUE
                Available = Rgb.WHITE_HALF

        class Sends:
            On = Rgb.VIOLET
            Off = Rgb.WHITE_HALF

            class Bank:
                Available = Rgb.WHITE_HALF

    class Recording:
        Off = Rgb.WHITE_HALF

    class Transport:
        PlayOff = Rgb.WHITE_HALF
        PlayOn = Rgb.GREEN
        ContinueOff = Rgb.AQUA
        ContinueOn = Rgb.RED_HALF
        CaptureOff = Rgb.BLACK
        CaptureOn = Rgb.CREAM
        TapTempo = Rgb.CREAM

    class Quantization:
        Off = Rgb.RED_HALF
        On = Rgb.AQUA


skin = merge_skins(*(base_skin, Skin(Colors)))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro_MK3/skin.pyc
