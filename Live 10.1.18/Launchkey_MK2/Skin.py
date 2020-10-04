# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\Skin.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import Skin
from .Colors import Rgb

class Colors:

    class Session:
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipEmpty = Rgb.BLACK
        RecordButton = Rgb.RED_HALF
        StopClip = Rgb.GREEN
        StopClipTriggered = Rgb.GREEN_BLINK
        StoppedClip = Rgb.GREEN_HALF
        Enabled = Rgb.YELLOW

    class Mode:
        DeviceMode = Rgb.PURPLE_HALF
        DeviceModeOn = Rgb.PURPLE
        PanMode = Rgb.ORANGE_HALF
        PanModeOn = Rgb.ORANGE
        Send0Mode = Rgb.DARK_BLUE_HALF
        Send0ModeOn = Rgb.BRIGHT_PURPLE
        Send1Mode = Rgb.BLUE_HALF
        Send1ModeOn = Rgb.BLUE
        Send2Mode = Rgb.LIGHT_BLUE_HALF
        Send2ModeOn = Rgb.LIGHT_BLUE
        Send3Mode = Rgb.MINT_HALF
        Send3ModeOn = Rgb.MINT
        Send4Mode = Rgb.DARK_YELLOW_HALF
        Send4ModeOn = Rgb.DARK_YELLOW
        Send5Mode = Rgb.YELLOW_HALF
        Send5ModeOn = Rgb.YELLOW
        Disabled = Rgb.BLACK

    class Device:
        Bank = Rgb.DARK_PURPLE
        BestOfBank = Rgb.PURPLE_HALF
        BankSelected = Rgb.PURPLE


def make_skin():
    return Skin(Colors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchkey_MK2/Skin.pyc
