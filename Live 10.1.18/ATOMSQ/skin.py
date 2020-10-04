# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\skin.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from .colors import Mono, Rgb

class Colors:

    class DefaultButton:
        On = Mono.ON
        Off = Mono.OFF
        Disabled = Mono.OFF

    class Transport:
        PlayOn = Mono.ON
        PlayOff = Mono.OFF

    class Recording:
        On = Mono.ON
        Transition = Mono.ON
        Off = Mono.OFF

    class Mixer:
        ArmOn = Mono.ON
        ArmOff = Mono.OFF
        SoloOn = Mono.ON
        SoloOff = Mono.OFF
        MuteOn = Mono.ON
        MuteOff = Mono.OFF

    class Device:
        Navigation = Mono.OFF
        NavigationPressed = Mono.ON

    class Session:
        ClipEmpty = Mono.OFF
        ClipTriggeredPlay = Mono.ON
        ClipTriggeredRecord = Mono.ON
        ClipStopped = Mono.ON
        ClipStarted = Mono.ON
        ClipRecording = Mono.ON
        RecordButton = Mono.OFF


class RgbColors:

    class DefaultButton:
        On = Rgb.ON
        Off = Rgb.OFF
        Disabled = Rgb.OFF

    class Transport:
        PlayOn = Rgb.GREEN
        PlayOff = Rgb.GREEN_DIM

    class Session:
        ClipEmpty = Rgb.OFF
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        RecordButton = Rgb.RED_HALF
        Scene = Rgb.GREEN_HALF
        NoScene = Rgb.OFF
        SceneTriggered = Rgb.GREEN_BLINK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF

    class View:
        DetailOn = Rgb.YELLOW
        DetailOff = Rgb.YELLOW_HALF
        MainOn = Rgb.BLUE
        MainOff = Rgb.BLUE_HALF
        ClipOn = Rgb.PURPLE
        ClipOff = Rgb.PURPLE_HALF
        BrowserOn = Rgb.GREEN
        BrowserOff = Rgb.GREEN_HALF


skin = Skin(Colors)
rgb_skin = Skin(RgbColors)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/skin.pyc
